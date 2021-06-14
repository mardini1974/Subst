from tkinter import *
from tkinter import filedialog, ttk, messagebox
import string
from ctypes import windll, c_int, c_wchar_p


class Root:
    def __init__(self):
        self.file_Path = ""
        self.available_drive = self.get_drives()
        self.DefineDosDevice = windll.kernel32.DefineDosDeviceW
        self.DefineDosDevice.argtypes = [c_int, c_wchar_p, c_wchar_p]

        self.pad = 10
        # --------------------------Window------------------------------------------------------------
        self.window = Tk()
        self.window.minsize(width=300, height=200)
        self.window.config(padx=self.pad, pady=self.pad)
        self.window.iconbitmap('images/favicon.ico')
        self.window.title('Path substitute')

        # --------------------------Title------------------------------------------------------------
        title_label = Label(text="Substitute folder", font=("Helvetica", 24))
        title_label.grid(column=0, row=0, columnspan=2, sticky=W)
        # --------------------------Folder selection-------------------------------------------------
        self.directory_btn = Button(text="Get directory", command=self.open_file_dialog, padx=self.pad)
        self.directory_btn.grid(column=0, row=1)
        self.directory_entry = Entry(width=40)
        self.directory_entry.grid(column=1, row=1, padx=self.pad)
        # --------------------------Folder Letter selection------------------------------------------
        title_letter = Label(text="Folder letter")
        title_letter.grid(column=0, row=2, sticky=W, padx=self.pad, pady=self.pad)
        self.selected_drive = StringVar()
        self.drive_combo = ttk.Combobox(textvariable=self.selected_drive, width=37)
        self.drive_combo['values'] = self.available_drive
        self.drive_combo['state'] = 'readonly'
        self.drive_combo.grid(column=1, row=2)
        # --------------------------Subst buttons----------------------------------------------------
        self.replace_btn = Button(text="Replace path", command=self.do_subst, padx=self.pad)
        self.replace_btn.grid(column=1, row=3, padx=self.pad, pady=self.pad)
        self.un_replace_btn = Button(text="Delete Letter", command=self.un_do_subst, padx=self.pad)
        self.un_replace_btn.grid(column=1, row=4, padx=self.pad, pady=self.pad)
        # --------------------------Help buttons----------------------------------------------------
        help_img = PhotoImage(file="images/icons8-help-64.png")
        self.help_btn = Button(text="Help", image=help_img, command=self.show_help, padx=self.pad)
        self.help_btn.grid(column=0, row=3, rowspan=4, padx=self.pad, pady=self.pad)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        if self.replace_btn['state'] == 'disabled':
            result = messagebox.askquestion(title="Path substitute is running",
                                            message="Do you want to disconnect the substitution ")

            if result == 'yes':
                self.subst(2, self.drive_combo.get(), None)

        self.window.destroy()

    def show_help(self):
        messagebox.showinfo(title="Help",
                            message="Manually remove letter\nOpen command prompt:\nWrite 'subst x: /d'\nReplace x "
                                    "with chosen letter\nPress enter")

    def subst(self, parameter: int, letter: string, path: string):
        # Delete the subst.
        # parameter = 0 add subst
        # parameter = 2 remove subst
        # parameter = 4 remove exact path subst
        letter = letter + ":"
        if self.DefineDosDevice(parameter, letter, path) == 0:
            if parameter == 0:
                raise RuntimeError("subst failed")
            elif parameter == 2 or parameter == 4:
                raise RuntimeError("Couldn't remove subst")
            else:
                raise RuntimeError("unknown error")

    @staticmethod
    def get_drives():
        used_drives = []

        bitmask = windll.kernel32.GetLogicalDrives()

        for letter in string.ascii_uppercase:
            if bitmask & 1:
                used_drives.append(letter)
            bitmask >>= 1
        # print(used_drives)
        return [x for x in string.ascii_uppercase[2:] if x not in used_drives]

    def open_file_dialog(self):
        self.file_Path = filedialog.askdirectory()
        self.set_text(self.directory_entry, self.file_Path)

    @staticmethod
    def set_text(e: Entry, text):
        e.delete(0, END)
        e.insert(0, text)
        return

    def do_subst(self):
        letter = self.drive_combo.get()
        path = self.directory_entry.get()
        if letter != "" and path != "":
            self.subst(0, letter, path)
            self.replace_btn['state'] = 'disabled'
            self.drive_combo['state'] = 'disabled'
        else:
            if letter == "":
                messagebox.showinfo(title="Error", message="No letter is selected, select a letter and click")
            if path == "":
                messagebox.showinfo(title="Error", message="No Path is selected, select a new path and click")

    def un_do_subst(self):
        letter = self.drive_combo.get()
        if letter != "":
            self.subst(2, letter, None)
            self.replace_btn['state'] = 'normal'
            self.drive_combo['state'] = 'normal'
        else:
            messagebox.showinfo(title="Error", message="No letter is selected, select a letter and click")


if __name__ == "__main__":
    window = Root()
