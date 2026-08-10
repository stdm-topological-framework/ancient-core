import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict

class SonaGraphEngine:
    """
    Вычислительный движок африканской песчаной геометрии 'Сона' (Народ Чокве, Ангола).
    Генерирует непрерывные Эйлеровы пути вокруг сетки точек на основе теории чисел.
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows  # Количество строк в сетке точек
        self.cols = cols  # Количество столбцов в сетке точек
        self.gcd = math.gcd(rows, cols)
        
    def get_academic_report(self) -> Dict[str, any]:
        """ Возвращает теоретико-числовой анализ топологии сетки """
        is_eulerian = (self.gcd == 1)
        return {
            "grid_dimensions": f"{self.rows}x{self.cols}",
            "greatest_common_divisor (НОД)": self.gcd,
            "single_loop_attainable (Эйлеров путь одной линией)": is_eulerian,
            "required_independent_loops (Всего изолированных петель)": self.gcd,
            "total_internal_dots": self.rows * self.cols
        }

    def generate_trace(self, start_loop_idx: int = 0) -> List[Tuple[float, float]]:
        """
        Моделирует движение пальца по песку под углом 45 градусов.
        Работает по физическому алгоритму 'биллиардного шара' в замкнутом пространстве.
        """
        # Масштабируем границы виртуального песчаного поля
        # Точки сетки будут находиться в полуцелых координатах (0.5, 1.5...)
        width = self.cols
        height = self.rows
        
        # Начальная точка траектории на границе (смещение зависит от индекса петли)
        x, y = 0.0, float(start_loop_idx)
        dx, dy = 1.0, 1.0  # Направление движения (45 градусов)
        
        path = [(x, y)]
        visited_states = set()
        
        # Шаг движения пальца (дискретный шаг)
        step = 0.5
        
        while True:
            # Запоминаем текущее состояние для предотвращения бесконечного цикла
            state = (x, y, dx, dy)
            if state in visited_states and len(path) > 1:
                break
            visited_states.add(state)
            
            # Просчитываем следующий шаг
            next_x = x + dx * step
            next_y = y + dy * step
            
            # Алгоритм зеркального отражения от внешних границ песчаного поля
            if next_x <= 0 or next_x >= width:
                dx = -dx
            if next_y <= 0 or next_y >= height:
                dy = -dy
                
            x += dx * step
            y += dy * step
            path.append((x, y))
            
            # Если вернулись в исходную точку с исходным направлением — петля замкнулась
            if abs(x - path[0][0]) < 1e-5 and abs(y - path[0][1]) < 1e-5 and dx == 1.0 and dy == 1.0:
                break
                
        return path

    def render_on_sand(self):
        """ Визуализирует африканский рисунок Сона на цифровом 'песке' """
        plt.figure(figsize=(self.cols + 2, self.rows + 2))
        
        # Задаем 'песочный' цвет фона
        ax = plt.gca()
        ax.set_facecolor('#E6C280')
        
        # Наносим сетку опорных точек Чокве
        dot_x, dot_y = np.meshgrid(np.arange(0.5, self.cols, 1), np.arange(0.5, self.rows, 1))
        plt.scatter(dot_x, dot_y, color='#4A3B22', s=120, zorder=5, label="Опорные узлы (Точки)")
        
        # Генерируем и рисуем петли траектории
        # Если НОД = 1, выполнится ровно один раз (одна непрерывная нить)
        colors = ['#8B0000', '#006400', '#00008B', '#FF8C00', '#4B0082']
        
        for loop_idx in range(self.gcd):
            path = self.generate_trace(start_loop_idx=loop_idx)
            px, py = zip(*path)
            
            color = colors[loop_idx % len(colors)]
            plt.plot(px, py, color=color, linewidth=3, zorder=3, 
                     label=f"Линия Сона (Петля {loop_idx + 1})")
            
            # Отмечаем точку старта
            plt.scatter(px[0], py[0], color='white', edgecolor='black', s=150, marker='*', zorder=6)

        report = self.get_academic_report()
        title_str = f"Африканская топология Сона ({report['grid_dimensions']})\n"
        title_str += f"НОД: {report['greatest_common_divisor (НОД)']}. Эйлеров путь: {'ДА' if report['single_loop_attainable (Эйлеров путь одной линией)'] else 'НЕТ'}"
        
        plt.title(title_str, fontsize=14, color='#4A3B22', fontweight='bold')
        plt.xlim(-0.5, self.cols + 0.5)
        plt.ylim(-0.5, self.rows + 0.5)
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        
        # Убираем дубликаты в легенде
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc='upper right')
        
        print(f"[+] Движок ICSR: Граф Сона сгенерирован успешно.")
        plt.show()

# === СТЕНДОВЫЕ ИСПЫТАНИЯ АФРИКАНСКОГО МОДУЛЯ ===
if __name__ == "__main__":
    print("================================================================")
    # Испытание 1: Взаимно простые числа (Идеальный Эйлеров путь одной линией)
    print("[Тест 1] Запуск идеальной сетки 5x4 (Взаимно простые, НОД = 1)...")
    sona_perfect = SonaGraphEngine(rows=5, cols=4)
    print(sona_perfect.get_academic_report())
    # Скрипт откроет окно визуализации (разверните его на компьютере)
    sona_perfect.render_on_sand()
    
    print("\n----------------------------------------------------------------")
    # Испытание 2: Нерегулярная сетка (Разделение на изолированные графы)
    print("[Тест 2] Запуск сложной сетки 6x4 (НОД = 2, узор из двух петел)...")
    sona_complex = SonaGraphEngine(rows=6, cols=4)
    print(sona_complex.get_academic_report())
    sona_complex.render_on_sand()
    print("================================================================")
