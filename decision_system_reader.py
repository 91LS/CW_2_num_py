import tools
from tkinter import *
from tkinter import ttk
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

        rb_frame = Frame(self)  # 2nd frame // radio buttons and GO!
        rb_frame.pack(fill=X)

        self.algorithm = IntVar()

        self.radio_button1 = Radiobutton(rb_frame, text="Covering", variable=self.algorithm, value=1)
        self.radio_button1.pack(side=LEFT, padx=5, pady=5)
        self.radio_button1.invoke()

        self.radio_button2 = Radiobutton(rb_frame, text="Exhaustive", variable=self.algorithm, value=2)
        self.radio_button2.pack(side=LEFT, padx=5, pady=5)

        self.radio_button3 = Radiobutton(rb_frame, text="LEM2", variable=self.algorithm, value=3)
        self.radio_button3.pack(side=LEFT, padx=5, pady=5)

        self.start_button = Button(rb_frame, text="GO!", state=DISABLED, command=self.__get_decision_system)
        self.start_button.pack(padx=5, pady=5, fill=X)

        tree_frame = Frame(self)  # 3rd frame // tree
        tree_frame.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(tree_frame, selectmode=NONE)
        self.tree.pack(padx=5, pady=5, fill=BOTH, expand=True)

        scrollbar.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading('#0', text='Rules')
        self.tree["columns"] = "count"
        self.tree.column("count", width=1)
        self.tree.heading("count", text="Count")

    def __get_system_filename(self):
        self.system_file_path = filedialog.askopenfilename(filetypes=[('Txt files', '*.txt')])
        self.system_text_box.configure(state=NORMAL)
        self.system_text_box.delete(0, "end")
        self.system_text_box.insert(0, self.system_file_path)
        self.system_text_box.configure(state=DISABLED)
        if self.system_text_box.get() != '':
            self.start_button.config(state=NORMAL)

    def insert_rules(self, rules):
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", 1, 1, text="All orders", values=rules.__len__())
        scales = tools.get_scales(rules)
        for scale in scales:
            self.tree.insert(1, scale+1, scale+1, text="Order {}".format(scale),
                             values=tools.get_rule_scale_length(rules, scale))
            for string_rule in tools.scale_rules(rules, scale):
                self.tree.insert(scale+1, scale+1, text=string_rule)

    def __get_decision_system(self):
        try:
            with open(self.system_file_path) as file:
                decision_system, names = tools.get_system_objects(file)
            rules = tools.find_rules(self.__get_algorithm(), decision_system)
            tools.rename_rules(rules, names)
            self.insert_rules(rules)
        except FileNotFoundError:
            messagebox.showerror("Error", "Oops! File not found!")

    def __get_algorithm(self):
        if self.algorithm.get() == 1:
            return tools.covering
        elif self.algorithm.get() == 2:
            return tools.exhaustive
        elif self.algorithm.get() == 3:
            return tools.lem2


def main():
    main_frame = Tk()
    ex = MainFrame(main_frame)
    main_frame.geometry("660x450+420+200")
    main_frame.mainloop()


if __name__ == '__main__':
    main()
