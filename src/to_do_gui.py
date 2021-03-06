import tkinter as tk
from tkinter import messagebox
from functions import *

# create instance of class
my_list = TaskList()

class Window:

    def __init__(self, master):
        self.master = master
        master.title('TO-DO-List')

        self.label1 = tk.Label(master, text = 'Welcome to TO-DO-List - made by Marterminator', font = ('Times', 14), bd = 15)
        self.label1.grid(row = 0, columnspan = 2)

        self.add_entry = tk.Entry(master, width = 32, fg = 'grey') 
        self.add_entry.insert(0, 'Enter a task here...')
        self.add_entry.bind('<Button-1>', lambda event: self.entry_click(event, 'Enter a task here...', self.add_entry))
        self.add_entry.bind('<Return>', lambda event: self.add_task())
        self.add_entry.grid(row = 1)

        self.add_button = tk.Button(master, text = 'ADD', bg = 'green', command = self.add_task)
        self.add_button.grid(row = 1, column = 1)

        self.del_entry = tk.Entry(master, width = 32, fg = 'grey') 
        self.del_entry.insert(0, 'Enter a number here...')
        self.del_entry.bind('<Button-1>', lambda event: self.entry_click(event, 'Enter a number here...', self.del_entry))
        self.del_entry.grid(row = 2)

        self.del_button = tk.Button(master, text = 'DELETE', bg = 'orange', command = self.del_task)
        self.del_button.grid(row = 2, column = 1)

        self.mark_button = tk.Button(master, text = 'MARK', bg = 'light blue', command = self.mark_task)
        self.mark_button.grid(row = 3, column = 1)

        self.mark_entry = tk.Entry(master, width = 32, fg = 'grey') 
        self.mark_entry.insert(0, 'Enter a number here...')
        self.mark_entry.bind('<Button-1>', lambda event: self.entry_click(event, 'Enter a number here...', self.mark_entry))
        self.mark_entry.grid(row = 3)

        self.clear_button = tk.Button(master, text = 'CLEAR', bg = 'red', command = self.warning_box)
        self.clear_button.grid(row = 5, column = 1)

        self.info_button = tk.Button(master, text = 'INFO', bg = 'yellow', command = self.info)
        self.info_button.grid(row = 4, column = 1)

        self.export_button = tk.Button(master, text = 'EXPORT', bg = 'green', command = self.export)
        self.export_button.grid(row = 5, column = 0)

        self.import_button = tk.Button(master, text = 'IMPORT', bg = 'green')
        self.import_button.bind('<Button-1>', self.importe)
        self.import_button.grid(row = 6, column = 0)

        # create a Frame for the Text and Scrollbar
        self.txt_frm = tk.Frame(master, width=200, height=200)
        self.txt_frm.grid(row = 4)
        # consistent gui size
        self.txt_frm.grid_propagate(False)
        # implement stretchability
        self.txt_frm.grid_rowconfigure(0, weight=1)
        self.txt_frm.grid_columnconfigure(0, weight=1)

        self.text_box = tk.Text(self.txt_frm, borderwidth = 3, relief = 'sunken')
        self.text_box.config(font=('consolas', 10), undo = True, wrap = 'word')
        self.text_box.grid(row = 0, column = 0, sticky = 'nsew', padx = 2, pady = 2)
        self.text_box.insert(tk.END, 'Your TO-DO-List:') 

        self.vscroll = tk.Scrollbar(self.txt_frm, orient=tk.VERTICAL, command=self.text_box.yview)
        self.text_box['yscroll'] = self.vscroll.set
        self.vscroll.grid(row = 0, column = 1, sticky = 'nsew')

        self.exit_button = tk.Button(master, text = 'EXIT', bg = 'red', command = master.quit)
        self.exit_button.grid(row = 6, column = 1)

        self.status = tk.Label(master, text = '', bd = 1, relief = 'sunken', anchor = tk.W)
        self.status.grid(row = 7, columnspan = 2, sticky = tk.W+tk.E)

    def entry_click(self, event, default_text, entry):
        if entry.get() == default_text:
           entry.delete(0, tk.END)
           entry.config(fg = 'black')

    def message_box(self, text):
        messagebox.showinfo('Info', text)
        
    def warning_box(self):
        result = messagebox.askquestion('Clear', 'Are You Sure?', icon = 'warning')
        if result == 'yes':
            self.clear_tasks()

    def print_tasks(self):
        self.text_box.delete(1.0, tk.END)
        output_list = show_list(my_list)
        self.text_box.insert(tk.END, 'Your TO-DO-List:') 
        for task in output_list:
            self.text_box.insert(tk.END, '\n' + task)    

    def add_task(self):
        user_input = self.add_entry.get()
        my_list.insert_task(user_input)
        self.add_entry.delete(0, tk.END)
        self.print_tasks()
        self.status_bar('Added "' + user_input + '" to TO-DO-List.')
        # autoscroll to last element
        self.text_box.see('end')

    def del_task(self):
        user_input = int(self.del_entry.get())
        try:
            my_list.delete_task(user_input)
        except IndexError:
            self.message_box('Your number is out of range.')
        self.del_entry.delete(0, tk.END)
        self.print_tasks()
        self.status_bar('Deleted task ' + str(user_input) + '.')
        
    def mark_task(self):
        user_input = int(self.mark_entry.get())
        try:
            my_list.mark_done(user_input)
        except IndexError:
            self.message_box('Your number is out of range.')        
        self.mark_entry.delete(0, tk.END)
        self.print_tasks()
        self.status_bar('Marked task ' + str(user_input) + ' as done.')

    def clear_tasks(self):
        my_list.clear_list()    
        self.print_tasks()
        self.status_bar('Cleared TO-DO-List.')

    def info(self):
        self.message_box(info(my_list))

    def export(self):
        export(my_list)
        self.message_box('Your Task List is written to data.txt')
        self.status_bar('Exported TO-DO-List to data.txt.')

    def importe(self, event):
        importe(my_list) 
        self.print_tasks()
        self.status_bar('Imported TO-DO-List from ' + str(my_list.creation_date) + '.')

    def status_bar(self, status_text):
         self.status.config(text  = status_text)

root = tk.Tk()
create_window = Window(root)
root.mainloop()
