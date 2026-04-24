from pythonosc import udp_client, osc_server
from pythonosc.dispatcher import Dispatcher
import mido
import argparse
import threading
import time
import socket
from sys import exit

# The state is managed in the FL studio MIDI script
# Here only the MIDI-OSC mapping is carried out
'''Assignable controls are direct MIDI and are used for
(A) Control of the whole session (play, pause, etc) and ontrol of the Equalizer (e.g. Pro-Q)
(B) Control of the Compressor (dyn) e.g. Pro-C
(C) Control of the Reverb, ambience processor e.g. Pro-R
'''

PORT = 10023
MAPPING = {
    "fader": {
        "1": "/ch/17/mix/fader",
        "2": "/ch/18/mix/fader",
        "3": "/ch/19/mix/fader",
        "4": "/ch/20/mix/fader",
        "5": "/ch/21/mix/fader",
        "6": "/ch/22/mix/fader",
        "7": "/ch/23/mix/fader",
        "8": "/ch/24/mix/fader",
        "9": "/ch/25/mix/fader",
        "10": "/ch/26/mix/fader",
        "11": "/ch/27/mix/fader",
        "12": "/ch/28/mix/fader",
        "13": "/ch/29/mix/fader",
        "14": "/ch/30/mix/fader",
        "15": "/ch/31/mix/fader",
        "16": "/ch/32/mix/fader",
        "17": "/bus/01/mix/fader",
        "18": "/bus/02/mix/fader",
        "19": "/bus/03/mix/fader",
        "20": "/bus/04/mix/fader",
        "21": "/bus/05/mix/fader",
        "22": "/bus/06/mix/fader",
        "23": "/bus/07/mix/fader",
        "24": "/bus/08/mix/fader"
    },
    "on": { # MUTE function
        "1": "/ch/17/mix/on",
        "2": "/ch/18/mix/on",
        "3": "/ch/19/mix/on",
        "4": "/ch/20/mix/on",
        "5": "/ch/21/mix/on",
        "6": "/ch/22/mix/on",
        "7": "/ch/23/mix/on",
        "8": "/ch/24/mix/on",
        "9": "/ch/25/mix/on",
        "10": "/ch/26/mix/on",
        "11": "/ch/27/mix/on",
        "12": "/ch/28/mix/on",
        "13": "/ch/29/mix/on",
        "14": "/ch/30/mix/on",
        "15": "/ch/31/mix/on",
        "16": "/ch/32/mix/on",
        "17": "/bus/01/mix/on",
        "18": "/bus/02/mix/on",
        "19": "/bus/03/mix/on",
        "20": "/bus/04/mix/on",
        "21": "/bus/05/mix/on",
        "22": "/bus/06/mix/on",
        "23": "/bus/07/mix/on",
        "24": "/bus/08/mix/on"
    },
    "solosw": {
        "1": "/-stat/solosw/17",
        "2": "/-stat/solosw/18",
        "3": "/-stat/solosw/19",
        "4": "/-stat/solosw/20",
        "5": "/-stat/solosw/21",
        "6": "/-stat/solosw/22",
        "7": "/-stat/solosw/23",
        "8": "/-stat/solosw/24",
        "9": "/-stat/solosw/25",
        "10": "/-stat/solosw/26",
        "11": "/-stat/solosw/27",
        "12": "/-stat/solosw/28",
        "13": "/-stat/solosw/29",
        "14": "/-stat/solosw/30",
        "15": "/-stat/solosw/31",
        "16": "/-stat/solosw/32",
        "17": "/-stat/solosw/49",
        "18": "/-stat/solosw/50",
        "19": "/-stat/solosw/51",
        "20": "/-stat/solosw/52",
        "21": "/-stat/solosw/53",
        "22": "/-stat/solosw/54",
        "23": "/-stat/solosw/55",
        "24": "/-stat/solosw/56"
    },
    "pan": {
        "1": "/ch/17/mix/pan",
        "2": "/ch/18/mix/pan",
        "3": "/ch/19/mix/pan",
        "4": "/ch/20/mix/pan",
        "5": "/ch/21/mix/pan",
        "6": "/ch/22/mix/pan",
        "7": "/ch/23/mix/pan",
        "8": "/ch/24/mix/pan",
        "9": "/ch/25/mix/pan",
        "10": "/ch/26/mix/pan",
        "11": "/ch/27/mix/pan",
        "12": "/ch/28/mix/pan",
        "13": "/ch/29/mix/pan",
        "14": "/ch/30/mix/pan",
        "15": "/ch/31/mix/pan",
        "16": "/ch/32/mix/pan",
        "17": "/bus/01/mix/pan",
        "18": "/bus/02/mix/pan",
        "19": "/bus/03/mix/pan",
        "20": "/bus/04/mix/pan",
        "21": "/bus/05/mix/pan",
        "22": "/bus/06/mix/pan",
        "23": "/bus/07/mix/pan",
        "24": "/bus/08/mix/pan"
    },
    "name": {
        "1": "/ch/17/config/name",
        "2": "/ch/18/config/name",
        "3": "/ch/19/config/name",
        "4": "/ch/20/config/name",
        "5": "/ch/21/config/name",
        "6": "/ch/22/config/name",
        "7": "/ch/23/config/name",
        "8": "/ch/24/config/name",
        "9": "/ch/25/config/name",
        "10": "/ch/26/config/name",
        "11": "/ch/27/config/name",
        "12": "/ch/28/config/name",
        "13": "/ch/29/config/name",
        "14": "/ch/30/config/name",
        "15": "/ch/31/config/name",
        "16": "/ch/32/config/name",
        "17": "/bus/01/config/name",
        "18": "/bus/02/config/name",
        "19": "/bus/03/config/name",
        "20": "/bus/04/config/name",
        "21": "/bus/05/config/name",
        "22": "/bus/06/config/name",
        "23": "/bus/07/config/name",
        "24": "/bus/08/config/name"
    },
    "icon": {
        "1": "/ch/17/config/icon",
        "2": "/ch/18/config/icon",
        "3": "/ch/19/config/icon",
        "4": "/ch/20/config/icon",
        "5": "/ch/21/config/icon",
        "6": "/ch/22/config/icon",
        "7": "/ch/23/config/icon",
        "8": "/ch/24/config/icon",
        "9": "/ch/25/config/icon",
        "10": "/ch/26/config/icon",
        "11": "/ch/27/config/icon",
        "12": "/ch/28/config/icon",
        "13": "/ch/29/config/icon",
        "14": "/ch/30/config/icon",
        "15": "/ch/31/config/icon",
        "16": "/ch/32/config/icon",
        "17": "/bus/01/config/icon",
        "18": "/bus/02/config/icon",
        "19": "/bus/03/config/icon",
        "20": "/bus/04/config/icon",
        "21": "/bus/05/config/icon",
        "22": "/bus/06/config/icon",
        "23": "/bus/07/config/icon",
        "24": "/bus/08/config/icon"
    },
    "color": {
        "1": "/ch/17/config/color",
        "2": "/ch/18/config/color",
        "3": "/ch/19/config/color",
        "4": "/ch/20/config/color",
        "5": "/ch/21/config/color",
        "6": "/ch/22/config/color",
        "7": "/ch/23/config/color",
        "8": "/ch/24/config/color",
        "9": "/ch/25/config/color",
        "10": "/ch/26/config/color",
        "11": "/ch/27/config/color",
        "12": "/ch/28/config/color",
        "13": "/ch/29/config/color",
        "14": "/ch/30/config/color",
        "15": "/ch/31/config/color",
        "16": "/ch/32/config/color",
        "17": "/bus/01/config/color",
        "18": "/bus/02/config/color",
        "19": "/bus/03/config/color",
        "20": "/bus/04/config/color",
        "21": "/bus/05/config/color",
        "22": "/bus/06/config/color",
        "23": "/bus/07/config/color",
        "24": "/bus/08/config/color"
    },
    "selidx": {
        "0": "/-stat/selidx/16",
        "1": "/-stat/selidx/17",
        "2": "/-stat/selidx/18",
        "3": "/-stat/selidx/19",
        "4": "/-stat/selidx/20",
        "5": "/-stat/selidx/21",
        "6": "/-stat/selidx/22",
        "7": "/-stat/selidx/23",
        "8": "/-stat/selidx/24",
        "9": "/-stat/selidx/25",
        "10": "/-stat/selidx/26",
        "11": "/-stat/selidx/27",
        "12": "/-stat/selidx/28",
        "13": "/-stat/selidx/29",
        "14": "/-stat/selidx/30",
        "15": "/-stat/selidx/31",
        "16": "/-stat/selidx/48",
        "17": "/-stat/selidx/49",
        "18": "/-stat/selidx/50",
        "19": "/-stat/selidx/51",
        "20": "/-stat/selidx/52",
        "21": "/-stat/selidx/53",
        "22": "/-stat/selidx/54",
        "23": "/-stat/selidx/55"
    }, #0-31: Ch 1-32, 48-63: Bus master
    "midiBank": "/-stat/userbank", #0 -> A, 1-> B, 2->C
    "assign": "",
}

COLORS = {
    "#000000": "OFFi",
    "#ff0000": "RD",
    "#00ff00": "GN",
    "#ffff00": "YE",
    "#0000ff": "BL",
    "#ff00ff": "MG",
    "#63e5ff": "CY",
    "#ffffff": "WH"
}

ICONS = {
    "kick": "03",
    "snare": "05",
    "timpani": "08",
    "hi-hat": "09",
    "drums": "11"
}

channel_fbk1 = 10
channel_fbk2 = 11
channel_fbk3 = 12
channel_pbk1 = 13
channel_pbk2 = 14
channel_pbk3 = 15

cc_custom_min = 16
cc_custom_max = 31

channel_direct_map = 9

max_precision = 16383.0
fbk1_chans = {
    1: [16, 17],
    2: [18, 19],
    3: [20, 21],
    4: [22, 23],
    5: [24, 25],
    6: [26, 27],
    7: [28, 29],
    8: [30, 31]
}

fbk2_chans = {
    9: [16, 17],
    10: [18, 19],
    11: [20, 21],
    12: [22, 23],
    13: [24, 25],
    14: [26, 27],
    15: [28, 29],
    16: [30, 31]
}

fbk3_chans = {
    17: [16, 17],
    18: [18, 19],
    19: [20, 21],
    20: [22, 23],
    21: [24, 25],
    22: [26, 27],
    23: [28, 29],
    24: [30, 31]
}

pbk1_chans = {
    1: [16, 17],
    2: [18, 19],
    3: [20, 21],
    4: [22, 23],
    5: [24, 25],
    6: [26, 27],
    7: [28, 29],
    8: [30, 31]
}

pbk2_chans = {
    9: [16, 17],
    10: [18, 19],
    11: [20, 21],
    12: [22, 23],
    13: [24, 25],
    14: [26, 27],
    15: [28, 29],
    16: [30, 31]
}

pbk3_chans = {
    17: [16, 17],
    18: [18, 19],
    19: [20, 21],
    20: [22, 23],
    21: [24, 25],
    22: [26, 27],
    23: [28, 29],
    24: [30, 31]
}

channel_mute = 10
channel_solo = 11
channel_sel = 12

HW_CHANNELS = [ "C17", "C18", "C19", "C20", "C21", "C22", "C23", "C24",
               "C25", "C26", "C27", "C28", "C29", "C30", "C31", "C32",
               "B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "M00"]

REF_SCRIB_STRIP = "RSS"
REF_FADER = "RFD"
REF_MUTE = "RMT"
REF_SOLO = "RSL"
REF_PAN = "RPN"
REF_SELECT = "RST"
REF_EQ = "REQ"
REF_COMP = "RCM"
REF_REV = "RVB"
REF_COLORS = "RCL"
REF_ICONS = "RIC"

class MidasM32:
    def __init__(self, ip, flMidiIn, flMidiOut, midasMidiIn, midasMidiOut, midasMidiOn, inPort=PORT, outPort=PORT):
        try:
            self.midasMidiOn = midasMidiOn
            self.midiOutput = mido.open_output(flMidiIn)
            self.midiInput = mido.open_input(flMidiOut)

            if self.midasMidiOn:
                self.midasMidiOutput = mido.open_output(midasMidiIn) # MIDO open
                self.midasMidiInput = mido.open_input(midasMidiOut) # MIDO open
                midi_in_client = threading.Thread(target=self.__directInMidiHandler, daemon=True)
                midi_in_client.start()
            
            midi_out_client = threading.Thread(target=self.__directOutMidiHandler, daemon=True)
            midi_out_client.start()

            # Sender
            sender_parser = argparse.ArgumentParser()
            sender_parser.add_argument("--ip", default=ip)
            sender_parser.add_argument("--port", type=int, default=outPort)
            
            args = sender_parser.parse_args()
            
            source_port = 63993
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', source_port))

            self.client = udp_client.SimpleUDPClient(args.ip, args.port)
            self.client._sock = sock # Force to use the customly crafted socket

            client_subscription = threading.Thread(target=self.__periodicSubscription, daemon=True)
            client_subscription.start()

            # Receiver
            recv_parser = argparse.ArgumentParser()
            recv_parser.add_argument("--ip", default=ip)
            recv_parser.add_argument("--port", type=int, default=inPort) # Careful using the same port on loopback

            dispatcher = Dispatcher()
            dispatcher.map("/ch/*", self.__chHandler) # To check if it works with a non static method
            dispatcher.map("/bus/*", self.__chHandler)
            dispatcher.map("/-stat/*", self.__statHandler)

            args = recv_parser.parse_args()
            server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", source_port), dispatcher, bind_and_activate=False)
            server.socket = sock
            server.serve_forever()
        except Exception as exception:
            print(exception)
            print("Outputs:", mido.get_output_names())
            exit(2)

    @staticmethod
    def colorMapping(color):
        pass
    
    @staticmethod
    def iconMapping(name):
        pass
    
    @staticmethod
    def remap(value, old_min, old_max, new_min, new_max):
        return new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)
    
    @staticmethod
    def mapFaderToFL(midas_value):
        if midas_value < 0.0625: # FL Studio from 0.0 to 0.00331968516111374
            return MidasM32.remap(midas_value, 0.0, 0.6249999999999999, 0.0, 0.00331968516111373)
        elif midas_value >= 0.0625 and midas_value < 0.25: # FL studio to 0.0916703343391418
            return MidasM32.remap(midas_value, 0.0625, 0.2499999999999999, 0.00331968516111374, 0.0916703343391417)
        elif midas_value >= 0.25 and midas_value < 0.50:
            return MidasM32.remap(midas_value, 0.25, 0.4999999999999999, 0.0916703343391418, 0.4757713794708249)
        elif midas_value >= 0.50 and midas_value < 0.7525:
            return MidasM32.remap(midas_value, 0.50, 0.7524999999999999, 0.4757713794708250, 0.7999999999999999)
        elif midas_value >= 0.7525: # FOr 0 dB alignment
            return MidasM32.remap(midas_value, 0.7525, 1.0, 0.8, 1.0)
    
    @staticmethod
    def mapFaderToMidas(fl_value):
        if fl_value < 0.00331968516111373:
            return MidasM32.remap(fl_value, 0.0, 0.00331968516111373, 0.0, 0.625)
        elif fl_value >= 0.00331968516111373 and fl_value < 0.0916703343391417:
            return MidasM32.remap(fl_value, 0.00331968516111374, 0.0916703343391417, 0.0625, 0.25)
        elif fl_value >= 0.0916703343391417 and fl_value < 0.4757713794708249:
            return MidasM32.remap(fl_value, 0.0916703343391418, 0.4757713794708249, 0.25, 0.50)
        elif fl_value >= 0.4757713794708249 and fl_value < 0.7999999999999999:
            return MidasM32.remap(fl_value , 0.4757713794708250, 0.7999999999999999, 0.50, 0.7525)
        elif fl_value >= 0.7999999999999999: # F0r 0 dB alignment
            return MidasM32.remap(fl_value, 0.8, 1.0, 0.7525, 1.0)
    
    @staticmethod
    def mapPanpotToMidas(fl_value):
        if fl_value < 0.0:
            return MidasM32.remap(fl_value, -1.0, -0.000000000000001, 0.0, 0.5)
        elif fl_value >= 0.0:
            return MidasM32.remap(fl_value, 0.0, 1.0, 0.5, 1.0)
        
    def __periodicSubscription(self):
        while True:
            self.client.send_message("/xremote", None)
            time.sleep(9)
    
    def __chHandler(self, address, *args):
        fnc = address.split("/")[-1]

        for i in MAPPING[fnc].keys():
            if MAPPING[fnc][i] == address:
                # Discriminate between possibilities
                if fnc == "fader":
                    # Compute the channels on which to send
                    ctrl = None
                    chan = None
                    inti = int(i)
                    if inti <= 8:
                        chan = channel_fbk1
                        ctrl = fbk1_chans[inti]
                    elif inti >= 17:
                        chan = channel_fbk3
                        ctrl = fbk3_chans[inti]
                    else:
                        chan = channel_fbk2
                        ctrl = fbk2_chans[inti]

                    # Sending value
                    val = int(MidasM32.mapFaderToFL(args[0]) * max_precision)
                    msb = (val >> 7) & 0x7F
                    lsb = val & 0x7F
                    msg = mido.Message("control_change", channel=chan, control=ctrl[0], value=msb)
                    self.midiOutput.send(msg)
                    msg = mido.Message("control_change", channel=chan, control=ctrl[1], value=lsb)
                    self.midiOutput.send(msg)
                elif fnc == "on":
                    # To distinguish if it's on or off mute
                    if args[0] == 1:
                        msg = mido.Message("note_on", channel=channel_mute, note=int(i)+60)
                    elif args[0] == 0:
                        msg = mido.Message("note_off", channel=channel_mute, note=int(i)+60)
                    self.midiOutput.send(msg)
                elif fnc == "pan":
                    # Compute the channels on which to send
                    ctrl = None
                    chan = None
                    inti = int(i)
                    if inti <= 8:
                        chan = channel_pbk1
                        ctrl = pbk1_chans[inti]
                    elif inti >= 17:
                        chan = channel_pbk3
                        ctrl = pbk3_chans[inti]
                    else:
                        chan = channel_pbk2
                        ctrl = pbk2_chans[inti]

                    # Sending value
                    val = int(args[0] * max_precision)
                    msb = (val >> 7) & 0x7F
                    lsb = val & 0x7F
                    msg = mido.Message("control_change", channel=chan, control=ctrl[0], value=msb)
                    self.midiOutput.send(msg)
                    msg = mido.Message("control_change", channel=chan, control=ctrl[1], value=lsb)
                    self.midiOutput.send(msg)
                elif fnc == "name":
                    # No control from Midas to FL Studio, only sw -> hw
                    pass
                elif fnc == "icon":
                    # No control from Midas to FL Studio, only sw -> hw
                    pass
                elif fnc == "color":
                    # No control from Midas to FL Studio, only sw -> hw
                    pass
    
    def __statHandler(self, address, *args):
        fnc = address.split("/")[2]

        if fnc in MAPPING.keys():
            for i in MAPPING[fnc].keys():
                if fnc == "solosw" and MAPPING[fnc][i] == address:
                    # To distinguish if it's on or off solo
                    if args[0] == 0:
                        msg = mido.Message("note_on", channel=channel_solo, note=int(i)+60)
                    elif args[0] == 1:
                        msg = mido.Message("note_off", channel=channel_solo, note=int(i)+60)
                    self.midiOutput.send(msg)
                elif fnc == "selidx" and int(MAPPING[fnc][i].split("/")[-1]) == args[0]:
                    msg = mido.Message("note_on", channel=channel_sel, note=int(i)+61)
                    self.midiOutput.send(msg)
    
    def __directInMidiHandler(self):
        for msg in self.midasMidiInput:
            self.midiOutput.send(msg)
    
    # Receive data from FL studio and send it to Midas
    def __directOutMidiHandler(self):
        for msg in self.midiInput:
            if msg.type == "sysex":
                data = ("".join(chr(b) for b in msg.data[:]))

                # Common parsing for all the possible messages
                type = data[0:3]
                data = data[3:]
                channel_type = None
                channel_nr = None

                if data[0] == "C":
                    channel_type = "ch"
                elif data[0] == "B":
                    channel_type = "bus"
                elif data[0] == "M":
                    channel_type = "master"
                channel_nr = data[1:3]

                data = data[3:]

                #== SCRIBBLE STRIP Update ==
                if type == REF_SCRIB_STRIP:
                    self.client.send_message(f"/{channel_type}/{channel_nr}/config/name", data[0:11])
                
                #== FADER Update ==
                elif type == REF_FADER:
                    fader_volume = MidasM32.mapFaderToMidas(int(data) / max_precision)
                    self.client.send_message(f"/{channel_type}/{channel_nr}/mix/fader", fader_volume)

                #== SELECTED Update ==
                elif type == REF_SELECT:
                    channel_nr = int(channel_nr) - 1
                    if channel_type == "bus":
                        channel_nr = int(channel_nr) + 48
                    elif channel_type == "master":
                        channel_nr = 70
                    self.client.send_message(f"/-stat/selidx", channel_nr)
                
                #== MUTE Update ==
                elif type == REF_MUTE:
                    mute = int(data)
                    self.client.send_message(f"/{channel_type}/{channel_nr}/mix/on", int(not mute))
                
                #== SOLO Update ==
                elif type == REF_SOLO:
                    solo = int(data)
                    if channel_type == "bus":
                        channel_nr = int(channel_nr) + 48
                    self.client.send_message(f"/-stat/solosw/{channel_nr}", int(solo))
                
                #== PAN Update
                elif type == REF_PAN:
                    track_pan = MidasM32.mapPanpotToMidas(int(data) / max_precision)
                    self.client.send_message(f"/{channel_type}/{channel_nr}/mix/pan", track_pan)
                
                #== COLORS Update
                elif type == REF_COLORS:
                    self.client.send_message(f"/{channel_type}/{channel_nr}/config/color", data)

                #== ICONS Update
                elif type == REF_ICONS:
                    self.client.send_message(f"/{channel_type}/{channel_nr}/config/icon", data)
            
            elif msg.type == "control_change" and msg.channel == channel_direct_map and self.midasMidiOn:
                self.midasMidiOutput.send(msg)