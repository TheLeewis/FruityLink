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
import time
from FruityParametricEQ2Ctrl import FruityParametricEq2Ctrl
from FruityCompressorCtrl import FruityCompressorCtrl
from FruityReeverb2Ctrl import FruityReeverb2Ctrl

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

HW_CHANNELS = ["C17", "C18", "C19", "C20", "C21", "C22", "C23", "C24",
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

# === MAY BE CHANGED WITH DIFFERENT PLUGINS === #
EQ = FruityParametricEq2Ctrl
COMP = FruityCompressorCtrl
REV = FruityReeverb2Ctrl
# === MAY BE CHANGED WITH DIFFERENT PLUGINS === #

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
        self.lock_sync_only_from_hw = False
        self.last_hw_update = (time.perf_counter()*1000 - 1000)/1000

        self.eq_selected_bands = {}

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
                idx = MidasM32.__findInList(chans[i], eventData.controlNum)
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
    
    def __nextFaderPage(self):
        if mixer.trackCount() - 2 - (self.current_span+1)*24 > 0:
            self.current_span += 24

            self.refreshScribbleStrip()
            self.refreshFadersPositions()
            self.refreshSelectedChannel()
            self.refreshMute()
            self.refreshSolo()
            self.refreshPan()
            self.refreshAssignSection()
            self.refreshColor()

    def __prevFaderPage(self):
        if (self.current_span+1)*24 - 24 > 0:
            self.current_span -= 24

            self.refreshScribbleStrip()
            self.refreshFadersPositions()
            self.refreshSelectedChannel()
            self.refreshMute()
            self.refreshSolo()
            self.refreshPan()
            self.refreshAssignSection()
            self.refreshColor()

    def onMidiMsg(self, eventData):
        if not self.lock_sync_only_from_sw:
            self.lock_sync_only_from_hw = True
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

                    #== For equalizer: frequency, gain, quality factor (Q), slope
                    #== Channels CC 16, 17, 18, 19
                    #== Enable/Disable Band (A5) -> 20
                    #== Scroll between EQ shapes (A6) -> 21
                    #== Equalizer Band - (A7) -> 22
                    #== Equalizer Band + (A8) -> 23
                    if eventData.controlNum >= 16 and eventData.controlNum <= 23:
                        slotIndex = EQ.channelHasEQ(selected)
                        if slotIndex != None:
                            currentBand = EQ.getCurrentBand(self.eq_selected_bands, selected, slotIndex)

                            if eventData.controlNum == 16:
                                EQ.setFrequency(selected, slotIndex, eventData.controlVal, currentBand)
                            elif eventData.controlNum == 17:
                                EQ.setGain(selected, slotIndex, eventData.controlVal, currentBand)
                            elif eventData.controlNum == 18:
                                EQ.setQualityFactor(selected, slotIndex, eventData.controlVal, currentBand)
                            elif eventData.controlNum == 19:
                                EQ.setSlope(selected, slotIndex, eventData.controlVal, currentBand)

                    #== For compressor: Threshold, Ratio, Attack, Release (Main 4 knobs)
                    #== Other parameters of interest could be Knee, Makeup Gain (Wet Gain)
                    #== Channels CC 24, 25, 26, 27
                    if eventData.controlNum >= 24 and eventData.controlNum <= 27:
                        slotIndex = COMP.channelHasCompressor(selected)
                        if slotIndex != None:
                            if eventData.controlNum == 24:
                                COMP.setThreshold(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 25:
                                COMP.setRatio(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 26:
                                COMP.setAttack(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 27:
                                COMP.setRelease(selected, slotIndex, eventData.controlVal)
                    
                    #== For reverb: Brightness, Distance, Space, Decay Rate
                    #== Channels CC 28, 29, 30, 31
                    if eventData.controlNum >= 28 and eventData.controlNum <= 31:
                        slotIndex = REV.channelHasReverb(selected)
                        if slotIndex != None:
                            if eventData.controlNum == 28:
                                REV.setBrightness(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 29:
                                REV.setDistance(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 30:
                                REV.setSpace(selected, slotIndex, eventData.controlVal)
                            elif eventData.controlNum == 31:
                                REV.setDecayRate(selected, slotIndex, eventData.controlVal)    

            elif eventData.midiId == midi.MIDI_NOTEON:
                # Mute (Mapped linearly from note 61 to 85 of the channel 10)
                if eventData.midiChan == channel_mute and not self.fader_flip_active:
                    mixer.muteTrack(eventData.note - 60 + self.current_span, 0)
                elif eventData.midiChan == channel_solo and not self.fader_flip_active:
                    mixer.soloTrack(eventData.note - 60 + self.current_span, 0)
                elif eventData.midiChan == channel_sel and not self.fader_flip_active:
                    mixer.setActiveTrack(eventData.note - 60 + self.current_span)
                    self.refreshAssignSection()
                # Direct midi mappings from the assign panel
                elif eventData.midiChan == channel_direct_map:
                    selected = mixer.trackNumber()

                    #== Block A ==#
                    if eventData.note == 0 and not self.fader_flip_active:
                        # Toggle arm track for recording (A9)
                        mixer.armTrack(selected)
                    elif eventData.note == 1 and not self.fader_flip_active: # Record (A10)
                        transport.record()
                    elif eventData.note == 2: # Enable/Disable Band (A5 Toggle)
                        slotIndex = EQ.channelHasEQ(selected)
                        if slotIndex != None:
                            currentBand = EQ.getCurrentBand(self.eq_selected_bands, selected, slotIndex)
                            EQ.toggleBand(selected, slotIndex, currentBand)
                    elif eventData.note == 3 and eventData.velocity == 127: # Scroll between EQ shapes (A6)
                        slotIndex = EQ.channelHasEQ(selected)
                        if slotIndex != None:
                            currentBand = EQ.getCurrentBand(self.eq_selected_bands, selected, slotIndex)
                            EQ.scrollEqShapes(selected, slotIndex, currentBand)
                    elif eventData.note == 4 and eventData.velocity == 0: # Equalizer band - (A7)
                        slotIndex = EQ.channelHasEQ(selected)
                        if slotIndex != None:
                            currentBand = EQ.getCurrentBand(self.eq_selected_bands, selected, slotIndex)
                            prevBand = EQ.selectPrevBand(currentBand, selected, slotIndex)
                            self.eq_selected_bands[selected] = {}
                            self.eq_selected_bands[selected][slotIndex] = prevBand

                            self.refreshAssignSection()
                    elif eventData.note == 5 and eventData.velocity == 0: # Equalizer band + (A8)
                        slotIndex = EQ.channelHasEQ(selected)
                        if slotIndex != None:
                            currentBand = EQ.getCurrentBand(self.eq_selected_bands, selected, slotIndex)
                            nextBand = EQ.selectNextBand(currentBand, selected, slotIndex)
                            self.eq_selected_bands[selected] = {}
                            self.eq_selected_bands[selected][slotIndex] = nextBand
                            
                            self.refreshAssignSection()
                    elif eventData.note == 6 and eventData.velocity == 0: # Prev page of faders - (A11)
                        if not self.fader_flip_active:
                            self.__nextFaderPage()
                    elif eventData.note == 7 and eventData.velocity == 0: # Next page of faders + (A12)
                        if not self.fader_flip_active:
                            self.__prevFaderPage() 
                    #== Block B ==#
                    elif eventData.note == 8: # None (B5)
                        pass
                    elif eventData.note == 9 and not self.fader_flip_active: # Compressor Style (B6)
                        slotIndex = COMP.channelHasCompressor(selected)
                        COMP.switchCompressorStyle(selected, slotIndex)
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

            self.lock_sync_only_from_hw = False
            self.last_hw_update = time.perf_counter()
            return True # By default, the midi events are handled
    
    def refreshScribbleStrip(self):
        totalChannels = mixer.trackCount()

        hw_count = 0

        for i in range(self.current_span + 1, self.current_span + 25):
            if i <= totalChannels - 2:
                associated = HW_CHANNELS[hw_count]
                channel_name = REF_SCRIB_STRIP + associated + mixer.getTrackName(i)
            else:
                associated = HW_CHANNELS[hw_count]
                channel_name = REF_SCRIB_STRIP + associated + "None"

            header = [0xF0]
            body = [ord(c) for c in channel_name]
            footer = [0xF7]

            full_message = bytes(header + body + footer)
            device.midiOutSysex(full_message)
            hw_count+=1
    
    def refreshColor(self, reset=False):
        totalChannels = mixer.trackCount()
        hw_count = 0
        for i in range(self.current_span + 1, self.current_span + 25):
            if not reset and i <= totalChannels - 2:
                associated = HW_CHANNELS[hw_count]
                channel_color = REF_COLORS + associated + "BL"
            else:
                associated = HW_CHANNELS[hw_count]
                channel_color = REF_COLORS + associated + "OFFi"

            header = [0xF0]
            body = [ord(c) for c in channel_color]
            footer = [0xF7]

            full_message = bytes(header + body + footer)
            device.midiOutSysex(full_message)
            hw_count += 1

    def refreshIcons(self):
        hw_count = 0
        for i in range(self.current_span + 1, self.current_span + 25):
            associated = HW_CHANNELS[hw_count]
            channel_icon = REF_ICONS + associated + "62"

            header = [0xF0]
            body = [ord(c) for c in channel_icon]
            footer = [0xF7]

            full_message = bytes(header + body + footer)
            device.midiOutSysex(full_message)
            hw_count += 1
    
    def refreshFadersPositions(self, reset=False):
        totalChannels = mixer.trackCount()

        hw_count = 0

        for i in range(self.current_span + 1, self.current_span + 25):
            associated = HW_CHANNELS[hw_count]
            if not reset and i <= totalChannels - 2:
                volume = mixer.getTrackVolume(i)
                volume = int(volume * max_precision)

                text = REF_FADER + associated + str(volume)
            else:
                text = REF_FADER + associated + str(0)

            header = [0xF0]
            body = [ord(c) for c in text]
            footer = [0xF7]

            full_message = bytes(header + body + footer)
            device.midiOutSysex(full_message)
            hw_count+=1
    
    def refreshSelectedChannel(self):
        # Implementation can be made more efficient for sure, but for now it's sufficient
        totalChannels = mixer.trackCount()

        hw_count = 0

        selected = mixer.trackNumber()

        if selected < self.current_span + 1 or selected > self.current_span + 25:
            text = REF_SELECT + "M00"

            header = [0xF0]
            body = [ord(c) for c in text]
            footer = [0xF7]

            full_message = bytes(header + body + footer)
            device.midiOutSysex(full_message)

        for i in range(self.current_span + 1, self.current_span + 25):
            if i <= totalChannels - 2:
                associated = HW_CHANNELS[hw_count]

                if(i == selected):
                    text = REF_SELECT + associated

                    header = [0xF0]
                    body = [ord(c) for c in text]
                    footer = [0xF7]

                    full_message = bytes(header + body + footer)
                    device.midiOutSysex(full_message)
                    break
            else:
                break
            hw_count+=1

    def refreshMute(self, reset=False):
        totalChannels = mixer.trackCount()

        hw_count = 0

        for i in range(self.current_span + 1, self.current_span + 25):
            if i <= totalChannels - 2:
                associated = HW_CHANNELS[hw_count]

                if not reset:
                    mute = mixer.isTrackMuted(i)
                else:
                    mute = 0

                text = REF_MUTE + associated + str(mute)

                header = [0xF0]
                body = [ord(c) for c in text]
                footer = [0xF7]

                full_message = bytes(header + body + footer)
                device.midiOutSysex(full_message)
            else:
                break
            hw_count+=1

    def refreshSolo(self, reset=False):
        totalChannels = mixer.trackCount()

        hw_count = 0

        for i in range(self.current_span + 1, self.current_span + 25):
            associated = HW_CHANNELS[hw_count]
            if not reset and i <= totalChannels - 2:
                solo = mixer.isTrackSolo(i)
                text = REF_SOLO + associated + str(solo)
            else:
                text = REF_SOLO + associated + str(0)

            header = [0xF0]
            body = [ord(c) for c in text]
            footer = [0xF7]

            full_message = bytes(header + body + footer)
            device.midiOutSysex(full_message)
            hw_count+=1

    def refreshPan(self, reset=False):
        totalChannels = mixer.trackCount()

        hw_count = 0

        for i in range(self.current_span + 1, self.current_span + 25):
            associated = HW_CHANNELS[hw_count]
            if not reset and i <= totalChannels - 2:
                pan = mixer.getTrackPan(i)
                text = REF_PAN + associated + str(int(pan * max_precision))
            else:
                text = REF_PAN + associated + str(int(0 * max_precision))

            header = [0xF0]
            body = [ord(c) for c in text]
            footer = [0xF7]

            full_message = bytes(header + body + footer)
            device.midiOutSysex(full_message)
            hw_count+=1
    
    def refreshAssignSection(self, reset=False):
        selected = mixer.trackNumber()

        # Refresh the EQ section
        # TODO: state buttons
        slotIndex = EQ.channelHasEQ(selected)
        if not reset and slotIndex != None:
            currentBand = EQ.getCurrentBand(self.eq_selected_bands, selected, slotIndex)

            # Get Values
            frequency = EQ.getFrequency(selected, slotIndex, currentBand)
            gain = EQ.getGain(selected, slotIndex, currentBand)
            quality_factor = EQ.getQualityFactor(selected, slotIndex, currentBand)
            slope = EQ.getSlope(selected, slotIndex, currentBand)
        else:
            frequency = 0
            gain = 0
            quality_factor = 0
            slope = 0
        
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 16, int(frequency*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 17, int(gain*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 18, int(quality_factor*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 19, int(slope*127))

        # Refresh the Comp section
        slotIndex = COMP.channelHasCompressor(selected)
        if not reset and slotIndex != None:
            # Get Values
            threshold = COMP.getThreshold(selected, slotIndex)
            ratio = COMP.getRatio(selected, slotIndex)
            attack = COMP.getAttack(selected, slotIndex)
            release = COMP.getRelease(selected, slotIndex)
        else:
            threshold = 0
            ratio = 0
            attack = 0
            release = 0
        
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 24, int(threshold*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 25, int(ratio*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 26, int(attack*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 27, int(release*127))

        # Refresh the Reverb section
        slotIndex = REV.channelHasReverb(selected)
        if not reset and slotIndex != None:
            # Get Values
            brightness = REV.getBrightness(selected, slotIndex)
            distance = REV.getDistance(selected, slotIndex)
            space = REV.getSpace(selected, slotIndex)
            decayRate = REV.getDecayRate(selected, slotIndex)
        else:
            brightness = 0
            distance = 0
            space = 0
            decayRate = 0
        
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 28, int(brightness*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 29, int(distance*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 30, int(space*127))
        device.midiOutMsg(midi.MIDI_CONTROLCHANGE, channel_direct_map, 31, int(decayRate*127))
    
    def refreshAll(self):
        if not self.lock_sync_only_from_hw and time.perf_counter()* 1000 - self.last_hw_update* 1000 > 100:
            self.lock_sync_only_from_sw = True

            self.refreshScribbleStrip()
            self.refreshFadersPositions()
            self.refreshSelectedChannel()
            self.refreshMute()
            self.refreshSolo()
            self.refreshPan()
            self.refreshAssignSection()
            self.refreshColor()
            
            self.lock_sync_only_from_sw = False
    
    def refreshAllInit(self):
        self.lock_sync_only_from_sw = True

        self.refreshScribbleStrip()
        self.refreshFadersPositions()
        self.refreshSelectedChannel()
        self.refreshMute()
        self.refreshSolo()
        self.refreshPan()
        self.refreshAssignSection()
        self.refreshColor()
        self.refreshIcons()
        
        self.lock_sync_only_from_sw = False
    
    def setDefaultfaderPage(self):
        self.current_span = 0
    
    def setUnloadedState(self):
        self.lock_sync_only_from_sw = True

        self.refreshFadersPositions(reset=True)
        self.refreshSelectedChannel()
        self.refreshMute(reset=True)
        self.refreshSolo(reset=True)
        self.refreshPan(reset=True)
        self.refreshAssignSection(reset=True)
        
        self.lock_sync_only_from_sw = False

midas = MidasM32()

def OnMidiMsg(event):
    handled = midas.onMidiMsg(event)
    event.handled = handled # Only some messages are actually handled by the Script
    return True

def OnInit():
    midas.setDefaultfaderPage()
    midas.refreshAllInit()

def OnRefresh(flags):
    midas.setDefaultfaderPage()
    midas.refreshAll()

def onDeInit():
    midas.setUnloadedState()