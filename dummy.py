import tkinter as tk

def dummy_command():
    print('dummy command executed')
root = tk.Tk()
root.title('menu bar')
root.geometry('400x300')

menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label='Option 1', command=dummy_command)
file_menu.add_command(label='Exit', command=root.quit)
menubar.add_cascade(label='File', menu=file_menu)

root.config(menu=menubar)

root.mainloop()