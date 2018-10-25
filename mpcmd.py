from multiprocessing import Process, Pipe
import subprocess
import json
import time
import sys
#import ast
import os


class TsharkJsonProcess:
    """Spawns the Tshark process with JSON output and parses it line for line.
    When a complete JSON object has been constructed, it is sent through the pipe,
    to the monitor process.
    """

    def __init__(self):
        self.command = '/usr/local/bin/tshark -i wlan0 -Q -T fields -E separator=\; -e "wlan.fc.type_subtype" -e "wlan_radio.signal_dbm" -e "wlan.ssid" -e "wlan.addr" -e "wlan.sa" -e "radiotap.present.channel" -e "wlan.country_info.code" 2> /dev/null'
        self.wlan_channel_hopping = True
        self.wlan_channel = 0

    def run_command(self, command, process_out):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        while True:
            line = process.stdout.readline().rstrip()
            if line.decode() != '':
                process_out.send(line.decode())

    def start(self, process_out):
        self.tshark_process = Process(target=self.run_command, args=(self.command, process_out,))
        self.tshark_process.start()


class TsharkJsonMonitor(TsharkJsonProcess):
    """Spawns the Monitor process, that checks the Tshark pipe for output. All received output,
    is handed over to the controller pipe. If the monitor sees no output from Tshark,
    for a given time (patience limit), it assumes something went wrong. It then kills the process,
    and creates a new one.
    """

    def __init__(self):
        self.patience_timer = 0
        self.patience_limit = 3000
        self.monitor_in, self.monitor_out = Pipe()
        self.monitor = Process(target=self.monitor, args=(self.monitor_out,))

    def start(self):
        self.monitor.start()

    def start_process(self):
        self.process = TsharkJsonProcess()
        self.process_in, self.process_out = Pipe()
        self.process.start(self.process_out)

    def monitor(self, monitor_out):
        self.start_process()
        while True:
            self.patience_timer += 1
            if self.process_in.poll():
                monitor_out.send(self.process_in.recv())
                self.patience_timer = 0
            if self.patience_timer == self.patience_limit:
                self.process.tshark_process.terminate()
                self.start_process()
            time.sleep(0.01)


class TsharkJsonController(TsharkJsonMonitor):
    """The controller is the facade to the main code. The only interesting part, for the main code,
    is the pipe, where all data from the monitor comes out.
    """

    def __init__(self):
        self.monitor = TsharkJsonMonitor()
        self.pipe = self.monitor.monitor_in

    def start(self):
        self.monitor.start()
