# from multiprocessing import Process, Pipe
# import subprocess
# import sys
#
# def run_command():
#     command = '/Users/ghost/anaconda/bin/python /Users/ghost/Documents/Github/WiPi/printer.py'
#
# def execute(cmd):
#     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
#     for stdout_line in iter(popen.stdout.readline, ""):
#         yield stdout_line
#     popen.stdout.close()
#     return_code = popen.wait()
#     if return_code:
#         raise subprocess.CalledProcessError(return_code, cmd)
#
# def execute2(command, south_pipe):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#
#     # Poll process for new output until finished
#     while True:
#         nextline = process.stdout.readline().decode("UTF-8")
#         if nextline == '' and process.poll() is not None:
#             break
#         else:
#             south_pipe.send(nextline)
#         # sys.stdout.write(nextline)
#         # sys.stdout.flush()
#
#     output = process.communicate()[0]
#     exitCode = process.returncode
#
#     if (exitCode == 0):
#         return output
#     else:
#         raise ProcessException(command, exitCode, output)
#
# def main(north_pipe):
#     while True:
#         if north_pipe.poll():
#             print(north_pipe.recv())
# # Example
#
# north_pipe, south_pipe = Pipe()
# p1 = Process(target=execute2, args=('/Users/ghost/anaconda/bin/python /Users/ghost/Documents/Github/WiPi/printer.py', south_pipe,))
# p1.start()
# main(north_pipe)
# p1.join()

from subprocess import Popen, PIPE
import json
import sys

def run(command):
    process = Popen(command, stdout=PIPE, stdin=PIPE, shell=True)
    iffie = ''
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        try_parsing = False
        text = line.decode()
        if text.replace(' ', '') == ',':
            try_parsing = True
            print('try')
        try:
            try_parsing = False
            iffie = iffie.lstrip('[')
            obj = json.loads(iffie.replace('\n', ''))
            print('angelic')
            iffie = ''
        except Exception as e:
            iffie += text + '\n'


if __name__ == "__main__":
    # while True:
    #     try:
    #         try_parsing = False
    #         iffie = ''
    #         jsons = []
    #         counter = 0
    #         for path in run("/usr/local/bin/tshark -T json"):
    #             text = path.decode()
    #             if text.replace(' ', '') == ',':
    #                 try_parsing = True
    #                 print('try')
    #             try:
    #                 try_parsing = False
    #                 iffie = iffie.lstrip('[')
    #                 obj = json.loads(iffie.replace('\n', ''))
    #                 print('angelic')
    #                 iffie = ''
    #             except Exception as e:
    #                 iffie += text + '\n'
    #     except KeyboardInterrupt:
    #         print(iffie)
    #         sys.exit()
    run("/usr/local/bin/tshark -T json")
