# Ancient-Core: Universal Computational Framework for Ethnomathematics and Archeo-Astronomy

   
[![License: MIT](https://shields.io)](https://opensource.org)
[![Python 3.10+](https://shields.io)](https://python.org)
[![Institution: ICSR](https://shields.io)](https://github.com/stdm-topological-framework)

Developed under the auspices of the **Independent Center for Space Research (ICSR)**.

---

## 🌌 Project Manifesto

Modern computer science and numerical astrophysics are heavily built upon the Western Eurocentric mathematical trajectory (continuous functions, Newtonian calculus, Euclidean space). However, ancient and medieval civilizations developed highly advanced, **discrete, algorithmic, and context-dependent computational systems** that were completely independent of Western algebra. 

Many of these methods do not use vectors or matrices; instead, they operate on complex discrete automata, non-Archimedean modular structures, and iterative finite differences. Because these manuscripts are studied almost exclusively by humanities scholars, **over 800 foundational algorithms of ancient mathematics remain un-coded** and locked away in static paper archives and PDF scans.

**Ancient-Core** is the world's first open-source, production-grade Python library designed to digitalize, reverse-engineer, and execute the ethnomathematical and archeo-astronomical algorithms of global civilizations. We bridge the gap between historical manuscripts and modern discrete computing.

---

## 🗺️ Global Monorepository Architecture

The framework is structured as a unified, tightly typed monorepository partitioned by cultural and geographic computing traditions:

```text
ancient-core/
│
├── README.md               # Global research manifesto and architecture
├── requirements.txt         # Environment dependencies (numpy, matplotlib, etc.)
│
├── africa/                  # Sub-Saharan Geometric & Logical Traditions
│   └── sona_graphs.py       # Chokwe "Sona" sand-graph Eulerian path generator
│
├── america/                 # Indigenous American Computational Systems
│   ├── medicine_wheel.py    # Non-Euclidean "Medicine Wheels" astronomical calculators
│   ├── quipu_decoder.py     # Hierarchical Inca Quipu data matrix parser & validator
│   ├── quipu_encoder.py     # Inca Quipu uldular data serializer (JSON-to-Quipu)
│   └── navajo_cellular.py   # Navajo Diné procedural fractal weaving engine (Cellular Automata)
│
├── babylon/                 # Mesopotamian Mathematics
│   └── base64_cascade.py    # Sexagesimal divisionless reciprocal arithmetic engine
│
├── china/                   # Sinitic Algorithmic Tradition
│   ├── cauldron_simulator.py # Waidan (外丹) phase-transition discrete automaton
│   └── shao_yong_matrix.py  # Shao Yong (邵雍) 6-bit binary cyclic space-time matrix
│
├── incas/                   # Legacy Andean Administrative Computations (Merged to /america)
│
├── india/                   # Vedic & Kerala Mathematical Traditions
│   └── kuttaka_solver.py    # Brahmagupta's (VII c.) "Pulverizer" astronomical solver
│
├── japan/                   # Wasan (和算) Edo-Period Mathematics
│   └── sangaku_generator.py # Sangaku (算额) non-trigonometric geometric engine
│
└── russia/                  # Old Russian Computational Manuscripts
    └── kirik_time.py        # Kirik the Novgorodian's (1136) 5-ary fractal time engine

```

---

## 🚀 Active Core Modules & Mathematical Logic

### 1. Sinitic Tradition (`/china`)
*   **`cauldron_simulator.py` (Waidan Alchemical Engine):** Simulates the non-linear thermodynamic phase transitions described in the *Zhouyi Cantong Qi* (II c. AD). It utilizes hexagram-driven time-varying steps to map changes in Yin (Mercury) and Yang (Lead) abstract variables, bypasses continuous differential equations, and operates as a strict finite-state machine.
*   **`shao_yong_matrix.py` (Binary Combinatorics):** Models Shao Yong's (XI c.) "Before Heaven" \(8 \times 8\) grid. It maps 64 hexagrams directly to 6-bit CPU integers (`0b000000` to `0b111111`) and processes topological state transitions via bitwise operations (`XOR`, Hamming distance shifts).

### 2. Vedic & Kerala Tradition (`/india`)
*   **`kuttaka_solver.py` (The Pulverizer):** Implements Brahmagupta's (628 AD) original algorithm for solving indeterminate linear equations (\(ax - by = c\)). Historically used to calculate planetary syzygies and orbital intersections, this module constructs an arithmetic "tower of quotients" and collapses it bottom-up, completely bypassing modern Extended Euclidean or matrix inversion methods.

### 3. Old Russian Tradition (`/russia`)
*   **`kirik_time.py` (Fractal Chronology Engine):** Recreates the temporal system of Kirik the Novgorodian (1136 AD). It translates modern ISO timestamps into a fractal, 5-ary system of "fractional hours" down to the 5th order of magnitude (\(\sim 11\text{ms}\) accuracy), allowing for historical calculations of lunar-solar cycles exactly as performed in XII-century Novgorod.

---

## 🛠️ Installation & Academic Execution

### Clone the Repository
```bash
git clone https://github.com/ancient-core.git
cd ancient-core
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Running a Sample Module (e.g., Brahmagupta's Solver)
```python
from india.kuttaka_solver import KuttakaSolver

# Solve 137x - 60y = 1 (Ancient astronomical conjunction cycle)
solver = KuttakaSolver(a=137, b=60, c=1)
x, y = solver.solve()

print(f"Planetary Intersection Step (x): {x}")
```
### 🚀 Как развернуть окружение ICSR:

1. Скопируйте файл `requirements.txt` в корне проекта.
2. Запустите в терминале команду для сборки окружения:

```bash
pip install -r requirements.txt
```

Все библиотеки установятся автоматически, и фреймворк будет полностью готов к запуску любого из созданных модулей.

---

## 🏛️ Institutional Collaboration & Digital Humanities

This project is actively developed and maintained by the **Independent Center for Space Research (ICSR)**. 

We openly welcome partnership requests from global academic entities, including:
*   **The Institute for the History of Natural Sciences, Chinese Academy of Sciences (IHNS CAS)**
*   **Center for Digital Humanities, Peking University**
*   **The Indian National Science Academy (INSA)**
*   **International Society for the History of East Asian Science, Technology, and Medicine (ISHEASTM)**

If your institution possesses non-digitized, non-transcribed mathematical manuscripts (written in Classical Chinese *Wenyan*, Sanskrit *Shlokas*, Old Japanese *Kambun*, or Old Church Slavonic), our engineering group can assist in reverse-engineering the text into verifiable Python architectures.

---

```Consolas
┌────────────────────────────────────────────────────────────────┐
│              БЭКЛОГ ВСЕМИРНОЙ ЭТНО-МАТЕМАТИКИ                  │
├────────────────────────────────────────────────────────────────┤
│ 🇨🇳 Китай: Алхимический котел (Инь/Ян автоматы)                 │
│ 🇮🇳 Индия: Поэтический "Кромсатель" Брахмагупта                 │
│ 🇯🇵 Япония: Геометрические картины самураев Сангаку             │
│ 🌍 Майя: Модулярные шестеренки временных циклов               │
│ 𓋹 Кельты: Процедурная генерация мегалитических эллипсов        │ 
│ 🇷🇺 Русь: Пятеричное фрактальное время Кирика Новгородца        │  
│ 🦁 Африка: Топологические песчаные узоры Sona                 │
│ 🏺 Вавилон: Шестидесятеричный каскад без деления               │
│ 🦘 Аборигены: Топология брака (Группы перестановок Клейна)    │
│ 🦙 Инки: Текстильный узелковый сериализатор данных (JSON-Кипу)│
└────────────────────────────────────────────────────────────────┘
```
---
### 🦅 Подмодуль 1.3: Нарративный трехъярусный генератор одежды (Layered Navajo PCG)
*   **Концепция:** Реализация синергетического ИТ-движка, сочетающего ручной сеттинг художника и процедурную логику одномерных автоматов.
*   **Игровая механика:** Каждое сгенерированное пончо/плащ состоит из 3 независимых вычислительных зон:
    1.  *Верхняя зона (Генетика/Фракция):* Кодирует цивилизацию через стабильные геометрические паттерны (например, Wolfram Rule 90).
    2.  *Средняя зона (География/Локация):* Кодирует город или клан персонажа через направленные шевроны и фазовые сдвиги (Rule 110).
    3.  *Нижняя зона (Профессия/Ремесло):* Кодирует класс персонажа (Маг, Кузнец, Охотник) через плотность распределения текстурных шумов (Rule 30).
*   **Результат:** Художнику больше не нужно рисовать пиксели вручную. Он настраивает «генетический код» вселенной, а Python за миллисекунды собирает уникальный, говорящий прикид для каждого NPC в игре.
---
## 📜 License & Citation

This framework is open-sourced under the **MIT License**. 

If you use this code or its algorithmic definitions in your research within historical astronomy, computational linguistics, or ethnomathematics, please cite this framework as:

```text
@software{ancient_core_2026,
  author = {Independent Center for Space Research (ICSR)},
  title = {Ancient-Core: Universal Computational Framework for Ethnomathematics and Archeo-Astronomy},
  year = {2026},
  url = {[https://github.com/ancient-core](https://github.com/stdm-topological-framework/ancient-core)}
}
```
