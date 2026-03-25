# Práctica 2: Construcción de Autómatas Finitos con Interfaz Gráfica

## 👥 Alumnos

-   **Bonilla Ojeda Gustavo Sebastián** - 2025630175
-   **Velázquez Mendoza Ximena** - 2024630176
-   **Velázquez Ramos Yoltic Isaí** - 2025230228

**Grupo:** 4CM4\
**Fecha de entrega:** 24 de marzo de 2026

------------------------------------------------------------------------

## 🎯 1. Objetivo

El propósito de esta práctica es profundizar en la comprensión y
aplicación de los **Autómatas Finitos No Deterministas (AFND)** mediante
el uso de **JFLAP**, y desarrollar una aplicación con interfaz gráfica
que permita simular **Autómatas Finitos Deterministas (AFD)** a partir
de diferentes formatos de entrada.

------------------------------------------------------------------------

## 🛠️ 2. Desarrollo de la práctica

### 🔹 Parte 1: Implementación y análisis de AFND con JFLAP

Se resolvieron los ejercicios de:

-   **Lista 2:** Autómatas Finitos Deterministas\
-   **Lista 3:** AFND y transiciones λ

#### ✔️ Diseño y validación

-   Construcción de grafos en JFLAP\
-   Validación con:
    -   5 cadenas válidas\
    -   5 cadenas inválidas\
-   Uso de simulación paso a paso para observar bifurcaciones

#### 🔄 Análisis y conversión

-   Cálculo de **λ-clausura**
-   Conversión:
    1.  AFND-λ → AFND\
    2.  AFND → AFD

------------------------------------------------------------------------

### 🔹 Parte 2: Desarrollo del simulador de AFD

Se desarrolló un software interactivo en:

-   **Lenguaje:** Python 3\
-   **GUI:** Tkinter

#### ⚙️ Funcionalidades principales

##### ✏️ Creación y edición manual

-   Definición de la quíntupla:
    -   Alfabeto\
    -   Estados\
    -   Estado inicial\
    -   Estados de aceptación\
    -   Matriz de transiciones

##### 📂 Importación y exportación

-   Formatos soportados:
    -   `.jff` (JFLAP)\
    -   `.xml`\
    -   `.json`\
-   Uso de:
    -   `xml.etree.ElementTree`\
    -   `json`

##### ▶️ Validación y simulación

-   Validación rápida\
-   Modo **Paso a Paso** con traza de estados

##### 📊 Visualización

-   Grafo del autómata con:
    -   `networkx`\
    -   `matplotlib`\
-   Tabla dinámica con `Treeview`

##### 🔤 Operaciones de lenguajes

-   Prefijos\
-   Sufijos\
-   Subcadenas\
-   Cerraduras:
    -   Positiva (Σ⁺)\
    -   Kleene (Σ\*)

------------------------------------------------------------------------

### 🔹 Parte 3: Requisitos del entorno

#### 🐍 Lenguaje base

-   Python 3.x (agregado al PATH)

#### 📦 Bibliotecas nativas

-   `tkinter` / `ttk` → GUI\
-   `xml.etree.ElementTree` → XML / JFLAP\
-   `json` → serialización

#### 🌐 Bibliotecas externas

-   `networkx`\
-   `matplotlib`

``` bash
python -m pip install networkx matplotlib
```

------------------------------------------------------------------------

### 🔹 Parte 4: Arquitectura del sistema

El sistema está dividido en tres bloques:

------------------------------------------------------------------------

#### 🧩 A) Operaciones de lenguajes formales

-   Uso de **slicing** y ciclos anidados\
-   Almacenamiento en **sets** para evitar duplicados

**Implementaciones:** - Prefijos, sufijos y subcadenas\
- Cerradura positiva (Σ⁺)\
- Cerradura de Kleene (Σ\*)

------------------------------------------------------------------------

#### ⚙️ B) Motor lógico (Clase `Automata`)

Representa la quíntupla:

(Q, Σ, δ, q0, F)

##### 📚 Estructuras de datos

-   Estados y alfabeto → `set` (O(1))\
-   Transiciones → diccionario anidado

``` python
transiciones[origen][simbolo] = destino
```

##### 📥 Módulo de parseo

-   Importación desde `.jff` (XML)\
-   Exportación a XML / JSON

##### 🔍 Validación

-   Procesamiento carácter por carácter\
-   Registro de la traza de estados

------------------------------------------------------------------------

#### 🖥️ C) Interfaz gráfica (Clase `SimuladorApp`)

##### 🧾 Creación manual

-   Validación en tiempo real

##### 📊 Simulación visual

-   Tabla con `Treeview`\
-   Grafo con `networkx` + `matplotlib`

##### 🔄 Paso a paso

-   Visualización detallada de transiciones
