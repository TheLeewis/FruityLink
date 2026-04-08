import customtkinter as ctk
from tkinter import ttk
from PIL import Image
import multiprocessing

from MidasM32 import MidasM32
from MidiManager import MidiManager
from Persistence import Persistence
from Utils import Utils

class GUI:
    def __init__(self):
        # Main app configuration
        self.app = ctk.CTk()
        self.app.geometry("600x600")
        self.app.title("FruityLink")
        self.app.iconbitmap(Utils.resourcePath("./src/FruityLink.ico"))
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.app.resizable(False, False)

        self.vcmd = (self.app.register(GUI.validateIpInput), '%P')

        self.entry1 = None
        self.entry2 = None
        self.entry3 = None
        self.entry4 = None
        self.log = None
        self.comboFlIn = None
        self.comboFlOut = None
        self.worker_process = None
        self.midi_in = None
        self.midi_out = None
        self.is_midi_on_midas_on = ctk.IntVar(value=1)

        self.createOSCFrame()
        self.createMIDIFrame()
        self.createSubmitFrame()
        self.setMemoryValues()

        self.app.mainloop()

    def createOSCFrame(self):
        osc_frame = ctk.CTkFrame(master=self.app, width=500, height=130)
        osc_frame.grid_propagate(False)
        osc_frame.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="nsew")

        osc_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        osc_frame.grid_rowconfigure((0, 1), weight=0)
        osc_frame.grid_rowconfigure(2, weight=1)

        label = ctk.CTkLabel(master=osc_frame, text="OSC Configuration", font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=0, padx=20, pady=10, sticky="nw", columnspan=4)

        label = ctk.CTkLabel(master=osc_frame, text="IP Address")
        label.grid(row=1, column=0, padx=20, sticky="nw")

        self.entry1 = ctk.CTkEntry(master=osc_frame, justify="center", validate="key", validatecommand=self.vcmd)
        self.entry1.grid(row=2, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")
        self.entry2 = ctk.CTkEntry(master=osc_frame, justify="center", validate="key", validatecommand=self.vcmd)
        self.entry2.grid(row=2, column=1, padx=10, pady=(10, 20), sticky="nsew")
        self.entry3 = ctk.CTkEntry(master=osc_frame, justify="center", validate="key", validatecommand=self.vcmd)
        self.entry3.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="nsew")
        self.entry4 = ctk.CTkEntry(master=osc_frame, justify="center", validate="key", validatecommand=self.vcmd)
        self.entry4.grid(row=2, column=3, padx=(10, 20), pady=(10, 20), sticky="nsew")
    
    def createMIDIFrame(self):
        midi_frame = ctk.CTkFrame(master=self.app, width=500, height=250)
        midi_frame.grid_propagate(False)
        midi_frame.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        midi_frame.grid_columnconfigure((0, 1), weight=1)
        midi_frame.grid_rowconfigure((0, 1, 2, 4), weight=0)
        midi_frame.grid_rowconfigure((3, 5), weight=1)

        # Get Options Data
        self.midi_in = MidiManager.getMidiInputs()
        self.midi_out = MidiManager.getMidiOutputs()

        label = ctk.CTkLabel(master=midi_frame, text="MIDI Configuration", font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=0, padx=20, pady=10, sticky="nw", columnspan=2)

        label = ctk.CTkLabel(master=midi_frame, text="FL In Interface")
        label.grid(row=2, column=0, padx=20, sticky="nw")

        label = ctk.CTkLabel(master=midi_frame, text="FL Out Interface")
        label.grid(row=2, column=1, padx=20, sticky="nw")

        self.comboFlIn = ctk.CTkComboBox(
            master=midi_frame,
            values=self.midi_out,
            command=None
        )
        self.comboFlIn.grid(padx=20, pady=0, row=3, column=0, sticky="ew")

        self.comboFlOut = ctk.CTkComboBox(
            master=midi_frame,
            values=self.midi_in,
            command=None
        )
        self.comboFlOut.grid(padx=20, pady=0, row=3, column=1, sticky="ew")

        # MIDAS use MIDI checkbox
        self.midasMIDICheckbox = ctk.CTkSwitch(
            master=midi_frame,
            text="Enable MIDI assign section on Midas",
            progress_color="#E85028",
            fg_color="grey50",
            button_hover_color="#FB9244",
            button_color="#fafafa",
            variable=self.is_midi_on_midas_on,
            onvalue=1,
            offvalue=0,
            state="enabled",
            command=self.midasMIDIEnableCallback
        )
        self.midasMIDICheckbox.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nw", columnspan=2)

        # Second row for MIDAS ports configuration
        label = ctk.CTkLabel(master=midi_frame, text="MIDAS In Interface")
        label.grid(row=4, column=0, padx=20, sticky="nw")

        label = ctk.CTkLabel(master=midi_frame, text="MIDAS Out Interface")
        label.grid(row=4, column=1, padx=20, sticky="nw")

        self.comboMidasIn = ctk.CTkComboBox(
            master=midi_frame,
            values=self.midi_out,
            command=None,
        )
        self.comboMidasIn.grid(padx=20, pady=(0, 10), row=5, column=0, sticky="ew")

        self.comboMidasOut = ctk.CTkComboBox(
            master=midi_frame,
            values=self.midi_in,
            command=None
        )
        self.comboMidasOut.grid(padx=20, pady=(0, 10), row=5, column=1, sticky="ew")

    def createSubmitFrame(self):
        submit_frame = ctk.CTkFrame(master=self.app, width=500, height=100)
        submit_frame.grid_propagate(False)
        submit_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")

        submit_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")
        submit_frame.grid_rowconfigure((0, 1), weight=0)

        img = Image.open(Utils.resourcePath("./src/wrench-adjustable-circle.png"))  # or your image path
        icon = ctk.CTkImage(img, size=(18, 18))

        img = Image.open(Utils.resourcePath("./src/x-circle.png"))
        icon2 = ctk.CTkImage(img, size=(18, 18))

        self.log = ctk.CTkLabel(submit_frame, text="", text_color="#E85028")
        self.log.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nw", columnspan=2)

        button = ctk.CTkButton(master=submit_frame, text="Set", width=30, height=30, image=icon, compound="left", text_color="black", fg_color="#E85028", hover_color="#FB9244", cursor="hand2", command=self.submitCallback)
        button.grid(row=1, column=0, padx=(20, 10), pady=(10, 20), sticky="ew")
        button = ctk.CTkButton(master=submit_frame, text="Unset", width=30, height=30, image=icon2, compound="left", text_color="white", fg_color="#515151", hover_color="#8E8E8E", cursor="hand2", command=self.stopCallback)
        button.grid(row=1, column=1, padx=(10, 20), pady=(10, 20), sticky="ew")

    def setMemoryValues(self):
        vals = Persistence.getSettings()
        
        if vals != None:
            if vals["ipc1"] and self.validateIpInput(vals["ipc1"]): self.entry1.insert(0, vals["ipc1"])
            if vals["ipc2"] and self.validateIpInput(vals["ipc2"]): self.entry2.insert(0, vals["ipc2"])
            if vals["ipc3"] and self.validateIpInput(vals["ipc3"]): self.entry3.insert(0, vals["ipc3"])
            if vals["ipc4"] and self.validateIpInput(vals["ipc4"]): self.entry4.insert(0, vals["ipc4"])

            if vals["flIn"] in self.midi_out: self.comboFlIn.set(vals["flIn"])
            if vals["flOut"] in self.midi_out: self.comboFlOut.set(vals["flOut"])
            if vals["midasIn"] in self.midi_out: self.comboMidasIn.set(vals["midasIn"])
            if vals["midasOut"] in self.midi_out: self.comboMidasOut.set(vals["midasOut"])
    
    def saveMemoryValues(self):
        Persistence.saveSettings(
            self.entry1.get(),
            self.entry2.get(),
            self.entry3.get(),
            self.entry4.get(),
            self.comboFlIn.get(),
            self.comboFlOut.get(),
            self.comboMidasIn.get(),
            self.comboMidasOut.get()
        )
    
    @staticmethod
    def validateIpInput(P):
        if P == "" or (P.isdigit() and int(P) >= 0 and int(P) <=255):
            return True
        return False
    
    def midasMIDIEnableCallback(self):
        value = self.midasMIDICheckbox.get()

        if value:
            self.comboMidasIn.configure(state="normal")
            self.comboMidasOut.configure(state="normal")
        else:
            self.comboMidasIn.configure(state="disabled")
            self.comboMidasOut.configure(state="disabled")

    def submitCallback(self):
        ip = ""
        inputs = [self.entry1, self.entry2, self.entry3, self.entry4]

        for i in inputs:
            raw = i.get()
            if raw.isdigit():
                number = int(raw)
                if number >= 0 and number <= 255:
                    ip += str(number)
                else:
                    self.log.configure(text=" Not a valid IP address.")
                    return

                if i != self.entry4:
                    ip += "."
            else:
                self.log.configure(text=" Not a valid IP address.")
                return
        self.log.configure(text="")

        # Reachable check
        '''response = pyping.ping(ip)
        if response.ret_code != 0:
            self.log.configure(text="Mixer not reachable.")
            return'''
        
        flMidiIn = self.comboFlIn.get()
        flMidiOut = self.comboFlOut.get()

        midasMidiOn = self.midasMIDICheckbox.get()
        midasMidiIn = self.comboMidasIn.get()
        midasMidiOut = self.comboMidasOut.get()

        self.worker_process = multiprocessing.Process(target=MidasM32, daemon=True, args=(ip, flMidiIn, flMidiOut, midasMidiIn, midasMidiOut, midasMidiOn))
        self.worker_process.start()

        self.saveMemoryValues()

        self.log.configure(text="Running")
    
    def stopCallback(self):
        self.worker_process.terminate()
        self.log.configure(text="Not running")