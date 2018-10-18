from multiprocessing import Process, Pipe
import subprocess
import json
import time


class TsharkJsonProcess:

    def __init__(self):
        self.command = '/usr/local/bin/tshark -T json'

    def run_command(self, command, process_out):
        print('spawned'*10)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        text_container = ''
        try_parsing = False
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            try_parsing = False
            text = line.decode()
            if text.replace(' ', '') == ',':
                try_parsing = True
            try:
                try_parsing = False
                text_container = text_container.lstrip('[')
                obj = json.loads(text_container.replace('\n', ''))
                process_out.send(obj)
                text_container = ''
            except Exception as e:
                text_container += text + '\n'

    def start(self, process_out):
        self.tshark_process = Process(target=self.run_command, args=(self.command, process_out,))
        self.tshark_process.start()


class TsharkJsonMonitor(TsharkJsonProcess):

    def __init__(self):
        self.patience_timer = 0
        self.patience_limit = 1000
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
                print('monitor got one')
                monitor_out.send(self.process_in.recv())
                self.patience_timer = 0
            if self.patience_timer == self.patience_limit:
                print('patience limit reached')
                self.process.tshark_process.terminate()
                self.start_process()
            time.sleep(0.01)


class TsharkJsonController(TsharkJsonProcess, TsharkJsonMonitor):

    def __init__(self):
        self.monitor = TsharkJsonMonitor()
        self.pipe = self.monitor.monitor_in

    def start(self):
        self.monitor.start()


if __name__ == "__main__":
    ts = TsharkJsonController()
    ts.start()
    while True:
        if ts.pipe.poll():
            text = ts.pipe.recv()
            print(text)
