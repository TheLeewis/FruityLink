import customtkinter as ctk
from tkinter import ttk
from PIL import Image

class GUI:
    def __init__(self):
        # Main app configuration
        self.app = ctk.CTk()
        self.app.geometry("600x550")
        self.app.title("FruityLink")
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure((0, 1, 2), weight=1)
        self.app.resizable(False, False)

        self.createOSCFrame()
        self.createMIDIFrame()
        self.createSubmitFrame()

        self.app.mainloop()
    
    def createOSCFrame(self):
        osc_frame = ctk.CTkFrame(master=self.app, width=500, height=130)
        osc_frame.grid_propagate(False)
        osc_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        osc_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        osc_frame.grid_rowconfigure((0, 1), weight=0)
        osc_frame.grid_rowconfigure(2, weight=1)

        label = ctk.CTkLabel(master=osc_frame, text="OSC Configuration", font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=0, padx=20, pady=10, sticky="nw", columnspan=4)

        label = ctk.CTkLabel(master=osc_frame, text="IP Address")
        label.grid(row=1, column=0, padx=20, sticky="nw")

        entry1 = ctk.CTkEntry(master=osc_frame, justify="center")
        entry1.grid(row=2, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")
        entry2 = ctk.CTkEntry(master=osc_frame, justify="center")
        entry2.grid(row=2, column=1, padx=10, pady=(10, 20), sticky="nsew")
        entry3 = ctk.CTkEntry(master=osc_frame, justify="center")
        entry3.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="nsew")
        entry4 = ctk.CTkEntry(master=osc_frame, justify="center")
        entry4.grid(row=2, column=3, padx=(10, 20), pady=(10, 20), sticky="nsew")
    
    def createMIDIFrame(self):
        midi_frame = ctk.CTkFrame(master=self.app, width=500, height=200)
        midi_frame.grid_propagate(False)
        midi_frame.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")

        midi_frame.grid_columnconfigure((0, 1), weight=1)
        midi_frame.grid_rowconfigure((0, 1, 3), weight=0)
        midi_frame.grid_rowconfigure((2, 4), weight=1)

        label = ctk.CTkLabel(master=midi_frame, text="MIDI Configuration", font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=0, padx=20, pady=10, sticky="nw", columnspan=4)

        label = ctk.CTkLabel(master=midi_frame, text="FL In Interface")
        label.grid(row=1, column=0, padx=20, sticky="nw")

        label = ctk.CTkLabel(master=midi_frame, text="FL Out Interface")
        label.grid(row=1, column=1, padx=20, sticky="nw")

        combo = ctk.CTkComboBox(
            master=midi_frame,
            values=["None"],
            command=None
        )
        combo.grid(padx=20, pady=0, row=2, column=0, sticky="ew")

        combo = ctk.CTkComboBox(
            master=midi_frame,
            values=["None"],
            command=None
        )
        combo.grid(padx=20, pady=0, row=2, column=1, sticky="ew")

        # Second row for MIDAS ports configuration
        label = ctk.CTkLabel(master=midi_frame, text="MIDAS In Interface")
        label.grid(row=3, column=0, padx=20, sticky="nw")

        label = ctk.CTkLabel(master=midi_frame, text="MIDAS Out Interface")
        label.grid(row=3, column=1, padx=20, sticky="nw")

        combo = ctk.CTkComboBox(
            master=midi_frame,
            values=["None"],
            command=None
        )
        combo.grid(padx=20, pady=0, row=4, column=0, sticky="ew")

        combo = ctk.CTkComboBox(
            master=midi_frame,
            values=["None"],
            command=None
        )
        combo.grid(padx=20, pady=0, row=4, column=1, sticky="ew")

    def createSubmitFrame(self):
        submit_frame = ctk.CTkFrame(master=self.app, width=500, height=100)
        submit_frame.grid_propagate(False)
        submit_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

        submit_frame.grid_columnconfigure((0, 1), weight=1)
        submit_frame.grid_rowconfigure((0, 1), weight=0)

        img = Image.open("./src/wrench-adjustable-circle.png")  # or your image path
        icon = ctk.CTkImage(img, size=(18, 18))

        log = ctk.CTkLabel(submit_frame, text=" This is a non‑editfyftyfytftyfable text area.", text_color="#E85028", image=icon, compound="left")
        log.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nw", columnspan=2)

        button = ctk.CTkButton(master=submit_frame, text="Set", width=30, height=30, image=icon, compound="left", text_color="black", fg_color="#E85028", hover_color="#FB9244", cursor="hand2")
        button.grid(row=1, column=1, padx=20, pady=(10, 20), sticky="se")

# Funzione callback
def combobox_callback(choice):
    print("Opzione selezionata:", choice)

app = GUI()