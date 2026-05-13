from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Кнопка и список")
root.geometry("300x250")

def _you_can_button():
    if enabled.get() == 1:
        my_list['state'] = 'readonly'  # или 'normal'
    else:
        my_list['state'] = 'disabled'


enabled = IntVar()


enabled_checkbutton = ttk.Checkbutton(text="Можно", variable=enabled, command=_you_can_button)
enabled_checkbutton.pack(padx=6, pady=6, anchor=NW)


languages = ["book", "lamp", "computer", "table" ]
my_list = ttk.Combobox(values=languages, state="disabled")  # По умолчанию он заблокирован
my_list.pack(padx=6, pady=6, anchor=NW)


my_list.current(0)

root.mainloop()