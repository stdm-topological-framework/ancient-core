import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict, Any

class SangakuGeometryEngine:
    """
    Вычислительный геометрический движок традиционной японской математики Васан (ICSR Node).
    Генерирует самурайские храмовые картины 'Сангаку' на основе касающихся окружностей.
    
    ПРАВИЛО ВАСАН: Использование тригонометрии (sin, cos, tan, радианы, градусы) КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО.
    Вычисления производятся только через алгебраические соотношения радиусов и теорему Пифагора.
    """
    
    def __init__(self, outer_radius: float = 10.0):
        self.R = outer_radius  # Радиус большого внешнего кольца-контейнера
        self.circles: List[Dict[str, Any]] = []

    def generate_soddy_chain(self, depth: int = 5):
        """
        Рекурсивный алгоритм расчета цепочки касающихся кругов внутри внешнего кольца R.
        Использует формулу кривизны Декарта-Содди, адаптированную под методы школы Васан.
        Кривизна (k) = 1 / radius. Внешнее кольцо имеет отрицательную кривизну.
        """
        self.circles = []
        
        # 1. Внешнее кольцо-контейнер (Кривизна k0)
        k0 = -1.0 / self.R
        
        # 2. Два первых внутренних симметричных круга (заполняют половину пространства)
        # Радиус первых двух кругов равен ровно половине внешнего
        r1 = self.R / 2.0
        k1 = 1.0 / r1
        k2 = 1.0 / r1
        
        # Добавляем базовые круги
        # Координаты (x, y) находятся через чистую алгебру пропорций
        self.circles.append({"x": 0.0, "y": 0.0, "r": self.R, "label": "Внешнее кольцо (Дай-эн)"})
        self.circles.append({"x": -r1, "y": 0.0, "r": r1, "label": "Первый внутренний круг"})
        self.circles.append({"x": r1, "y": 0.0, "r": r1, "label": "Второй внутренний круг"})
        
        # 3. Каскадное вычисление уменьшающихся кругов (Цепочка Сангаку)
        # Математика Васан: k_next = k1 + k2 + k0 + 2 * sqrt(k1*k2 + k2*k0 + k0*k1)
        # Для расчета координат центров (y) используется теорема Пифагора для треугольников касания
        
        last_k = k1
        last_r = r1
        current_y_offset = 0.0
        
        for i in range(1, depth + 1):
            # Самурайская формула шага кривизны для симметричного случая:
            # k_next = 2*last_k - k0 + 2 * sqrt(last_k^2 - 2*last_k*k0) -- адаптировано для оптимизации
            inner_term = last_k * last_k + 2 * last_k * abs(k0)
            k_next = last_k + abs(k0) + 2 * math.sqrt(abs(inner_term))
            
            r_next = 1.0 / k_next
            
            # Нахождение координаты Y центра круга через чистый Пифагор:
            # (R - r_next)^2 = x^2 + y^2, где x = 0 (круги идут строго по вертикальной оси симметрии)
            # Следовательно: y = sqrt((R - r_next)^2 - 0) = R - r_next
            y_next = self.R - r_next
            
            # Добавляем верхний и нижний зеркальные круги цепочки
            self.circles.append({"x": 0.0, "y": y_next, "r": r_next, "label": f"Цепь Сё-эн, ярус {i} (Верх)"})
            self.circles.append({"x": 0.0, "y": -y_next, "r": r_next, "label": f"Цепь Сё-эн, ярус {i} (Ниж)"})
            
            # Переходим к следующей итерации каскада
            last_k = k_next
            last_r = r_next

    def render_wooden_tablet(self):
        """ Отрисовывает геометрию Сангаку в стиле традиционной деревянной дощечки храма Эдо """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Текстурирование под древнее лакированное дерево
        ax.set_facecolor('#D2B48C')  # Цвет выцветшей древесины суги (японский кедр)
        
        # Отрисовка всех рассчитанных кругов самурайской цепи
        # Первым рисуем внешнее кольцо
        outer = self.circles[0]
        outer_circle = plt.Circle((outer["x"], outer["y"]), outer["r"], 
                                  facecolor='#C0392B', edgecolor='#4A2711', linewidth=4, zorder=1)
        ax.add_patch(outer_circle)
        
        # Рисуем первые два больших внутренних круга (Традиционно красим в контрастный цвет)
        for c in self.circles[1:3]:
            circle_patch = plt.Circle((c["x"], c["y"]), c["r"], 
                                      facecolor='#34495E', edgecolor='#1A252F', linewidth=2, zorder=2)
            ax.add_patch(circle_patch)
            
        # Рисуем бесконечную каскадную цепочку мелких кругов
        colors_chain = ['#F1C40F', '#E67E22', '#9B59B6', '#1ABC9C', '#2ECC71']
        for idx, c in enumerate(self.circles[3:]):
            color = colors_chain[(idx // 2) % len(colors_chain)]
            circle_patch = plt.Circle((c["x"], c["y"]), c["r"], 
                                      facecolor=color, edgecolor='#2C3E50', linewidth=1.5, zorder=3)
            ax.add_patch(circle_patch)

        # Стилизация под храмовую вывеску
        title_text = "算額 — ТАБЛИЦА САНГАКУ ЭПОХИ ЭДО\n"
        title_text += "Каскад вписанных кругов Содди методами геометрии Васан (Без тригонометрии)"
        plt.title(title_text, fontsize=12, family='serif', color='#4A2711', weight='bold', pad=15)
        
        # Настройка осей и границ графического холста
        limit = self.R * 1.1
        plt.xlim(-limit, limit)
        plt.ylim(-limit, limit)
        plt.grid(False)
        ax.set_aspect('equal')
        
        # Убираем системные деления линеек (В храмах не было декартовых сеток)
        plt.xticks([])
        plt.yticks([])
        
        # Текстовое художественное клеймо на деревянной плашке
        ax.text(-self.R*1.0, -self.R*1.0, "独立宇宙研究所 (ICSR Node)", 
                fontsize=10, color='#4A2711', style='italic', weight='bold')

        print(f"[+] Движок ICSR: Самурайская табличка Сангаку успешно визуализирована.")
        plt.show()


# === СТЕНДОВЫЕ ИСПЫТАНИЯ ЯПОНСКОГО ГЕОМЕТРИЧЕСКОГО МОДУЛЯ ===
if __name__ == "__main__":
    # Инициализируем движок Сангаку с внешним радиусом кольца 12 единиц
    sangaku = SangakuGeometryEngine(outer_radius=12.0)
    
    # Запускаем рекурсивный расчет самурайской цепи кругов на глубину 5 ярусов
    # Всего алгоритм рассчитает и свяжет между собой 13 окружностей
    sangaku.generate_soddy_chain(depth=5)
    
    # Выводим математический отчет по координатам центров некоторых кругов
    print("📍 Технологическая карта центров окружностей (Васан-каскад):")
    for i, circle in enumerate(sangaku.circles[:6]):
        print(f"  • {circle['label']}: Центр = ({circle['x']:.2f}, {circle['y']:.2f}), Радиус = {circle['r']:.4f}")
        
    # Запускаем отрисовку цифровой деревянной дощечки
    sangaku.render_wooden_tablet()
