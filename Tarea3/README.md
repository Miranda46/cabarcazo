# Proyecto de Análisis y Visualización de Datos

## Descripción General
Este proyecto implementa un sistema de análisis y visualización de datos que procesa datos experimentales utilizando interpolación mediante splines cúbicos naturales.

## Requisitos
- Python 3.x
- NumPy
- Matplotlib
- Pandas
- SciPy (utilizado solo para probar nuestra implementación de interpolación spline cúbica)

## Formato de Datos de Entrada
- Archivo CSV con N+1 filas y M+1 columnas
- Primera fila contiene los encabezados de las columnas
- Primera columna representa coordenadas x
- Columnas subsiguientes representan coordenadas y para diferentes experimentos
- Valores separados por punto y coma

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

## Manejo de Errores
- Validación de existencia de archivos
- Verificación de formato de datos
- Manejo de errores de cálculos numéricos

## Uso
