import sys
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


def get_contour_points(A: float,
                       B: float,
                       num_points: int = 200):
    x = np.linspace(-A, A, num_points)  # область значений x

    # Выразим теперь y отсюда
    t = (x / A) ** 4
    t = np.clip(t, 0, 1)  # т.к 4-ая степень любого числа неотрицательна!
    y_pos = B * (1 - t) ** 0.25  # ** 0.25 -- извлечение корня 4-ой степени
    y_neg = -y_pos
    return x, y_pos, y_neg


def get_plot(A: float,
             B: float,
             num_points: int = 200):
    x, y_pos, y_neg = get_contour_points(A, B, num_points)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(x, y_pos)
    ax.plot(x, y_neg)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title(f'|x/{A}|^4 + |y/{B}|^4 = 1')
    ax.set_xlabel('x (см.)')
    ax.set_ylabel('y (см.)')
    ax.legend()
    return fig


def calc_square(A: float,
                B: float,
                method: str) -> float:
    def _calc_y(x):
        t = (x / A) ** 4
        if t > 1:
            t = 1.0
        return B * (1 - t) ** 0.25

    def _trapezoid_square(x: list, y: list):
        full_square = 0.0
        for i in range(len(x) - 1):
            dx = x[i + 1] - x[i]  # высота
            height = (y[i] + y[i + 1]) / 2.0  # полусумма оснований
            full_square += height * dx
        return full_square

    if method == 'scipy':
        half_square, _ = quad(_calc_y, -A, A)
        return half_square * 2

    if method == 'trapezoid':
        x_values, y_values, _ = get_contour_points(A, B, num_points=1000)
        half_square = _trapezoid_square(x_values, y_values)
        return half_square * 2


def main():
    # Настройки окна
    my_window = Tk()

    we = 1920  ## Разрешение экрана в пикселях
    he = 1080
    ww = 1280  ## Размеры окна в пикселях
    hw = 720
    s = (str(ww) + "x" + str(hw) + "+"  ## Управляющая строка
         + str(int(we / 2 - ww / 2)) + "+"
         + str(int(he / 2 - hw / 2)))
    my_window.geometry(s)
    my_window.title('Расчетно-графическое задание (вариант 9)')
    icon = PhotoImage(file='assets/icon.png')
    my_window.iconphoto(False, icon)
    my_window.resizable(False, False)  ## Зафиксировать размер окна

    background = Image.open('assets/background.jpg')
    bg_image = ImageTk.PhotoImage(background)
    bg_label = Label(my_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    function = PhotoImage(file='assets/conditions.png')
    equation = Label(image=function)
    equation.place(x=int(ww / 8.0), y=20)
    equation.lift()

    def _exit_button():
        my_window.quit()
        sys.exit()

    exit_btn = Button(
        my_window,
        text='Выход',
        command=_exit_button,
        font=("Ubuntu Mono", 10))

    exit_btn.place(x=1200, y=680, width=70, height=30)

    # Входные данные
    A = Label(
        my_window,
        text='a = ',
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono', 20),
        width=5)
    A.place(x=60, y=170)
    A_input = Entry(
        my_window,
        font=('Ubuntu Mono', 19),
        justify=LEFT)
    A_input.place(x=120, y=170, width=100)

    B = Label(
        my_window,
        text='b = ',
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono', 20),
        width=5)
    B.place(x=250, y=170)
    B_input = Entry(
        my_window,
        font=('Ubuntu Mono', 19),
        justify=LEFT)
    B_input.place(x=310, y=170, width=100)

    delta = Label(
        my_window,
        text="\u03b4 = ",
        background="#6B7D81",
        foreground="#030303",
        font=('Ubuntu Mono', 20),
        width=5)
    delta.place(x=440, y=170)
    delta_input = Entry(
        my_window,
        font=('Ubuntu Mono', 19),
        justify=LEFT)
    delta_input.place(x=500, y=170, width=100)

    square_methods = ["scipy.integrate.quad", "Метод трапеций"]
    combobox = ttk.Combobox(my_window,
                            values=square_methods,
                            state="readonly",
                            background="#6B7D81",
                            foreground="#030303",
                            font=('Ubuntu Mono', 14), )
    combobox.set("Выберите метод вычисления площади проводника")
    combobox.place(x=80, y=240, width=500)

    trapezoid_formula_ = PhotoImage(file='assets/trapezoid_formula.png')
    trapezoid_formula = Label(image=trapezoid_formula_)
    trapezoid_formula.place(x=30, y=300)
    trapezoid_formula.lift()

    # Вывод ответа/ошибки
    out_status = StringVar()
    out_error_widget = Label(
        my_window,
        font=('Ubuntu Mono', 14),
        justify=LEFT,
        background="#FFFFFF",
        foreground="#D41111",
        textvariable=out_status,
        wraplength=380)
    out_error_widget.place(x=130, y=570, width=400, height=100)

    # Значения по умолчанию
    A_input.insert(0, '1.0')
    B_input.insert(0, '2.0')
    delta_input.insert(0, '200.0')

    # Фрейм для графика
    plot_frame = Frame(my_window, background="#FFFFFF", relief=SUNKEN, bd=2)
    plot_frame.place(x=750, y=250, width=425, height=425)
    label = Label(my_window, text="Форма поперечного сечения проводника в масштабе")
    label.place(x=750, y=180, width=425, height=50)

    # Получение значений и вывод графика с ответом
    def _calc_integral_button():
        out_status.set("")
        for widget in plot_frame.winfo_children():
            widget.destroy()
        try:
            A_value = float(A_input.get())
            B_value = float(B_input.get())
            delta_value = float(delta_input.get())

            # Проверка на корректность интервала
            if A_value >= B_value:
                out_status.set("Ошибка: A должен быть меньше B")
                return

            # Построение графика
            generated_fig = get_plot(A_value, B_value)

            # Встраиваем фигуру во фрейм
            canvas = FigureCanvasTkAgg(generated_fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH,
                                        expand=True,
                                        padx=5, pady=5)

            # Сохраняем ссылки, чтобы предотвратить сборку мусора
            plot_frame.canvas = canvas
            plot_frame.fig = generated_fig

            # Получение выбора метода расчета площади
            calc_type = combobox.get()
            if 'scipy' in calc_type:
                square_value = calc_square(A_value, B_value, 'scipy')
            else:
                square_value = calc_square(A_value, B_value, 'trapezoid')
            answer = square_value / 10000 * delta_value
            out_status.set(f'Ответ: {answer:.4f} A')
        except ValueError as e:
            out_status.set(f'Ошибка ввода числа: {str(e)}')
        except Exception as e:
            out_status.set(f'Ошибка: {str(e)}')

    btn = Button(
        my_window,
        text='Рассчитать величину тока',
        command=_calc_integral_button,
        font=("Ubuntu Mono", 19))
    btn.place(x=130, y=470, width=400, height=50)

    # Запуск
    my_window.mainloop()


if __name__ == "__main__":
    main()мс