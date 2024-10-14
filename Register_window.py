import tkinter as tk
from tkinter import messagebox

class RegisterWindow:
    def __init__(self, master, database, root):
        self.master = master
        self.root = root
        self.master.title("Registration form")
        self.master.geometry('340x440')
        self.database = database

        self.frame = tk.Frame(master)
        self.frame.pack()
        
        # Create error message label (Empty)
        self.error_label = tk.Label(self.frame, text='', font=('Arial', 12), fg='red')
        self.error_label.grid(row=0, column=0, columnspan=2)

        # create labels for user input
        self.register_label = tk.Label(self.frame, text='Register', font=('Arial', 30))
        self.username_label = tk.Label(self.frame, text='Username', font=('Arial', 16))
        self.username_entry = tk.Entry(self.frame, font=('Arial', 16))
        self.password_label = tk.Label(self.frame, text='Password', font=('Arial', 16))
        self.password_entry = tk.Entry(self.frame, show='*', font=('Arial', 16))
        self.register_button = tk.Button(self.frame, text='Submit', command = self.register_user, font=('Arial', 16))
        self.back_button = tk.Button(self.frame, text='Back', command=self.go_back, font=('Arial', 16))

        # department selection
        self.department_label = tk.Label(self.frame, text='Select Department', font=('Arial', 16))

        # define the departments
        self.departments = [' ', 'Mence', 'Mapp', 'Beck']
        self.selected_department = tk.StringVar(self.master)
        self.selected_department.set(self.departments[0]) # default value

        # create the option menu
        self.department_menu = tk.OptionMenu(self.frame, self.selected_department, *self.departments)

        # place widgets on grid
        self.register_label.grid(row=0, column=0, columnspan=2, pady=40)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        self.department_label.grid(row=4, column=0)
        self.department_menu.grid(row=4, column=1, pady=10)
        self.register_button.grid(row=5, column=0, columnspan=2, pady=30)
        self.error_label.grid(row=4, column=0, pady=2)
        self.back_button.grid(row=0, column=0)

        # add department dropdown
        self.department_label.grid(row=3, column=0)
        self.department_menu.grid(row=3, column=1, pady=20)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        department = self.selected_department.get()

        if not username:
            self.error_label.config(text='Registration failed: Please enter Username')
            return
        elif not password:
            self.error_label.config(text='Registration failed: Please enter Password')
            return
        elif department == ' ':
            self.error_label.config(text='Registration failed, Please select a valid department')
            return
        elif not username and not password:
            self.error_label.config(text='Registration failed: please enter username and password')
            return
        else:
            self.database.add_user(username, password, department)
            self.error_label.config(text='')

        success_window = tk.Toplevel(self.master)
        success_window.title('Success')
        success_window.geometry('300x300')

        self.success_label = tk.Label(success_window, text='Registration successful. Returning you to the login screen', font=('Arial', 16))
        success_window.after(3000, lambda: self.close_success_window(success_window))
    
    def close_success_window(self, success_window):
        success_window.destroy()
        # return to login window
        self.master.destroy()
        self.root.deiconify()
    
    def go_back(self):
        self.master.destroy()
        self.root.deiconify()

    
