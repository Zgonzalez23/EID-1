# EID-1 — Análisis de Secciones Cónicas y Funciones por Tramos a partir del RUT

**Asignatura:** MAT1186 - Introducción al Cálculo  
**Universidad:** Universidad Católica de Temuco  
**Evaluación:** Evaluación Integrada de Desempeño N°1 (25% de la nota final)

---

## Descripción

Aplicación web desarrollada en Python con Streamlit que permite:

- **Validar un RUT chileno** usando el algoritmo oficial del módulo 11, mostrando el procedimiento paso a paso.
- **Construir automáticamente** una ecuación general de segundo grado a partir de los dígitos del RUT.
- **Clasificar la cónica** obtenida (circunferencia, elipse, hipérbola o parábola).
- **Transformar** la ecuación general a su forma canónica y viceversa, con desarrollo matemático paso a paso.
- **Graficar** la cónica en el plano cartesiano con sus elementos geométricos principales.
- **Analizar funciones por tramos** generadas desde el RUT: límites laterales, continuidad y tipos de discontinuidad.

---

## Estructura del proyecto

```
EID-1/
├── app.py                  # Punto de entrada principal (Streamlit)
├── utilidades.py           # Funciones auxiliares de formato y validación
├── requirements.txt        # Dependencias del proyecto
├── .gitignore
├── logicas/
│   ├── logica_rut.py       # Algoritmo módulo 11 para validar el RUT
│   ├── logica_conicas.py   # Construcción, clasificación y graficación de cónicas
│   └── logica_tramos.py    # Generación y análisis de funciones por tramos
└── pestanas/
    ├── rut.py              # Interfaz de la pestaña de validación de RUT
    ├── conicas.py          # Interfaz de la pestaña de análisis de cónicas
    └── tramos.py           # Interfaz de la pestaña de funciones por tramos
```

---

## Instalación y ejecución

### Requisitos previos

- Python 3.10 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone <URL-del-repositorio>
cd EID-1

# 2. (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`.

---

## Uso

1. Ingresa un RUT chileno válido en el campo de texto (formatos aceptados: `12345678-9`, `12.345.678-9`).
2. Navega entre las tres pestañas:
   - **Validación de RUT**: muestra el procedimiento del módulo 11 y los dígitos extraídos.
   - **Análisis de Cónicas**: muestra la ecuación general, la clasificación, la forma canónica, la transformación inversa y la gráfica interactiva.
   - **Función por Tramos**: muestra la función generada a partir del RUT, la tabla de valores, la gráfica y el módulo de análisis para la defensa oral.

---

## Restricciones de implementación

Todos los cálculos matemáticos (validación del RUT, construcción de coeficientes, completación de cuadrados, cálculo de límites laterales, clasificación de discontinuidades y generación de tablas de valores) están **implementados manualmente** en Python puro, sin uso de librerías como `numpy`, `math`, `sympy` o `scipy`.

Se usa `plotly` exclusivamente para la representación gráfica de las curvas, lo cual está permitido por la pauta.

---

## RUTs de prueba

A continuación se listan RUTs válidos que permiten observar cada tipo de cónica:

| RUT | Cónica generada |
|---|---|
| Por definir según dígitos del grupo | Circunferencia |
| Por definir según dígitos del grupo | Elipse |
| Por definir según dígitos del grupo | Hipérbola |
| Por definir según dígitos del grupo | Parábola |

*(Completar con los RUTs de prueba encontrados durante la Fase 4)*

---

## Código de ética del grupo

*Adjuntar o referenciar el documento de código de ética interno del grupo según lo exigido en la Fase 3 de la pauta.*
