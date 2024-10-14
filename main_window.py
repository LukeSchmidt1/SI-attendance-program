import tkinter as tk
import webbrowser
from tkinter import ttk
from Database_init import Database

class MainWindow:
    def __init__(self, master, database):
        self.master = master
        self.master.title('Main Application')
        self.master.geometry('2880x1800')

        self.database = database

        # Fetch leaders data from the database (excluding ID)
        leaders_data = self.database.get_leaders()  # Fetch all the fields excluding ID

        # Create a Treeview widget
        columns = ('First Name', 'Last Name', 'Session Days', 'Session Times', 'Room location', 'Observed Count', 'Department')
        self.tree = ttk.Treeview(self.master, columns=columns, show='headings')

        # Create headings for each column
        for column in columns:
            self.tree.heading(column, text=column)

        # Set column widths
        for column in columns:
            self.tree.column(column, width=100)

        # Add gridlines using alternating row colors
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='white')

        # Insert the data into the treeview with tags
        for index, leader in enumerate(leaders_data):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=leader, tags=(tag,))

        # Configure the treeview to show gridlines
        self.tree.pack(side='bottom', anchor='center', fill='x', expand=True)

        # Add a separator
        self.seperator = ttk.Separator(self.master, orient='horizontal')
        self.seperator.pack(fill='x')

    def logout(self):
        print('logout clicked')
        self.master.withdraw()  # Hide the current window
        root.deiconify()  # Show the root window

    def admin_login(self):
        print('Admin login clicked')

    def open_website(self):
        webbrowser.open('https://sidocuments.com')

if __name__ == '__main__':
    root = tk.Tk()
    database = Database()
    app = MainWindow(root, database)  
    root.mainloop()
