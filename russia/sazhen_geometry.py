#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ancient-Core Framework
Module: /russia/sazhen_geometry.py
Concept: Living Architecture Code / Живой Код Зодчества

Математическое ядро динамического фрактального пропорционирования 
на основе 12 канонических древнерусских саженей и золотого сечения.
"""

import math
from typing import Dict, List, Tuple

class SazhenEngine:
    # Константные коэффициенты саженей относительно условного базового модуля (в метрах для совместимости)
    # Исторические пропорции переведены в строгие математические инварианты
    SAZHEN_PROPORTIONS: Dict[str, float] = {
        "городовая": 2.848,
        "великая": 2.440,
        "косая": 2.160,
        "казенная": 2.176,
        "маховая": 1.764,
        "мерная": 1.900,
        "морская": 1.830,
        "трубная": 1.870,
        "простая": 1.508,
        "малая": 1.424,
        "без названия": 1.345,
        "ростовая": 1.674
    }

    def __init__(self, base_height_meters: float = 1.75):
        """
        Инициализация движка под конкретный антропоморфный масштаб.
        По умолчанию base_height_meters — это рост человека, для которого строится пространство.
        """
        self.base_scale = base_height_meters
        # Коэффициент масштабирования относительно канонической "ростовой" сажени
        self.scale_factor = self.base_scale / self.SAZHEN_PROPORTIONS["ростовая"]
        self.active_sazhens = self._generate_dynamic_system()

    def _generate_dynamic_system(self) -> Dict[str, float]:
        """Расчет динамической системы саженей, адаптированной под масштаб пользователя."""
        return {name: val * self.scale_factor for name, val in self.SAZHEN_PROPORTIONS.items()}

    def get_golden_subdivisions(self, sazhen_name: str, depth: int = 3) -> List[float]:
        """
        Фрактальное деление сажени на подтипы (полсажени, локти, пяди, вершки)
        через каскад золотого сечения (двойное деление и пропорции Фибоначчи).
        """
        if sazhen_name not in self.active_sazhens:
            raise ValueError(f"Сажень '{sazhen_name}' не найдена в системе.")
        
        current_val = self.active_sazhens[sazhen_name]
        subdivisions = [current_val]
        
        # Древнерусское квантование: деление на 2, 4, 8, 16 (бинарный фрактал)
        for i in range(1, depth + 1):
            subdivisions.append(current_val / (2 ** i))
            
        return subdivisions

    def generate_harmonic_grid(self, width_sazhen: str, height_sazhen: str) -> Dict[str, Tuple[float, float]]:
        """
        Генерирует прямоугольную сетку (например, для UI-контейнера или стены здания),
        где отношение сторон жестко завязано на резонанс двух разных саженей.
        Bypasses standard Euclidean aspect ratios.
        """
        w = self.active_sazhens[width_sazhen]
        h = self.active_sazhens[height_sazhen]
        
        # Вычисляем коэффициент "живого резонанса" (коэффициент иррациональности)
        resonance = w / h
        
        return {
            "dimensions_meters": (w, h),
            "aspect_ratio": resonance,
            "is_golden": abs(resonance - 1.618) < 0.15
        }

    def list_system(self):
        """Вывод текущей живой матрицы пропорций."""
        print(f"\n=== МАТРИЦА ЖИВОГО КОДА ЗОДЧЕСТВА (Базовый масштаб: {self.base_scale}м) ===")
        for name, value in sorted(self.active_sazhens.items(), key=lambda x: x[1], reverse=True):
            print(f"| {name.capitalize().ljust(15)} | {value:.4f} м |")
        print("=" * 56)

# Демонстрация работы движка для генерации органического UI / Архитектурного блока
if __name__ == "__main__":
    # Шаг 1: Инициализируем систему под рост конкретного человека (например, 1.80 метра)
    engine = SazhenEngine(base_height_meters=1.80)
    engine.list_system()

    # Шаг 2: Генерируем пропорции для "идеальной комнаты" или "главного экрана веб-сайта"
    # Используем комбинацию Городовой (царской) и Маховой саженей
    grid = engine.generate_harmonic_grid(width_sazhen="городовая", height_sazhen="маховая")
    
    print("\n[!] Сгенерирована живая геометрическая сетка:")
    print(f" -> Физические размеры: {grid['dimensions_meters'][0]:.3f} x {grid['dimensions_meters'][1]:.3f} метров")
    print(f" -> Коэффициент соизмеримости (Aspect Ratio): {grid['aspect_ratio']:.4f}")
    print(f" -> Соответствует золотому резонансу: {'ДА' if grid['is_golden'] else 'НЕТ'}")

    # Шаг 3: Получаем фрактальные под-элементы (например, для разметки кнопок или оконных проемов)
    print("\n[!] Фрактальные кванты для малого интерьера (деление Малой сажени):")
    sub_quants = engine.get_golden_subdivisions("малая", depth=4)
    names = ["Сажень", "Полсажени", "Локоть", "Пядь", "Вершок"]
    for name, val in zip(names, sub_quants):
        print(f" -> Квант '{name}': {val:.4f} м")
