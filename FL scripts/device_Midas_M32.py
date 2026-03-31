# name=Midas M32
# version=2026.1

''' references
Midas M32: http://behringer.world/wiki/doku.php?id=x32_midi_table
Image Line: https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm
'''

# imports
import mixer
import device
import midi
import transport
import plugins
from FabFilterProQ3Ctrl import FabFilterProQ3Ctrl

max_precision = 16383.0
span_block_size = 24

channel_fbk1 = 10
channel_fbk2 = 11
channel_fbk3 = 12
channel_pbk1 = 13
channel_pbk2 = 14
channel_pbk3 = 15

channel_mute = 10
channel_solo = 11
channel_sel = 12

channel_direct_map = 9

cc_custom_min = 16
cc_custom_max = 31
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

# All in double precision
class MidasM32:
    def __init__(self):
        self.faders_vals = {
             1: {"MSB": None, "LSB": None},
             2: {"MSB": None, "LSB": None},
             3: {"MSB": None, "LSB": None},
             4: {"MSB": None, "LSB": None},
             5: {"MSB": None, "LSB": None},
             6: {"MSB": None, "LSB": None},
             7: {"MSB": None, "LSB": None},
             8: {"MSB": None, "LSB": None},
             9: {"MSB": None, "LSB": None},
             10: {"MSB": None, "LSB": None},
             11: {"MSB": None, "LSB": None},
             12: {"MSB": None, "LSB": None},
             13: {"MSB": None, "LSB": None},
             14: {"MSB": None, "LSB": None},
             15: {"MSB": None, "LSB": None},
             16: {"MSB": None, "LSB": None},
             17: {"MSB": None, "LSB": None},
             18: {"MSB": None, "LSB": None},
             19: {"MSB": None, "LSB": None},
             20: {"MSB": None, "LSB": None},
             21: {"MSB": None, "LSB": None},
             22: {"MSB": None, "LSB": None},
             23: {"MSB": None, "LSB": None},
             24: {"MSB": None, "LSB": None}
        }

        self.panpot_vals = {
             1: {"MSB": None, "LSB": None},
             2: {"MSB": None, "LSB": None},
             3: {"MSB": None, "LSB": None},
             4: {"MSB": None, "LSB": None},
             5: {"MSB": None, "LSB": None},
             6: {"MSB": None, "LSB": None},
             7: {"MSB": None, "LSB": None},
             8: {"MSB": None, "LSB": None},
             9: {"MSB": None, "LSB": None},
             10: {"MSB": None, "LSB": None},
             11: {"MSB": None, "LSB": None},
             12: {"MSB": None, "LSB": None},
             13: {"MSB": None, "LSB": None},
             14: {"MSB": None, "LSB": None},
             15: {"MSB": None, "LSB": None},
             16: {"MSB": None, "LSB": None},
             17: {"MSB": None, "LSB": None},
             18: {"MSB": None, "LSB": None},
             19: {"MSB": None, "LSB": None},
             20: {"MSB": None, "LSB": None},
             21: {"MSB": None, "LSB": None},
             22: {"MSB": None, "LSB": None},
             23: {"MSB": None, "LSB": None},
             24: {"MSB": None, "LSB": None}
        }

        self.fbk1_chans_keys = list(fbk1_chans.keys())
        self.fbk2_chans_keys = list(fbk2_chans.keys())
        self.fbk3_chans_keys = list(fbk3_chans.keys())
        self.pbk1_chans_keys = list(pbk1_chans.keys())
        self.pbk2_chans_keys = list(pbk2_chans.keys())
        self.pbk3_chans_keys = list(pbk3_chans.keys())

        self.current_span = 0 # To add to get the page of channels in which the hardware is

        self.lock_sync_only_from_sw = False

    @staticmethod
    def findInList(list, element):
        try:
            idx = list.index(element)
            return idx
        except ValueError:
            return None
    
    @staticmethod
    def channelHasProC2(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == "FabFilter Pro-C 2":
                return slotIndex
    
    @staticmethod
    def channelHasProR(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == "FabFilter Pro-R":
                return slotIndex

    def faderControl(self, chan_keys, chans, eventData):
        #=== Fader ctrl ===#
        # Computation to have the double precision (14 bits)
        for i in chan_keys: # Not so efficient
            idx = MidasM32.findInList(chans[i], eventData.controlNum)
            if idx != None:
                if idx == 0:
                    self.faders_vals[i]["MSB"] = eventData.controlVal
                elif idx == 1:
                    self.faders_vals[i]["LSB"] = eventData.controlVal
                break
        print(self.faders_vals[i]["MSB"], self.faders_vals[i]["LSB"])
        
        # If the information is complete, make the change
        if self.faders_vals[i]["MSB"] is not None and self.faders_vals[i]["LSB"] is not None:
            combined = (self.faders_vals[i]["MSB"] << 7) | self.faders_vals[i]["LSB"]
            normalized = combined / max_precision
            mixer.setTrackVolume(i + self.current_span, normalized)

            # Clean old values
            self.faders_vals[i]["MSB"] = None
            self.faders_vals[i]["LSB"] = None
    
    def panpotControl(self, chan_keys, chans, eventData):
        #=== Pan potentiometers ctrl ===#
        # Computation to have the double precision (14 bits)
        for i in chan_keys: # Not so efficient
            idx = MidasM32.findInList(chans[i], eventData.controlNum)
            if idx != None:
                if idx == 0:
                    self.panpot_vals[i]["MSB"] = eventData.controlVal
                elif idx == 1:
                    self.panpot_vals[i]["LSB"] = eventData.controlVal
                break
        
        # If the information is complete, make the change
        if self.panpot_vals[i]["MSB"] is not None and self.panpot_vals[i]["LSB"] is not None:
            combined = (self.panpot_vals[i]["MSB"] << 7) | self.panpot_vals[i]["LSB"]
            normalized = (combined * 2 / max_precision) - 1
            mixer.setTrackPan(i + self.current_span, normalized)

            # Clean old values
            self.panpot_vals[i]["MSB"] = None
            self.panpot_vals[i]["LSB"] = None

    def onMidiMsg(self, eventData):
        if not self.lock_sync_only_from_sw:
            if eventData.midiId == midi.MIDI_CONTROLCHANGE and eventData.controlNum <= cc_custom_max and eventData.controlNum >= cc_custom_min:
                # Faders
                if eventData.midiChan == channel_fbk1:
                    self.faderControl(self.fbk1_chans_keys, fbk1_chans, eventData)
                elif eventData.midiChan == channel_fbk2:
                    self.faderControl(self.fbk2_chans_keys, fbk2_chans, eventData)
                elif eventData.midiChan == channel_fbk3:
                    self.faderControl(self.fbk3_chans_keys, fbk3_chans, eventData)
                # Panpots
                elif eventData.midiChan == channel_pbk1:
                    self.panpotControl(self.pbk1_chans_keys, pbk1_chans, eventData)
                elif eventData.midiChan == channel_pbk2:
                    self.panpotControl(self.pbk2_chans_keys, pbk2_chans, eventData)
                elif eventData.midiChan == channel_pbk3:
                    self.panpotControl(self.pbk3_chans_keys, pbk3_chans, eventData)
                elif eventData.midiChan == channel_direct_map: # Plugin mapping directly to equalizer, compressor, reverb
                    pass # Maps
                    # For equalizer: frequency, gain, quality factor (Q), dynamic range
                    # For compressor: Threshold, Ratio, Knee, Makup Gain
                    # For reverb: Brightness, Distance, Space, Dry/wet
            elif eventData.midiId == midi.MIDI_NOTEON:
                # Mute (Mapped linearly from note 61 to 85 of the channel 10)
                if eventData.midiChan == channel_mute:
                    mixer.muteTrack(eventData.note - 60 + self.current_span, 0)
                elif eventData.midiChan == channel_solo:
                    mixer.soloTrack(eventData.note - 60 + self.current_span, 0)
                    #Need some refresh here
                elif eventData.midiChan == channel_sel:
                    mixer.setActiveTrack(eventData.note - 60 + self.current_span)
                # Direct midi mappings from the assign panel
                elif eventData.midiChan == channel_direct_map:
                    selected = mixer.trackNumber()

                    #== Block A ==#
                    if eventData.note == 0:
                        # Toggle arm track for recording (A9)
                        mixer.armTrack(selected)
                    elif eventData.note == 1: # Record (A10)
                        transport.record()
                    elif eventData.note == 2: # Enable/Disable Band (A5)
                        pluginSlot = FabFilterProQ3Ctrl.channelHasProQ3(selected)
                        if pluginSlot:
                            FabFilterProQ3Ctrl.getProQ3FirstUsedBand(selected, pluginSlot)
                    elif eventData.note == 3: # Scroll between EQ shapes (A6)
                        pass
                    elif eventData.note == 4: # Equalizer band - (A7)
                        pass
                    elif eventData.note == 5: # Equalizer band + (A8)
                        pass
                    elif eventData.note == 6: # Prev page of faders - (A11)
                        pass
                    elif eventData.note == 7: # Next page of faders + (A12)
                        pass
                    #== Block B ==#
                    elif eventData.note == 8: # None (B5)
                        pass
                    elif eventData.note == 9: # Compressor Style (B6)
                        pass
                    elif eventData.note == 10: # Current plugin preset - (B7)
                        pass
                    elif eventData.note == 11: # Current plugin preset + (B8)
                        pass
                    elif eventData.note == 12: # Virtual fader flip (B10)
                        pass
                    # B11 and B12 mapped like A11 and A12 so to have prev and next page for faders available directly after fader flip #
                    #== Block C ==#
                    # None
                
            elif eventData.midiId == midi.MIDI_NOTEOFF:
                if eventData.midiChan == channel_mute:
                    mixer.muteTrack(eventData.note - 60 + self.current_span, 1)
                elif eventData.midiChan == channel_solo:
                    mixer.soloTrack(eventData.note - 60 + self.current_span, 1)
                    #Need some refresh here

midas = MidasM32()

def OnMidiMsg(event):
    midas.onMidiMsg(event)
    event.handled = True # No message is propagated, all are intercepted
    return True