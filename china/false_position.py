#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ancient-Core Framework
Module: /china/false_position.py
Method: Ying Bu Zu Shu (盈不足术) / Метод ложного положения

Древнекитайский итерационный алгоритм нахождения корней нелинейных уравнений 
путем анализа избытка (盈) и недостатка (不足) без использования производных.
"""

from typing import Callable, Dict, Any

class YingBuZuSolver:
    @staticmethod
    def solve(func: Callable[[float], float], guess1: float, guess2: float, tolerance: float = 1e-6, max_iter: int = 20) -> Dict[str, Any]:
        """
        Решение нелинейного уравнения f(x) = 0 по правилу 'взаимного умножения крест-накрест'.
        Bypasses Newton-Raphson calculus.
        """
        x1, x2 = guess1, guess2
        
        for iteration in range(1, max_iter + 1):
            y1 = func(x1)
            y2 = func(x2)
            
            # Если знаки одинаковые, метод ложного положения в базовом каноне требует корректировки диапазона
            if y1 * y2 > 0:
                # Адаптивный сдвиг границ по китайскому правилу смещения
                x2 = x2 + (x2 - x1)
                continue
                
            # y1 и y2 выступают как физические величины избытка/недостатка (Ying / Bu Zu)
            # Применяем каноническую формулу Суаньпань (счетной доски)
            denominator = abs(y2) + abs(y1)
            if denominator == 0:
                break
                
            # Формула перекрестного умножения
            x_next = (x1 * abs(y2) + x2 * abs(y1)) / denominator
            y_next = func(x_next)
            
            if abs(y_next) < tolerance:
                return {
                    "root": x_next,
                    "iterations": iteration,
                    "status": "SUCCESS",
                    "residual": y_next
                }
                
            # Сдвиг границ для следующей итерации
            if y_next * y1 < 0:
                x2 = x_next
            else:
                x1 = x_next
                
        return {"status": "MAX_ITER_REACHED", "last_approx": x_next}

if __name__ == "__main__":
    # Тест: найдем корень кубического уравнения из трактатов Лю Хуэя: x^3 - 2 = 0
    # Точный корень: кубический корень из 2 ~= 1.259921
    equation = lambda x: x**3 - 2
    
    solver = YingBuZuSolver()
    result = solver.solve(equation, guess1=1.0, guess2=2.0)
    
    print("\n☯️ === СУАНЬПАНЬ-СОЛВЕР ИНЬ БУ ЦЗУ ШУ ===")
    print(f" -> Статус вычислений: {result['status']}")
    print(f" -> Найденный корень:   {result['root']:.6f}")
    print(f" -> Итераций затрачено: {result['iterations']}")
    print(f" -> Остаточная ошибка:  {result['residual']:.8e}")
    print("=========================================\n")
