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
