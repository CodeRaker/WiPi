from mpcmd import TsharkJsonController


class DataRecorder:

    def __init__(self, Game):
        self.game = Game
        self.total_packets = 0
        self.total_packets_per_second = 0
        self.total_packets_per_second_cache = {}
        self.ts = TsharkJsonController()
        self.ts.start()

    def update(self):
        self.total_packets_per_second_cache.pop(self.game.frameCounter, None)
        if self.ts.pipe.poll():
            text = self.ts.pipe.recv()
            self.total_packets += 1
            self.total_packets_per_second_cache[self.game.frameCounter] = ''
            self.total_packets_per_second = len(self.total_packets_per_second_cache)
