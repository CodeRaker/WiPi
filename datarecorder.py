from mpcmd import TsharkJsonController
import datetime

class DataRecorder:

    def __init__(self, Game):
        self.game = Game
        self.total_packets = 0
        self.total_packets_per_second = 0
        self.total_packets_per_second_counter = 0
        self.total_beacons = 0
        self.total_beacons_per_second = 0
        self.total_beacons_per_second_counter = 0
        self.total_probes = 0
        self.devices = {}
        self.vendor_dict = {}
        self.load_vendors
        self.ts = TsharkJsonController()
        self.ts.start()

    def load_vendors(self):
        with open ('/root/wipi/vendors.txt') as f:
            try:
                for line in f:
                    if "(base 16)" in line:
                        line_list = line.rstrip('\n').split('(base 16)')
                        line_list[0] = line_list[0].replace(' ', '')
                        line_list[1] = line_list[1].replace('\t', '')
                        self.vendor_dict[line_list[0]] = line_list[1]
            except:
                pass

    #Update probe/device data
    def update(self):
        """
        Packet List contents
        --------------------
        0: "wlan.fc.type_subtype"
        1: "wlan_radio.signal_dbm"
        2: "wlan.ssid"
        3: "wlan.addr"
        4: "wlan.sa"
        5: "radiotap.present.channel"
        6: "wlan.country_info.code"

        Device List contents
        --------------------
        Key: MAC address
        0: First Seen timestamp #datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M")
        1: Last Seen timestamp #datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M")
        2: Probe Count
        3: SSIDs requested - List
        4: Device Vendor
        5: Last signal strength
        6: Country Code
        """

        #Keep track of packets per second
        if self.game.frameCounter == 1:
            self.total_beacons_per_second_counter = 0
            self.total_packets_per_second_counter = 0
        elif self.game.frameCounter == 60:
            self.total_packets_per_second = self.total_packets_per_second_counter
            self.total_beacons_per_second = self.total_beacons_per_second_counter

        #Message coming from mpcmd
        if self.ts.pipe.poll():
            text = self.ts.pipe.recv()
            packet_list = text.split(';')
            self.total_packets += 1
            self.total_packets_per_second_counter += 1

            #Is a Beacon
            if packet_list[0] == '8':
                self.total_beacons += 1
                self.total_beacons_per_second_counter += 1

            #Is a probe request
            elif packet_list[0] in ['4']:
                self.total_probes += 1

                #Is a new probe request
                vendor_selector = packet_list[4].strip(':')
                if packet_list[4] not in self.devices.keys():
                    # Key: MAC address
                    self.devices[packet_list[4]] = [
                    # 0: First Seen timestamp
                    datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M"),
                    # 1: Last Seen timestamp
                    datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M"),
                    # 2: Probe Count
                    1,
                    # 3: SSIDs requested - List
                    [packet_list[2]],
                    # 4: Device Vendor
                    self.vendor_dict[vendor_selector[:6]],
                    # 5: Last signal strength
                    packet_list[1],
                    # 6: Country Code
                    packet_list[6]
                    ]

                #Is a known probe request
                else:
                    # 1: Last Seen timestamp
                    self.devices[packet_list[4]][1] = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M")
                    # 2: Probe Count
                    self.devices[packet_list[4]][2] += 1
                    # 3: SSIDs requested - List
                    if packet_list[2] not in self.devices[packet_list[4]][3]:
                        self.devices[packet_list[4]][3].append(packet_list[2])
                    # 5: Last signal strength
                    self.devices[packet_list[4]][5] = packet_list[1]
