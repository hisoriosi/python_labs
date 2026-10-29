
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

t0=time.time()

w=2*np.pi*N

a=np.zeros(10, dtype=float)
b=np.zeros(10, dtype=float)

for k in range(10):
    a[k] = (h / ts) * (1 + u[N - 1] * np.cos((k + 1) * w * ts) + 2 * np.sum(u[0:N - 1] * np.cos((k + 1) * w * t[0:N - 1])))
    b[k] = (h / ts) * (u[N - 1] * np.sin((k + 1) * w * ts) + 2 * np.sum(u[0:N - 1] * np.sin((k + 1) * w * t[0:N - 1])))

# Рассчитываем амплитуды гармоник
F = np.sqrt(a**2 + b**2)

tp = time.time() - t0       # Определение потраченного времени

print('Время выполнения ',tp,' с')

plt.figure(2)
plt.bar(np.arange(1,11), F)
plt.grid()
plt.show(block=False)

# Использование формулы дискретного преобразования Фурье

t0 = time.time()

X = np.zeros(N, dtype = complex)

for k in range(N):
    X[k] = np.sum(u*np.exp(-2*np.pi*1j*k*np.arange(N)/N))

F1 = (2/N)*abs(X[1:11])

tp = time.time() - t0       # Определение потраченного времени

print('Время выполнения ',tp,' с')

plt.figure(3)
plt.bar(np.arange(1,11),F1)
plt.grid()
plt.show(block=True)