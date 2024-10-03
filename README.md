# README - Analizador de EMG

## Introducción
El electromiograma (EMG) es una grabación de la actividad eléctrica de los músculos, también llamada actividad mioeléctrica.Para poder realizar la captura de las señales mioeléctricas se utilizan dos electrodos activos y un electrodo de tierra o conocido como el de referencia .

### Objetivos

- Captura de señales EMG en tiempo real desde un ESP32.
- Aplicación de diferentes filtros (Hamming, Hanning y Butterworth) a las señales.
- Análisis de pulsos detectados en la señal EMG.
- Visualización de la transformada de Fourier de la señal.

## Requisitos

Antes de ejecutar, asegúrate de tener instalados los programas y bibliotecas


### Hardware

- Microcontrolador ESP32
- Cables de conexión y electrodos para la captura de señales EMG
- Computadora para ejecutar la interfaz gráfica

### Software

- Python (versión 3.6 o superior)
- Bibliotecas de Python:
  - NumPy
  - Matplotlib
  - SciPy
  - Tkinter (incluido en la mayoría de las instalaciones de Python)
  - PySerial

Puedes instalar las bibliotecas necesarias ejecutando:
pip install numpy matplotlib scipy pyserial

## Ventanas de Hamming y Hanning

### Ventana de Hamming

La **ventana de Hamming** es una función de ventana utilizada para reducir las discontinuidades en los extremos de una señal. Se define matemáticamente como:

\[ w[n] = 0.54 - 0.46 \cdot \cos\left(\frac{2\pi n}{N-1}\right) \]

donde \( N \) es el número total de muestras y \( n \) varía de 0 a \( N-1 \).

**Importancia**: Al aplicar la ventana de Hamming, se atenúan las fugas espectrales que pueden ocurrir al realizar la Transformada de Fourier. Esto es crucial en el análisis de señales, ya que permite obtener una representación más precisa del contenido en frecuencia de la señal.

### Ventana de Hanning

La **ventana de Hanning** (o ventana de coseno) también se utiliza para suavizar la señal. Su fórmula es:

\[ w[n] = 0.5 \cdot \left(1 - \cos\left(\frac{2\pi n}{N-1}\right)\right) \]

**Importancia**: Similar a la ventana de Hamming, la ventana de Hanning reduce el efecto de fugas. Sin embargo, su aplicación puede resultar en una mayor pérdida de amplitud para ciertas frecuencias. Es particularmente útil en aplicaciones donde se desea minimizar el ruido y resaltar las características relevantes de la señal.

## Importancia del Filtro

Los filtros son herramientas fundamentales en el procesamiento de señales, y su importancia radica en los siguientes aspectos:

1. **Reducción de Ruido**: Los filtros permiten eliminar componentes no deseadas de la señal, como el ruido de fondo, que puede afectar la calidad del análisis.
  
2. **Atenuación de Frecuencias no Deseadas**: Al aplicar un filtro pasa bajo, por ejemplo, se pueden atenuar las frecuencias que no son relevantes para el análisis, enfocándose en las frecuencias de interés.

3. **Mejora de la Precisión**: Al limpiar la señal, se mejora la precisión de la detección de picos y otros análisis cuantitativos, como el cálculo de estadísticas.

## Metodología

### 1. Captura de Señales

Se utilizan electrodos conectados al ESP32 para captar las señales EMG. Estas señales se transmiten a una computadora a través de un puerto serial, donde se procesan y analizan.

### 2. Aplicación de Filtros

Se aplicaron diferentes tipos de filtros para mejorar la calidad de las señales:

- **Filtro Butterworth**: Se utilizó un filtro de paso bajo para eliminar el ruido de alta frecuencia, estableciendo una frecuencia de corte en 100 Hz.
- **Ventanas de Hamming y Hanning**: Estas ventanas se aplicaron para reducir el efecto de fuga al realizar la transformada de Fourier, mejorando la resolución en frecuencia.


![](https://github.com/Nupan07/Laboratorio3/blob/main/Ventana%20Hamming.png)
![](https://github.com/Nupan07/Laboratorio3/blob/main/Ventana%20Hanning.png)
### 3. Análisis de Pulsos

Se implementaron técnicas de detección de picos para identificar los picos de la señal EMG. Se calcularon estadísticas como la media, la mediana y la desviación estándar de cada pulso detectado, lo que permite caracterizar la actividad muscular.

### 3.1. Hipotesis nula 
En estadística, una hipótesis nula es una afirmación que se utiliza para negar o confirmar una conclusión sobre un parámetro de la muestra que se está estudiando. En el contexto de la prueba de hipótesis, la hipótesis nula sostiene que los resultados de un experimento son incorrectos.

Por lo tanto, la hipótesis nula es la que se intenta rechazar. Si el investigador logra rechazar la hipótesis nula, esto sugiere que la hipótesis que quería probar en su estudio estadístico probablemente sea verdadera. Por el contrario, si no se puede rechazar la hipótesis nula, esto indica que la suposición que se quería demostrar es más probable que sea falsa. Más adelante, veremos en qué situaciones se puede rechazar la hipótesis nula.

### Frecuencia Dominante:
El resultado dice que la frecuencia dominante en la señal que analizaste es de 24.35 Hz. Esto significa que, en tu señal, hay un pico importante en esa frecuencia, lo que puede indicar que esa es la frecuencia más relevante o activa en la actividad muscular que estás midiendo.

### Estadístico de Prueba:
El estadístico de prueba es 8951091.0. Este número se usa para comparar cómo se comportan los datos con respecto a la hipótesis nula. Cuanto más alto sea este número, más probable es que los datos se aparten de lo que se espera según la hipótesis nula.

p-valor: 
El p-valor obtenido es 0.774. Este valor es clave porque te ayuda a determinar si debes rechazar la hipótesis nula. Un p-valor alto, como el que se obtuvo , generalmente indica que no hay suficiente evidencia para rechazar la hipótesis nula.




### 4. Visualización

Los resultados se visualizaron mediante gráficos, que incluyen:

- **Gráficas de la señal original y filtrada**: Comparación entre la señal capturada y la señal filtrada.
- **Pulsos detectados**: Visualización de los picos en la señal EMG.
- **Representación de la transformada de Fourier de la señal**
-  **Ventana de Hamming y Hanning**
-  
## Resultados

Los resultados obtenidos del análisis de las señales EMG incluyen:

- **Mejora en la Calidad de la Señal**: Se observó una reducción significativa del ruido tras aplicar el filtro Butterworth.
- **Detección de Pulsos**: Se identificaron múltiples pulsos en la señal, y se calcularon estadísticas que reflejan la actividad muscular.
- **Espectro de Frecuencia**: La transformada de Fourier mostró la distribución de frecuencias de la señal EMG, permitiendo una mejor comprensión de la actividad muscular.
