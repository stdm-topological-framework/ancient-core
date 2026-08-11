# Модуль `america/navajo_cellular.py`

## 🦅 Историческая справка и контекст

### 📊 Общая информация

*   **Кто создатели:** Женщины-ткачихи индейского народа **Навахо (Diné)**, проживающего на юго-западе современных США. Традиция ковроткачества достигла своего пика в XVIII–XIX веках.
*   **Где применялось:** Создание священных одеял, накидок («Chief's Blankets») и ковров. Узоры несли в себе историю рода, карту местности или зашифрованные мифологические сюжеты.
*   **Суть традиции:** Ткачиха Навахо садилась за вертикальный станок без каких-либо эскизов, чертежей или разметки. Весь сложнейший фрактальный узор, состоящий из сотен вложенных ромбов, зигзагов и треугольников («глаз Навахо»), она держала в голове, создавая ковер снизу вверх, ряд за рядом.

---

## 📐 Математическая и ИТ-уникальность алгоритма

*   **Клеточные автоматы Вольфрама:** Современные исследования в области этноматематики доказали, что логика Навахо эквивалентна работе дискретных клеточных автоматов. Каждая ячейка (узел нити) нового ряда принимает решение о своем цвете (состоянии) на основе жесткого логического правила, анализируя три ячейки прямо под ней (левую, центральную и правую).
*   **Смена прикидов (Skin Generation) через побитовые правила:** В Computer Science есть 256 фундаментальных правил Клеточных автоматов. Например, знаменитое **Правило 90** (работающее на побитовом `XOR`) при одиночной начальной точке генерирует идеальный фрактальный Треугольник Серпинского. Навахо интуитивно использовали комбинации этих правил, чтобы создавать каскады вложенных ромбов.
*   **Процедурный генератор одежды (PCG):** Переводя эту логику в Python, мы получаем мощный движок. Достаточно передать коду одно число (индекс правила) и массив стартовых цветов, чтобы алгоритм мгновенно построил бесшовную текстуру ткани. Это идеальное решение для геймдева: можно генерировать бесконечное количество уникальных скинов и одежды для персонажей, тратя ноль ресурсов памяти на хранение тяжелых картинок.

```text
                      📊 СТРУКТУРА ПЛАЩА ICSR 📊
                      
       ┌───────────────────────────────────────────────────────┐
       │   ЯРУС 1 (ПЛЕЧИ): ФРАКЦИЯ / СТРАНА                    │
       │   • Правило 90 (Четкие имперские ромбы)               │
       │   • Сигнал игроку: "Этот рыцарь из Столицы"           │
       ├───────────────────────────────────────────────────────┤
       │   ЯРУС 2 (СПИНА): КЛАН / ГОРОД                        │
       │   • Правило 150 (Уникальные наклонные шевроны)        │
       │   • Сигнал игроку: "Он подчиняется северному графу"   │
       ├───────────────────────────────────────────────────────┤
       │   ЯРУС 3 (ПОДОЛ): РЕМЕСЛО / КЛАСС                     │
       │   • Правило 30 (Хаотичный плотный шум-кольчуга)       │
       │   • Сигнал игроку: "Осторожно, это тяжелый пехотинец" │
       └───────────────────────────────────────────────────────┘
```
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
