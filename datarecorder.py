from mpcmd import TsharkJsonController


class DataRecorder:

    def __init__(self, Game):
        self.game = Game
        self.total_packets = 0
        self.total_packets_per_second = 0
        self.total_packets_per_second_cache = {}
        self.total_beacons = 0
        self.total_beacons_per_second = 0
        self.total_beacons_per_second_cache = {}
        self.total_probes = 0
        self.devices = {}
        self.ts = TsharkJsonController()
        self.ts.start()

    def update(self):
        self.total_packets_per_second_cache.pop(self.game.frameCounter, None)
        self.total_beacons_per_second_cache.pop(self.game.frameCounter, None)
        if self.ts.pipe.poll():
            text = self.ts.pipe.recv()
            packet_list = text.split(';')
            self.total_packets += 1
            self.total_packets_per_second_cache[self.game.frameCounter] = ''
            self.total_packets_per_second = len(self.total_packets_per_second_cache)
            if packet_list[0] == '8':
                self.total_beacons += 1
                self.total_beacons_per_second_cache[self.game.frameCounter] = ''
                self.total_beacons_per_second = len(self.total_beacons_per_second_cache)
            elif packet_list[0] in ['4','5']:
                self.total_probes += 1
                if packet_list[2] not in ['lichen','huron','CSCEmployee','']:
                    if packet_list[4] not in self.devices.keys():
                        if packet_list[2]:
                            self.devices[packet_list[4]] = [packet_list[2]]
                    else:
                        if packet_list[2] not in self.devices[packet_list[4]]:
                            self.devices[packet_list[4]].append(packet_list[2])
                    print(self.devices)
