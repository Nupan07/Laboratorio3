# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 21:54:38 2024

@author: valen
"""
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from scipy.signal import find_peaks, butter, filtfilt
from scipy.fftpack import fft
import serial  # instalar la biblioteca pyserial
import time

class EMGAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de EMG")
        self.data = []
        self.fs = 1000  # Frecuencia de muestreo
        self.serial_port = 'COM3'  # Cambia esto al puerto correspondiente
        self.baud_rate = 115200  # Asegúrate de que coincida con tu configuración ESP32
        self.create_widgets()

    def create_widgets(self):
        self.load_button = ttk.Button(self.root, text="Cargar Señal", command=self.load_signal)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.filter_button = ttk.Button(self.root, text="Aplicar Filtro", command=self.apply_filter)
        self.filter_button.pack(side=tk.LEFT, padx=5)

        self.hamming_button = ttk.Button(self.root, text="Aplicar Hamming", command=self.apply_hamming)
        self.hamming_button.pack(side=tk.LEFT, padx=5)

        self.hanning_button = ttk.Button(self.root, text="Aplicar Hanning", command=self.apply_hanning)
        self.hanning_button.pack(side=tk.LEFT, padx=5)

        self.analyze_button = ttk.Button(self.root, text="Analizar Pulsos", command=self.analyze_pulses)
        self.analyze_button.pack(side=tk.LEFT, padx=5)

        self.fft_button = ttk.Button(self.root, text="Transformada Fourier", command=self.apply_fft)
        self.fft_button.pack(side=tk.LEFT, padx=5)

        # Botón de captura en tiempo real
        self.real_time_button = ttk.Button(self.root, text="Captura en Tiempo Real", command=self.real_time_capture)
        self.real_time_button.pack(side=tk.LEFT, padx=5)

    def load_signal(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt")])
        if file_path:
            try:
                data = np.loadtxt(file_path, delimiter=',', skiprows=3)
                self.data = data[:, 1] 
                self.fs = 1000 
                print("Señal cargada correctamente")
                plt.figure()
                plt.plot(self.data, label="Señal Cargada", color='blue')
                plt.title(f"Señal Cargada - Longitud: {len(self.data)} muestras")
                plt.xlabel("Muestras")
                plt.ylabel("Amplitud")
                plt.legend()
                plt.grid()
                plt.show()
            except Exception as e:
                print(f"Error al cargar la señal: {e}")

    def apply_filter(self):
        if len(self.data) == 0:
            print("No se ha cargado ninguna señal.")
            return
        b, a = butter(4, 100 / (0.5 * self.fs), btype='low')
        filtered_data = filtfilt(b, a, self.data)
        plt.figure()
        plt.plot(filtered_data, color='orange')
        plt.title("Señal Filtrada")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud")
        plt.grid()
        plt.show()

    def apply_hamming(self):
        if len(self.data) == 0:
            print("No se ha cargado ninguna señal.")
            return
        window = np.hamming(len(self.data))
        filtered_data = self.data * window
        plt.figure()
        plt.plot(filtered_data, color='green')
        plt.title("Señal con Ventana de Hamming")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud")
        plt.grid()
        plt.show()

    def apply_hanning(self):
        if len(self.data) == 0:
            print("No se ha cargado ninguna señal.")
            return
        window = np.hanning(len(self.data))
        filtered_data = self.data * window
        plt.figure()
        plt.plot(filtered_data, color='red')
        plt.title("Señal con Ventana de Hanning")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud")
        plt.grid()
        plt.show()

    def analyze_pulses(self):
        if len(self.data) == 0:
            print("No se ha cargado ninguna señal.")
            return
        peaks, _ = find_peaks(self.data, height=0.5, distance=200)
        plt.figure()
        plt.plot(self.data, label="Señal")
        plt.plot(peaks, self.data[peaks], 'rx', label="Pulsos detectados")
        plt.title(f"Pulsos Detectados - Total: {len(peaks)}")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud")
        plt.legend()
        plt.grid()
        plt.show()

        for i, peak in enumerate(peaks):
            start = max(0, peak - 50)
            end = min(len(self.data), peak + 50)
            pulse = self.data[start:end]
            media = np.mean(pulse)
            mediana = np.median(pulse)
            desviacion = np.std(pulse)
            print(f"Pulso {i + 1}: Media = {media:.2f}, Mediana = {mediana:.2f}, Desviación Estándar = {desviacion:.2f}")

    def apply_fft(self):
        if len(self.data) == 0:
            print("No se ha cargado ninguna señal.")
            return
        N = len(self.data)
        T = 1.0 / self.fs
        yf = fft(self.data)
        xf = np.fft.fftfreq(N, T)[:N // 2]
        plt.figure()
        plt.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
        plt.title("Transformada de Fourier")
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Amplitud")
        plt.grid()
        plt.show()

        max_freq_index = np.argmax(2.0 / N * np.abs(yf[:N // 2]))
        frecuencia_dominante = xf[max_freq_index]
        print(f"Frecuencia Dominante: {frecuencia_dominante:.2f} Hz")

    def real_time_capture(self):
        try:
            with serial.Serial(self.serial_port, self.baud_rate, timeout=1) as ser:
                plt.ion() 
                fig, ax = plt.subplots()
                ax.set_title("Captura en Tiempo Real")
                ax.set_xlabel("Muestras")
                ax.set_ylabel("Amplitud")
                line, = ax.plot([], [], color='blue') 
                ax.set_xlim(0, 100)
                ax.set_ylim(-1, 1)  
                plt.show()

                # Bucle de captura de datos
                while True:
                    data = ser.readline().decode('utf-8').strip()  
                    if data:
                        value = float(data)  # Convierte el valor a float
                        self.data.append(value) 
                        line.set_xdata(np.arange(len(self.data)))
                        line.set_ydata(self.data)
                        ax.set_xlim(0, len(self.data))  
                        plt.pause(0.01)

        except Exception as e:
            print(f"Error en la captura en tiempo real: {e}")

# Crear la interfaz de Tkinter
root = tk.Tk()
app = EMGAnalyzer(root)
root.mainloop()
