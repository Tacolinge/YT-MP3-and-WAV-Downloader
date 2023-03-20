import tkinter
import customtkinter
import Downloader_and_Functions as Df
import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("YT MP3 and WAV Downloader")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)

        # Input and button frame
        self.input_frame = customtkinter.CTkFrame(self, width=1100, height=75)
        self.input_frame.grid(row=0, columnspan=10, sticky="nsew")
        self.input_frame.grid_columnconfigure(5, weight=1)
        self.input_frame.grid_rowconfigure((0, 2), weight=0)
        self.label = customtkinter.CTkLabel(self.input_frame, text="YT MP3 and WAV Downloader",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, columnspan=10, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry_link = customtkinter.CTkEntry(self.input_frame, placeholder_text="Insert Youtube links here",
                                                 border_color="light gray", width=800, height=40)
        self.entry_link.grid(row=1, column=1, columnspan=10, padx=(25, 25), pady=(0, 20), sticky="nsew")

        # buttons
        self.settings_button = customtkinter.CTkButton(self.input_frame, text="Settings",
                                                       command=lambda: self.write_to_finish_textbox("Settings button"),
                                                       state="disabled")  # unused atm, may use in a future version
        self.settings_button.grid(row=2, column=1, padx=(25, 25), pady=(0, 20))
        self.label = customtkinter.CTkLabel(self.input_frame, text="Download as:")
        self.label.grid(row=2, column=6, padx=(5, 5), pady=(0, 20))
        self.file_type_value = tkinter.IntVar(value=0)
        self.mp3_button = customtkinter.CTkRadioButton(master=self.input_frame, text=".MP3",
                                                       variable=self.file_type_value, value=0)
        self.mp3_button.grid(row=2, column=7, padx=(5, 5), pady=(0, 20))
        self.waw_button = customtkinter.CTkRadioButton(master=self.input_frame, text=".WAV",
                                                       variable=self.file_type_value,
                                                       value=1)
        self.waw_button.grid(row=2, column=8, padx=(0, 0), pady=(0, 20))
        self.download_button = customtkinter.CTkButton(self.input_frame, text="DOWNLOAD",
                                                       command=lambda: self.initialize_download())
        self.download_button.grid(row=2, column=9, padx=(25, 25), pady=(0, 20))

        # textbox for download info
        self.textbox_frame = customtkinter.CTkFrame(self, width=600)
        self.textbox_frame.grid(row=1, rowspan=5, columnspan=10, sticky="nsew")
        self.textbox_frame.grid_columnconfigure(1, weight=1)
        self.textbox_frame.grid_rowconfigure((1, 2), weight=1)

        self.finished_num = tkinter.IntVar(value=Df.finished_display_number)
        self.download_que_num = tkinter.IntVar(value=Df.progress_que)
        self.finished_label = customtkinter.CTkLabel(self.textbox_frame,
                                                     text=("Finished:", Df.finished_display_number), text_color="light green")
        self.finished_label.grid(row=0, column=0, padx=(25, 10), pady=(10, 0), sticky="nsew")
        self.download_label = customtkinter.CTkLabel(self.textbox_frame,
                                                     text=("Que:", Df.progress_que),
                                                     text_color="light green")
        self.download_label.grid(row=2, column=0, padx=(25, 10), pady=(10, 0), sticky="new")
        self.textbox_show_finished = customtkinter.CTkTextbox(self.textbox_frame, text_color="light green", width=600,
                                                              height=250)
        self.textbox_show_finished.grid(row=0, column=1, rowspan=2, columnspan=10, padx=(25, 25), pady=(10, 20),
                                        sticky="nsew")
        self.textbox_prog = customtkinter.CTkTextbox(self.textbox_frame, width=600, height=100)
        self.textbox_prog.grid(row=2, column=1, columnspan=10, padx=(25, 25), pady=(0, 20), sticky="nsew")
        self.statusbar = customtkinter.CTkProgressBar(self.textbox_frame)
        self.statusbar.grid(row=3, column=1, columnspan=10, padx=(10, 10), pady=(0, 20), sticky="s")

        # set start values
        self.statusbar.configure(mode="indeterminnate")
        self.entry_link.focus_set()
        self.entry_link.bind('<Return>', command=lambda start: self.initialize_download())
        self.entry_link.bind('<Button-3>', command=lambda start: self.clear_entry())  # QoL right clear to clear input

        def updater(self):  # updates the gui, 500ms
            que_size = Df.progress_que
            self.download_label.configure(True, text=("Que:", que_size))
            self.finished_label.configure(True, text=("Finished:", Df.finished_display_number))

            if que_size != 0:
                self.statusbar.start()
            if que_size == 0:
                self.statusbar.stop()

            if len(Df.finished) > 0:  # adding finshed to display in textbox
                for element in Df.finished:
                    self.write_to_finish_textbox(element)
                    self.write_download_prog_textbox(element)
                    Df.finished.remove(element)
            self.write_download_prog_textbox(Df.download_status[0])
            App.after(self, 500, lambda: updater(self))  # updates every 500ms

        updater(self)

        # self.after(500)

    def write_to_finish_textbox(self, finished):
        tb = self.textbox_show_finished
        tb.insert("1.0", finished)
        tb.insert("1.0", "\n")

    def write_download_prog_textbox(self, prog):
        tb = self.textbox_prog
        tb.delete('1.0', tkinter.END)
        tb.insert("1.0", prog)

    def clear_entry(self):
        self.entry_link.delete([0], tkinter.END)
        print("Called clear_entry")

    def initialize_download(self):
        print("Called initialize_download")
        try:
            threading.Thread(target=Df.download_handler, args=(
                self.entry_link.get(), self.file_type_value)).start()  # spans new therad to keep the gui responsive
            self.clear_entry()
        except UserWarning:
            print("something went wrong with initialize_download")
            pass


