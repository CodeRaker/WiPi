from multiprocessing import Process, Pipe
import subprocess
import json
import time

class TsharkJson:
    def __init__(self):
        self.command = ''
        self.northpipe, self.southpipe = Pipe()

    def run_command(self, command, southpipe):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        fail_count = 0
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
                southpipe.send(obj)
                text_container = ''
            except Exception as e:
                text_container += text + '\n'

    def run_process(self):
        self.process = Process(target=self.run_command, args=(self.command, self.southpipe,))
        self.process.start()


if __name__ == "__main__":
    tsharkjson = TsharkJson()
    tsharkjson.command = '/usr/local/bin/tshark -T json'
    tsharkjson.run_process()
    patience_timer = 0
    while True:
        patience_timer += 1
        time.sleep(0.01)
        if tsharkjson.northpipe.poll():
            test = tsharkjson.northpipe.recv()
            patience_timer = 0
        if patience_timer == 3000:
            print('killing')
            tsharkjson.process.terminate()
            del tsharkjson
            tsharkjson = TsharkJson()
            tsharkjson.command = '/usr/local/bin/tshark -T json'
            tsharkjson.run_process()
            patience_timer = 0
        print(str(patience_timer))
