import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
from scipy.integrate import quad
from PIL import Image, ImageTk


def f(x, A, w):
    return A * np.sin(w * x)**2

def calculate_integral(xmin, xmax, A, w):
    integral, _ = quad(f, xmin, xmax, args=(A, w))
    return integral

def plot_function_and_integral(A, w, xmin, xmax, integral_value, plot_frame):    
    # Очищаем фрейм от предыдущих графиков
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    x = np.linspace(xmin, xmax, 1000)
    y = f(x, A, w)
    
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=100)
    
    # Строим график
    ax.plot(x, y, 'b-', linewidth=2, label=f'$f(x) = {A} \cdot \sin^2({w}x)$')
    ax.axhline(y=integral_value, color='r', linestyle='--', linewidth=2, 
               label=f'Интеграл = {integral_value:.4f}')
    
    # Настройки графика
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('f(x)', fontsize=10)
    ax.set_title(f'График функции f(x) = {A}·sin²({w}x)\nИнтеграл = {integral_value:.6f}', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)
    
    # Встраиваем график в tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=5, pady=5)
    
    # Сохраняем ссылки, чтобы предотвратить сборку мусора
    plot_frame.canvas = canvas
    plot_frame.fig = fig


def main():
    my_window = Tk()

    # Оформление
    we = 1920     ## Разрешение экрана в пикселях
    he = 1080
    ww = 1280     ## Размеры окна в пикселях
    hw = 720
    s = (str(ww)+"x"+str(hw)+"+"       ## Управляющая строка
        + str(int(we/2-ww/2))+"+"
        + str(int(he/2-hw/2)))
    my_window.geometry(s)
    my_window.title('Расчет определенного интеграла функции (вариант 9)')
    icon = PhotoImage(file='assets/icon.png')
    my_window.iconphoto(False, icon)
    my_window.resizable(False,False)  ## Зафиксировать размер окна
   
    background = Image.open('assets/background.jpg')
    bg_image = ImageTk.PhotoImage(background)
    bg_label = Label(my_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    function = PhotoImage(file='assets/function.png')
    equation = Label(image=function)
    equation.place(x=int(ww/4.5), y=60)
    equation.lift()

    # Интерфейс
    A = Label(
        my_window,
        text='A = ',
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono',20),
        width=5)
    A.place(x=60, y=250)
    A_input = Entry(
        my_window,
        font=('Ubuntu Mono',19),
        justify=LEFT)
    A_input.place(x=120, y=250, width=100)

    w = Label(
        my_window, text='w = ',
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono',20),
        width=5)
    w.place(x=60, y=300)
    w_input = Entry(
        my_window,
        font=('Ubuntu Mono',19),
        justify=LEFT)
    w_input.place(x=120, y=300, width=100)

    x_min = Label(
        my_window, text='x_min = ',
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono',20),
        width=8)
    x_min.place(x=60, y=350)
    x_min_input = Entry(
        my_window,
        font=('Ubuntu Mono',19),
        justify=LEFT)
    x_min_input.place(x=165, y=350, width=100)

    x_max = Label(
        my_window, text='x_max = ',
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono',20),
        width=8)
    x_max.place(x=60, y=400)
    x_max_input = Entry(
        my_window,
        font=('Ubuntu Mono',19),
        justify=LEFT)
    x_max_input.place(x=165, y=400, width=100)

    # Значения по умолчанию
    A_input.insert(0,'2.0')
    w_input.insert(0,'-3.0')
    x_min_input.insert(0,'1.0')
    x_max_input.insert(0,'2.0')

    out_error_title = Label(
        my_window, text='Результат:',
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono',15))
    out_error_title.place(x=35, y=550)

    out_status = StringVar()
    out_error_widget = Label(
        my_window,
        font=('Ubuntu Mono',14),
        justify=LEFT,
        background="#FFFFFF",
        foreground="#D41111",
        textvariable=out_status,
        wraplength=280)
    out_error_widget.place(x=35, y=575, width=300, height=100)

    # Фрейм для графика
    plot_frame = Frame(my_window, background="#FFFFFF", relief=SUNKEN, bd=2)
    plot_frame.place(x=400, y=250, width=700, height=425)

    # Кнопки
    def _calc_integral_button():
        out_status.set("")
        try:
            A_value = float(A_input.get())
            w_value = float(w_input.get())
            x_min_value = float(x_min_input.get())
            x_max_value = float(x_max_input.get())
            
            # Проверка на корректность интервала
            if x_min_value >= x_max_value:
                out_status.set("Ошибка: x_min должен быть меньше x_max")
                return
            
            integral_value = calculate_integral(x_min_value, x_max_value, A_value, w_value)
            plot_function_and_integral(A_value, w_value, x_min_value, x_max_value, integral_value, plot_frame)
            out_status.set(f'{integral_value:.6f}')
        except ValueError as e:
            out_status.set(f'Ошибка ввода числа: {str(e)}')
        except Exception as e:
            out_status.set(f'Ошибка: {str(e)}')

    def _exit_button():
        my_window.quit()
        sys.exit()
    
    btn = Button(
        my_window,
        text='Рассчитать интеграл',
        command=_calc_integral_button,
        font=("Ubuntu Mono", 19))
    btn.place(x=35, y=480, width=300, height=50)

    exit_btn = Button(
        my_window,
        text='Выход',
        command=_exit_button,
        font=("Ubuntu Mono", 10))
    exit_btn.place(x=1200, y=680, width=70, height=30)

    # Запуск
    my_window.mainloop()

if __name__ == "__main__":
    main()
