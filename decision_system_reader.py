import tools
from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox


class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.system_file_path = ''
        self.type_filename = ''
        self.__init_ui()

    def __init_ui(self):
        self.parent.title("Decision System Reader")
        self.pack(fill=BOTH, expand=True)

        system_load_frame = Frame(self)  # 1st frame
        system_load_frame.pack(fill=X)

        self.load_system_button = Button(system_load_frame, text="Load system",
                                         command=self.__get_system_filename, width=15)
        self.load_system_button.pack(side=LEFT, padx=5, pady=5)

        self.system_text_box = Entry(system_load_frame)
        self.system_text_box.pack(fill=X, padx=5, expand=True)
        self.system_text_box.configure(state=DISABLED)

        start_button_frame = Frame(self)  # 2nd frame // GO!
        start_button_frame.pack(fill=X)

        self.start_button = Button(start_button_frame, text="GO!", state=DISABLED, command=self.__get_decision_system)
        self.start_button.pack(padx=5, pady=5, fill=X)

    def __get_system_filename(self):
        self.system_file_path = filedialog.askopenfilename(filetypes=[('Txt files', '*.txt')])
        self.system_text_box.configure(state=NORMAL)
        self.system_text_box.delete(0, "end")
        self.system_text_box.insert(0, self.system_file_path)
        self.system_text_box.configure(state=DISABLED)
        if self.system_text_box.get() != '':
            self.start_button.config(state=NORMAL)

    def __get_decision_system(self):
        try:
            system_file = open(self.system_file_path)
            self.decision_system, self.name_dictionary = tools.get_system_objects(system_file)
            rules = tools.covering(self.decision_system)
            tools.rename_rules(rules, self.name_dictionary)
            system_file.close()
        except FileNotFoundError:
            messagebox.showerror("Error", "Oops! File not found!")


def main():
    main_frame = Tk()
    ex = MainFrame(main_frame)
    main_frame.geometry("500x350+500+300")
    main_frame.mainloop()


if __name__ == '__main__':
    main()
