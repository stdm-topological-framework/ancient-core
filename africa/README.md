## 🌍 Историческая справка и контекст модуля `sona_graphs.py`

### 📊 Общая информация

* **Создатели:** Мудрецы и старейшины народа **Чокве (Chokwe)**, а также родственных племен лучази и нгангуэла, проживающих на территории современных Анголы, Замбии и Демократической Республики Конго.
* **Область применения:** Обучение юношей в общинах, передача мифов, басен, космологических представлений и исторических хроник, а также в качестве интеллектуальных состязаний между старейшинами.
* **Суть традиции:** Традиция рисования на песке называется **Лусаона (Lusona)**, во множественном числе — **Сона (Sona)**. Рассказчик сначала очищает площадку на песке, затем быстрыми и точными движениями пальцев наносит геометрическую сетку из точек (опорных узлов). После этого он начинает вести непрерывную линию, которая огибает эти точки, создавая сложнейший симметричный узор, и одновременно рассказывает историю. Линия должна закончиться ровно в той точке, откуда началась.

### 📐 Математическая уникальность алгоритма

* **Теория графов и топология:** Рисунки Сона — это чистые **Эйлеровы пути на графах**, открытые в Европе Леонардом Эйлером только в XVIII веке при решении задачи о Кёнигсбергских мостах. Африканские математики веками использовали этот аппарат на практике.
* **Концепция зеркальных отражений:** Траектория движения пальца подчиняется жестким правилам «биллиардного шара». Линия движется под углом 45 градусов к осям сетки и зеркально отражается от невидимых внешних границ, аккуратно огибая внутренние точки.
* **Связь с теорией чисел:** Старейшины эмпирически (на практике) знали свойства **Наибольшего Общего Кратного (НОК)** и **Наибольшего Общего Делителя (НОД)**. Они знали: если размеры сетки точек $N \times M$ являются взаимно простыми числами (то есть $\gcd(N, M) = 1$), то весь сложнейший геометрический узор можно нарисовать **одной-единственной непрерывной линией**, ни разу не оторвав палец от песка и не повторив маршрут! Если числа не взаимно простые, узор распадается на несколько изолированных петель (что тоже использовалось для зашифровки сюжетов с несколькими героями).
# 🌍 Module `africa/sona_graphs.py`

## 📊 Ethnomathematical Context & Logic

*   **Origin:** The **Sona** sand-drawing tradition developed by the **Chokwe people** of Central Africa (Angola, DRC, and Zambia).
*   **The Medium:** Drawings executed in sand by tracing continuous loops around a regular grid of reference dots without lifting the finger or retracing paths.
*   **Mathematical Core:** The algorithm operates on **Number Theory** and **Topological Graphs**, acting as a discrete billiard ball simulator. The path bounces at $45^\circ$ angles relative to the bounding box of the grid nodes.

---

## 📐 Computational Matrix & GCD Mechanics

The topology of a Sona sand-graph is strictly bound by the dimensions of the internal node grid ($M \times N$):

1.  **The GCD Rule:** The number of independent intertwined loops required to completely trace a closed grid is exactly equal to the **Greatest Common Divisor** of its dimensions:
    $$\text{Required Loops} = \gcd(M, N)$$
2.  **Eulerian Path Singularity:** 
    *   If $\gcd(M, N) = 1$ (e.g., a $5 \times 4$ grid), the graph is **monocursual**. An **Eulerian path** exists (`single_loop_attainable: True`), allowing the entire pattern to be drawn with one single continuous line.
    *   If $\gcd(M, N) > 1$ (e.g., a $6 \times 4$ grid, where $\gcd = 2$), a traditional single Eulerian path is **impossible** (`single_loop_attainable: False`). The system dynamically handles this by generating multiple interleaved, perfectly symmetrical independent loops.

---

## 🎮 Game Engine & PCG Integration (Use Cases)

For game developers, the `sona_graphs.py` core serves as an automated mathematical backend for:
*   **Dynamic Rune Generators:** Procedurally creating distinct geometric pattern overlays for armor and weapon slots based on item level matrices.
*   **Multi-Agent Puzzle Mechanics:** Designing topological connection puzzles where the player must deploy multiple synchronous energy rays (equal to $\gcd(M, N)$) to power up ancient artifacts.
