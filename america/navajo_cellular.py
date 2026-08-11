import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any

class NavajoCellularEngine:
    """
    Процедурный фрактальный движок ткачества Навахо (ICSR Node).
    Генерирует текстуры одежды и геометрические орнаменты на базе клеточных автоматов.
    
    Применяется для процедурной генерации игровых скинов (PCG) и текстур тканей.
    """
    def __init__(self, width: int = 101, height: int = 60):
        self.width = width if width % 2 != 0 else width + 1  # Ширина ковра (лучше нечетная для симметрии)
        self.height = height                                 # Длина (количество рядов ткачества)
        self.grid = np.zeros((self.height, self.width), dtype=int)

    def _get_wolfram_rule_map(self, rule_number: int) -> Dict[Tuple[int, int, int], int]:
        """
        Преобразует индекс правила (0-255) в бинарную маску переходов для трех соседних клеток.
        Это чистый цифровой аналог логики, которую ткачиха Навахо держала в уме.
        """
        if not (0 <= rule_number <= 255):
            raise ValueError("Индекс правила Вольфрама должен быть в диапазоне от 0 до 255")
            
        # Переводим число в 8-битную строку (например, 90 -> '01011010')
        binary_rule = f"{rule_number:08b}"
        
        # Карта состояний для трех нижних клеток: (Левая, Центральная, Правая)
        states = [
            (1, 1, 1), (1, 1, 0), (1, 0, 1), (1, 0, 0),
            (0, 1, 1), (0, 1, 0), (0, 0, 1), (0, 0, 0)
        ]
        
        # Маппим биты правила к состояниям (разворачиваем, так как биты идут справа налево)
        return {states[i]: int(binary_rule[i]) for i in range(8)}

    def generate_poncho_texture(self, rule_number: int = 90, custom_center_seed: bool = True) -> np.ndarray:
        """
        Пошагово ткет полотно снизу вверх. Каждый новый ряд вычисляется на основе
        булевой маски предыдущего ряда по правилам Навахо.
        """
        self.grid = np.zeros((self.height, self.width), dtype=int)
        
        # Шаг 1: Задаем начальные условия (первая нить на станке)
        if custom_center_seed:
            # Одна активная точка в центре — дает чистый фрактальный треугольник/ромб
            self.grid[0, self.width // 2] = 1
        else:
            # Случайные нити — дают сложную шумовую текстуру одежды
            self.grid[0] = np.random.randint(0, 2, self.width)
            
        # Получаем логическую маску переходов
        rule_map = self._get_wolfram_rule_map(rule_number)
        
        # Шаг 2: Итерационный каскад ткачества
        for r in range(1, self.height):
            for c in range(self.width):
                # Находим индексы соседей с учетом циклических граничных условий (чтобы узор был бесшовным!)
                left = self.grid[r-1, (c - 1) % self.width]
                center = self.grid[r-1, c]
                right = self.grid[r-1, (c + 1) % self.width]
                
                # Вычисляем цвет новой клетки
                self.grid[r, c] = rule_map[(left, center, right)]
                
        return self.grid

    def render_preview(self, rule_number: int, palette_name: str = "Navajo_Traditional"):
        """ Визуализирует узор ткани и выводит отчет для геймдева """
        plt.figure(figsize=(10, 6))
        
        # Традиционные цветовые палитры Навахо
        palettes = {
            "Navajo_Traditional": ['#F5F5DC', '#C0392B'], # Бежевый и терракотовый (природные красители)
            "Navajo_Night": ['#1A252F', '#F1C40F'],        # Угольно-черный и священный желтый
            "Navajo_Ghost": ['#BDC3C7', '#2C3E50']         # Призрачный серый и глубокий синий (для брони)
        }
        
        selected_colors = palettes.get(palette_name, palettes["Navajo_Traditional"])
        cmap = plt.cm.colors.ListedColormap(selected_colors)
        
        # Отображаем матрицу клеточного автомата
        plt.imshow(self.grid, cmap=cmap, origin='lower', interpolation='nearest')
        
        # Стилизация под игровой интерфейс генерации скинов
        title_str = f"ПРОЦЕДУРНЫЙ ГЕНЕРАТОР ОДЕЖДЫ НАВАХО (ICSR PCG NODE)\n"
        title_str += f"Текстура: Ковер/Пончо | Правило Вольфрама: #{rule_number} | Палитра: {palette_name}"
        plt.title(title_str, fontsize=12, color='#2C3E50', fontweight='bold', pad=15)
        
        plt.xlabel("Ширина полотна (Индексы нитей)", fontsize=10)
        plt.ylabel("Ряды ткачества (Временные шаги автомата)", fontsize=10)
        plt.grid(False)
        
        # Добавляем текстовое клеймо
        plt.text(2, 2, "ASSET TYPE: PROCEDURAL SKIN", fontsize=9, color=selected_colors[1], weight='bold', bbox=dict(facecolor='white', alpha=0.7))
        
        print(f"[+] Движок ICSR: Текстура Навахо для правила #{rule_number} успешно сгенерирована.")
        plt.show()


# === СТЕНДОВЫЕ ИСПЫТАНИЯ ИГРОВОГО ДВИЖКА НАВАХО ===
if __name__ == "__main__":
    # Создаем холст для генерации одежды размером 121 на 70 ячеек
    engine = NavajoCellularEngine(width=121, height=70)
    
    # Испытание 1: Классический фрактальный ромбовидный узор Навахо (Правило 90 - Чистый XOR)
    # Идеально подходит для создания пончо главного героя
    print("[Тест 1] Генерация фрактального скина 'Пончо Вождя' (Правило 90)...")
    engine.generate_poncho_texture(rule_number=90, custom_center_seed=True)
    engine.render_preview(rule_number=90, palette_name="Navajo_Traditional")
    
    # Испытание 2: Плотная шевронная броня (Правило 30 - Хаотичный узор)
    # Используем случайный старт для создания уникальной неповторимой текстуры ткани
    print("\n[Тест 2] Генерация хаотичной текстуры ткани 'Священная Ночь' (Правило 30)...")
    engine.generate_poncho_texture(rule_number=30, custom_center_seed=False)
    engine.render_preview(rule_number=30, palette_name="Navajo_Night")
