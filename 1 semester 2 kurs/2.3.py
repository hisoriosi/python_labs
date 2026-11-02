
import numpy as np
import matplotlib.pyplot as plt
import time

# A1, A2, A3, Амплитуды гармоник
# f1, f2, f3 Частоты гармоник
A1, A2, A3, f1, f2, f3 =1.25, 60, 0.4, 420, 0.25, 780


T=1/f1 #Перид высшей гармоники
k3=50 # Количество точек высшей гармоники
h=T/k3 # шаг дискритизации
ts=2*T #Продолжительность сигнала (три переуда)
N=round(ts/h)

t=np.linspace(0, ts, N)

u = (A1 * np.sin(2 * np.pi * f1 * t) +
     A2 * np.sin(2 * np.pi * f2 * t) +
     A3 * np.sin(2 * np.pi * f3 * t))

plt.figure(1)
plt.plot(t, u)
plt.grid()
plt.show(block=False)

