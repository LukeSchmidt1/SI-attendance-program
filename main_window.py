import tkinter as tk
import webbrowser
from tkinter import ttk, Menu
from Database_init import Database

class MainWindow:
    def __init__(self, master, database):
        self.master = master
        self.master.title('Main Application')
        self.master.geometry('800x600')  # Set a manageable window size

        self.database = database

        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Create a dropdown menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Options', menu=self.file_menu)

        # Add items to the dropdown menu
        self.file_menu.add_command(label='Open Website', command=self.open_website)
        self.file_menu.add_command(label='Admin Login', command=self.admin_login)
        self.file_menu.add_separator()  # Add a separator
        self.file_menu.add_command(label='Logout', command=self.logout)

        # Fetch leaders data from the database (excluding ID)
        self.leaders_data = self.database.get_leaders()  # Fetch all the fields excluding ID

        # Create a Treeview widget
        columns = ('First Name', 'Last Name', 'Class', 'Session Days', 'Session Times', 'Room Location', 'Observed Count', 'Department')
        self.tree = ttk.Treeview(self.master, columns=columns, show='headings')

        # Create headings for each column
        for column in columns:
            self.tree.heading(column, text=column, anchor='center')

        # Set column widths
        for column in columns:
            self.tree.column(column, width=100, anchor='center')

        # Add gridlines using alternating row colors
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='white')

        # Add scroll bar
        self.scrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Pack the Treeview and scrollbar at the bottom
        self.scrollbar.place(relx=1, rely=0.45, anchor='ne', height=300)  # Right side of the window
        self.tree.place(relx=0, rely=0.56, anchor='nw', relwidth=1, relheight=0.8)  # Centered and positioned below

        # Insert initial data into the treeview
        self.insert_data(self.leaders_data)

        # Create a frame for the filter entry and button
        filter_frame = tk.Frame(self.master)
        filter_frame.place(relx=.5, rely=.5, anchor='center')  # Position just above the treeview

        # Create filter entry (shortened width)
        self.filter_var = tk.StringVar()
        self.filter_entry = tk.Entry(filter_frame, textvariable=self.filter_var, width=30)  # Shortened width
        self.filter_entry.pack(side='left', padx=(0, 5))  # Pack left with some padding

        # Create filter button
        self.filter_button = tk.Button(filter_frame, text='Filter', command=self.apply_filter)
        self.filter_button.pack(side='left')  # Pack button to the right of the entry

        # Add a separator
        #self.separator = ttk.Separator(self.master, orient='horizontal')
        #self.separator.place(relx=0, rely=0.09, relwidth=1)  # Adjust position above the filter frame

    def logout(self):
        print('Logout clicked')
        self.master.withdraw()  # Hide the current window
        root.deiconify()  # Show the root window

    def admin_login(self):
        print('Admin login clicked')

    def open_website(self):
        webbrowser.open('https://sidocuments.com')
    
    def apply_filter(self):
        """Filter the treeview data based on the filter entry."""
        filter_value = self.filter_var.get().strip()  # Get the filter term
        filter_words = [word.strip().lower() for word in filter_value.split(',')]  # Split by comma and lower the case

        # Check if the filter value is empty
        if not filter_value:
            self.insert_data(self.leaders_data)
            return

        # Filter the data based on the filter_words
        filtered_data = [
            leader for leader in self.leaders_data
            if any(any(word in str(value).lower() for word in filter_words) for value in leader)
        ]

        # Insert the filtered data into the treeview
        self.insert_data(filtered_data)

    def insert_data(self, data):
        # Clear previous data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert the data into the treeview with tags
        for index, leader in enumerate(data):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=leader, tags=(tag,))

if __name__ == '__main__':
    root = tk.Tk()
    database = Database()
    app = MainWindow(root, database)  
    root.mainloop()
