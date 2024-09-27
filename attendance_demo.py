import tkinter as tk
from tkinter import messagebox
from Database_init import Database
from Register_window import RegisterWindow


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Form")
        self.master.geometry('340x440')
        self.database = Database()

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.login_label = tk.Label(self.frame, text='Login', font=('Arial', 30))
        self.username_label = tk.Label(self.frame, text='Username', font=('Arial', 16))
        self.username_entry = tk.Entry(self.frame, font=('Arial', 16))
        self.password_label = tk.Label(self.frame, text='Password', font=('Arial', 16))
        self.password_entry = tk.Entry(self.frame, show='*', font=('Arial', 16))
        self.login_button = tk.Button(self.frame, text='Login', command=self.login, font=('Arial', 16))
        self.register_button = tk.Button(self.frame, text='Register', command=self.register, font=('Arial', 16))

        self.login_label.grid(row=0, column=0, columnspan=2, pady=40)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30)
        self.register_button.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.database.verify_user(username, password):
            print('Login successful')
            self.master.withdraw()
            MainWindow(tk.Toplevel(self.master))
        else:
            print('Login failed')
            #messagebox.showerror('Error', 'Invalid credentials')

    def register(self):
        self.master.withdraw()
        RegisterWindow(tk.Toplevel(self.master), self.database, root)

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Main Application')
        self.master.geometry('400x300')

        self.welcome_label = tk.Label(self.master, text='Welcome to the main window of the application')
        self.welcome_label.pack(pady=20)

        self.logout_button = tk.Button(self.master, text='Logout', command=self.logout)
        self.logout_button.pack(pady=20)

    def logout(self):
        self.master.destroy()
        root.deiconify()


if __name__ == '__main__':
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
