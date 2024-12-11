# Proyecto de Análisis y Visualización de Datos

## Descripción General
Este proyecto implementa un sistema de análisis y visualización de datos que procesa datos experimentales utilizando interpolación mediante splines cúbicos naturales.

## Requisitos
- Python
- NumPy
- Matplotlib
- Pandas
- SciPy
- pytest

Para instalar todas las dependencias:
```bash
pip install numpy matplotlib pandas scipy pytest
```

## Formato de Datos de Entrada
- Archivo data.csv con N+1 filas y M+1 columnas
- Primera fila contiene los nombres de M experimentos
- Primera columna representa coordenadas "x"
- Columnas subsiguientes representan coordenadas "y" para diferentes experimentos
- Valores separados por punto y coma ( ; )

## Detalles de Implementación

### Procesamiento de Datos
1. Leer archivo CSV de entrada
2. Dividir el rango de coordenadas x en n intervalos iguales
3. Realizar regresión lineal para cada intervalo
4. Calcular puntos medios de las líneas de regresión
5. Aplicar interpolación spline cúbico
6. Calcular la derivada de la curva de interpolación

### Interpolación con Splines Cúbicos Naturales
La implementación utiliza splines cúbicos naturales, donde:
- Las segundas derivadas en los extremos son cero
- Se garantiza continuidad C2 en los nodos internos
- El algoritmo sigue el método descrito en Burden & Faires
  1. Calcula las diferencias de x (h)
  2. Calcula los coeficientes alpha
  3. Resuelve el sistema tridiagonal para los coeficientes c
  4. Calcula los coeficientes b y d

### Visualización
- Generar gráficos individuales mostrando:
  - Puntos de datos originales
  - Líneas de regresión lineal
  - Puntos medios
  - Curva de interpolación spline cúbica
  - Curva derivada (en eje secundario)
- Crear una cuadrícula de visualización con:
  - Columnas: Diferentes experimentos
  - Filas: Valores de n desde 6 hasta 10

### Convención de Nombres de Archivos
Los archivos de salida se guardan como `{nombre_columna}_n.png` donde:
- nombre_columna: Nombre del experimento (encabezado de columna)
- n: Número de intervalos utilizados

## Pruebas
- Pruebas unitarias para la interpolación spline cúbica que comparan nuestra implementación con la biblioteca SciPy:
  - Prueba de interpolación polinomial cúbica
  - Prueba de interpolación sinusoidal
  - Prueba de condiciones de frontera
  - Prueba de puntos de interpolación
- Las pruebas utilizan la implementación de `CubicSpline` de SciPy como referencia para validar la precisión numérica de nuestra propia implementación
- Manejo de errores para operaciones de archivo de entrada

### Ejecutar Pruebas

```bash
python test.py
```

## Uso
1. Prepare sus datos en formato CSV con el formato especificado (ver sección "Formato de Datos de Entrada")

2. Ejecute el programa:

3. El programa generará:

- Gráficos individuales para cada columna de datos con nombre {columna}_n{numero}.png
- Un gráfico de cuadrícula comparativo grid_visualization.png

4. Interpretación de los gráficos:

- Puntos grises: datos originales
- Puntos rojos: puntos medios de intervalos
- Línea verde: curva de interpolación spline
- Línea roja punteada: derivada de la curva (eje secundario)
