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
import ui
from FabFilterProC2Ctrl import FabFilterProC2Ctrl
from FabFilterProRCtrl import FabFilterProRCtrl

# TODO: replace python constants with canonical capital names

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
        self.fader_flip_span = 0 # Span of channels in the fader flip view for channel link to busses/sends
        self.fader_flip_active = False
        self.fader_flip_bus = None # Number of the bus on which apply the fader flip

        self.lock_sync_only_from_sw = False

    @staticmethod
    def __findInList(list, element):
        try:
            idx = list.index(element)
            return idx
        except ValueError:
            return None

    def __faderControl(self, chan_keys, chans, eventData):
        #=== Fader ctrl ===#
        # Computation to have the double precision (14 bits)
        for i in chan_keys: # Not so efficient
            idx = MidasM32.__findInList(chans[i], eventData.controlNum)
            if idx != None:
                if idx == 0:
                    self.faders_vals[i]["MSB"] = eventData.controlVal
                elif idx == 1:
                    self.faders_vals[i]["LSB"] = eventData.controlVal
                break
        
        # If the information is complete, make the change
        if self.faders_vals[i]["MSB"] is not None and self.faders_vals[i]["LSB"] is not None:
            combined = (self.faders_vals[i]["MSB"] << 7) | self.faders_vals[i]["LSB"]
            normalized = combined / max_precision

            if not self.fader_flip_active: # Apply default
                mixer.setTrackVolume(i + self.current_span, normalized)
            else:
                mixer.setRouteToLevel(self.fader_flip_bus, i + self.current_span, normalized)

            # Clean old values
            self.faders_vals[i]["MSB"] = None
            self.faders_vals[i]["LSB"] = None
    
    def __panpotControl(self, chan_keys, chans, eventData):
        #=== Pan potentiometers ctrl ===#

        if not self.fader_flip_active:
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

    @staticmethod
    def __getFocusedPlugin(self):
        form_id = ui.getFocusedFormID()

        if form_id == -1:
            return None
        
        #== CASE 1: Channel rack plugin (instrument)
        if 0 <= form_id < 99999:
            return {
                "type": "instrument",
                "index": form_id
            }

        #== CASE 2: Mixer plugin (effect)
        track = form_id // 4194304
        slot = (form_id // 65536) % 64

        if 0 <= mixer.trackCount() and 0 <= slot < 64:
            return {
                "type": "effect",
                "track": track,
                "slot": slot
            }
        
        #== CASE 3: Not a plugin window
        return {
            "type": "generic",
            "index": form_id
        }

    def onMidiMsg(self, eventData):
        if not self.lock_sync_only_from_sw:
            if eventData.midiId == midi.MIDI_CONTROLCHANGE and eventData.controlNum <= cc_custom_max and eventData.controlNum >= cc_custom_min:
                # Faders
                if eventData.midiChan == channel_fbk1:
                    self.__faderControl(self.fbk1_chans_keys, fbk1_chans, eventData)
                elif eventData.midiChan == channel_fbk2:
                    self.__faderControl(self.fbk2_chans_keys, fbk2_chans, eventData)
                elif eventData.midiChan == channel_fbk3:
                    self.__faderControl(self.fbk3_chans_keys, fbk3_chans, eventData)
                # Panpots
                elif eventData.midiChan == channel_pbk1:
                    self.__panpotControl(self.pbk1_chans_keys, pbk1_chans, eventData)
                elif eventData.midiChan == channel_pbk2:
                    self.__panpotControl(self.pbk2_chans_keys, pbk2_chans, eventData)
                elif eventData.midiChan == channel_pbk3:
                    self.__panpotControl(self.pbk3_chans_keys, pbk3_chans, eventData)
                elif eventData.midiChan == channel_direct_map:
                    selected = mixer.trackNumber()
                    #== For equalizer: frequency, gain, quality factor (Q), dynamic range (directly mapped using MIDI learn)
                    #== Channels CC 16, 17, 18, 19
                    #== Enable/Disable Band (A5) -> 20
                    #== Scroll between EQ shapes (A6) -> 21
                    #== Equalizer Band - (A7) -> 22
                    #== Equalizer Band + (A8) -> 23
                    if eventData.controlNum >= 16 and eventData.controlNum <= 23:
                        return False # Directly elaborated by the plugin

                    #== For compressor: Threshold, Ratio, Attack, Release (Main 4 knobs)
                    #== Other parameters of interest could be Knee, Makeup Gain (Wet Gain)
                    #== Channels CC 24, 25, 26, 27
                    if eventData.controlNum >= 24 and eventData.controlNum <= 27:
                        slotIndex = FabFilterProC2Ctrl.channelHasProC2(selected)
                        if slotIndex != None:
                            if eventData.controlNum == 24:
                                FabFilterProC2Ctrl.setThreshold(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 25:
                                FabFilterProC2Ctrl.setRatio(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 26:
                                FabFilterProC2Ctrl.setAttack(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 27:
                                FabFilterProC2Ctrl.setRelease(selected, slotIndex, eventData.controlVal)
                    
                    #== For reverb: Brightness, Distance, Space, Decay Rate
                    #== Channels CC 28, 29, 30, 31
                    if eventData.controlNum >= 28 and eventData.controlNum <= 31:
                        slotIndex = FabFilterProRCtrl.channelHasProR(selected)
                        if slotIndex != None:
                            if eventData.controlNum == 28:
                                FabFilterProRCtrl.setBrightness(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 29:
                                FabFilterProRCtrl.setDistance(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 30:
                                FabFilterProRCtrl.setSpace(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 31:
                                FabFilterProRCtrl.setDecayRate(selected, slotIndex, eventData.controlVal)    

            elif eventData.midiId == midi.MIDI_NOTEON:
                # Mute (Mapped linearly from note 61 to 85 of the channel 10)
                if eventData.midiChan == channel_mute and not self.fader_flip_active:
                    mixer.muteTrack(eventData.note - 60 + self.current_span, 0)
                elif eventData.midiChan == channel_solo and not self.fader_flip_active:
                    mixer.soloTrack(eventData.note - 60 + self.current_span, 0)
                    #Need some refresh here
                elif eventData.midiChan == channel_sel and not self.fader_flip_active:
                    mixer.setActiveTrack(eventData.note - 60 + self.current_span)
                # Direct midi mappings from the assign panel
                elif eventData.midiChan == channel_direct_map:
                    selected = mixer.trackNumber()

                    #== Block A ==#
                    if eventData.note == 0 and not self.fader_flip_active:
                        # Toggle arm track for recording (A9)
                        mixer.armTrack(selected)
                    elif eventData.note == 1 and not self.fader_flip_active: # Record (A10)
                        transport.record()
                    #== Already managed in the control block
                    #elif eventData.note == 2: # Enable/Disable Band (A5)
                        #pass #== Directly mapped using Pro Q MIDI Learn (for graphic alignment with selected band interface)
                    #elif eventData.note == 3: # Scroll between EQ shapes (A6)
                        #pass #== Directly mapped using Pro Q MIDI Learn
                    #elif eventData.note == 4: # Equalizer band - (A7)
                        #pass #== Directly mapped using Pro Q MIDI Learn
                    #elif eventData.note == 5: # Equalizer band + (A8)
                        #pass #== Directly mapped using Pro Q MIDI Learn'''
                    elif eventData.note == 6: # Prev page of faders - (A11)
                        if not self.fader_flip_active and self.current_span > 0:
                            self.current_span = self.current_span - 24
                        elif self.fader_flip_span > 0:
                            self.fader_flip_span = self.fader_flip_span - 24
                    elif eventData.note == 7: # Next page of faders + (A12)
                        if not self.fader_flip_active and mixer.trackCount > self.current_span:
                            self.current_span = self.current_span + 24
                        elif mixer.trackCount > self.fader_flip_span:
                            self.fader_flip_span = self.fader_flip_span + 24
                    #== Block B ==#
                    elif eventData.note == 8: # None (B5)
                        pass
                    elif eventData.note == 9 and not self.fader_flip_active: # Compressor Style (B6)
                        slotIndex = FabFilterProC2Ctrl.channelHasProC2(selected)
                        FabFilterProC2Ctrl.switchCompressorStyle(selected, slotIndex)
                    elif eventData.note == 10: # Current plugin preset - (B7)
                        currentWin = self.__getFocusedPlugin()
                        if currentWin["type"] == "instrument":
                            plugins.prevPreset(currentWin["index"])
                        elif currentWin["type"] == "effect":
                            plugins.prevPreset(currentWin["track"], currentWin["slot"])
                    elif eventData.note == 11: # Current plugin preset + (B8) 
                        currentWin = self.__getFocusedPlugin()
                        if currentWin["type"] == "instrument":
                            plugins.nextPreset(currentWin["index"])
                        elif currentWin["type"] == "effect":
                            plugins.nextPreset(currentWin["track"], currentWin["slot"])
                        pass
                    elif eventData.note == 12: # Virtual fader flip (B10)
                        self.fader_flip_active = not self.fader_flip_active
                        if self.fader_flip_active:
                            self.fader_flip_bus = selected
                            # TODO: refresh scribble strip and faders
                        else:
                            self.fader_flip_span = 0
                            self.fader_flip_bus = None
                    elif eventData.note == 13 and self.fader_flip_active: # Send channel to bus (VFF Mode)
                        mixer.setRouteTo(self.fader_flip_bus, selected, 1, True)
                        mixer.setRouteToLevel(self.fader_flip_bus, selected, 0.75) # Set send level to 0 dB by default
                        mixer.afterRoutingChanged() # Notify FL studio about the change
                        ## TODO: refresh
                    elif eventData.note == 14 and self.fader_flip_active: # Unsend channel to bus (VFF Mode)
                        mixer.setRouteTo(self.fader_flip_bus, selected, 0, True)
                        mixer.afterRoutingChanged()
                    # B11 and B12 mapped like A11 and A12 so to have prev and next page for faders available directly after fader flip #
                    #== Block C ==#
                    # None
                
            elif eventData.midiId == midi.MIDI_NOTEOFF:
                if eventData.midiChan == channel_mute and not self.fader_flip_active:
                    mixer.muteTrack(eventData.note - 60 + self.current_span, 1)
                elif eventData.midiChan == channel_solo and not self.fader_flip_active:
                    mixer.soloTrack(eventData.note - 60 + self.current_span, 1)
                    #Need some refresh here

            return True # By default, the midi events are handled
    
    def refreshScribbleStrip(self):
        pass
    
midas = MidasM32()

def OnMidiMsg(event):
    handled = midas.onMidiMsg(event)
    event.handled = handled # Only some messages are actually handled by the Script
    return True

def onInit():
    midas.refreshScribbleStrip()