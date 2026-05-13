from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Кнопка и список")
root.geometry("300x250")


# Функция, которая срабатывает при клике на флажок
def _you_can_button():
    if enabled.get() == 1:
        # Если галочка стоит, делаем список активным
        my_list['state'] = 'readonly'  # или 'normal'
    else:
        # Если галочки нет, блокируем список
        my_list['state'] = 'disabled'


enabled = IntVar()

# Добавляем параметр command, который вызывает функцию toggle_list при клике
enabled_checkbutton = ttk.Checkbutton(text="Можно", variable=enabled, command=_you_can_button)
enabled_checkbutton.pack(padx=6, pady=6, anchor=NW)

# Создаем выпадающий список (Combobox)
languages = ["book", "lamp", "computer", "table" ]
my_list = ttk.Combobox(values=languages, state="disabled")  # По умолчанию он заблокирован
my_list.pack(padx=6, pady=6, anchor=NW)

# Устанавливаем первое значение по умолчанию
my_list.current(0)

root.mainloop()