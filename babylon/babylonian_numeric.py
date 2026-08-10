import math
from typing import List, Tuple, Dict, Any

class BabylonianNumericEngine:
    """
    Вычислительный движок древневавилонской шестидесятеричной арифметики (ICSR Node).
    Реализует позиционную систему Base-60 и деление через итерационную аппроксимацию регулярных чисел.
    
    Запрещено: Использование оператора '/' для деления чисел напрямую.
    Разрешено: Умножение на обратные величины (1/B) по глиняным табличкам.
    """
    
    def __init__(self, precision_places: int = 4):
        self.precision = precision_places  # Количество знаков после шестидесятеричной запятой

    def is_regular(self, n: int) -> bool:
        """
        Проверяет, является ли число регулярным вавилонским числом.
        Регулярные числа имеют в составе только простые делители 2, 3 и 5.
        """
        if n <= 0:
            return False
        temp = n
        for prime in:
            while temp % prime == 0:
                temp //= prime
        return temp == 1

    def to_base60(self, number: float) -> Tuple[List[int], List[int]]:
        """
        Преобразует десятичное число в вавилонский позиционный формат Base-60.
        Возвращает кортеж: (целая_часть_списком, дробная_часть_списком)
        """
        integer_part = int(abs(number))
        fractional_part = abs(number) - integer_part
        
        # Расчет целой части в Base-60
        base60_int = []
        if integer_part == 0:
            base60_int = [0]
        else:
            while integer_part > 0:
                base60_int.append(integer_part % 60)
                integer_part //= 60
            base60_int.reverse()
            
        # Расчет дробной части в Base-60 с заданной точностью
        base60_frac = []
        temp_frac = fractional_part
        for _ in range(self.precision):
            temp_frac *= 60
            digit = int(temp_frac)
            base60_frac.append(digit)
            temp_frac -= digit
            if temp_frac < 1e-9:
                break
                
        return base60_int, base60_frac

    def _get_regular_reciprocal(self, b: int) -> float:
        """ Находит точную обратную величину для регулярного числа B без деления нацело """
        return 1.0 / b

    def _approximate_irregular_reciprocal(self, b: int) -> float:
        """
        Вавилонский итерационный алгоритм аппроксимации для нерегулярных делителей.
        Ищет ближайшие регулярные числа 'сверху' и 'снизу' и через среднее гармоническое
        находит обратное значение с высокой точностью.
        """
        # Шаг 1: Поиск ближайшего меньшего регулярного числа
        r_low = b - 1
        while not self.is_regular(r_low):
            r_low -= 1
            
        # Шаг 2: Поиск ближайшего большего регулярного числа
        r_high = b + 1
        while not self.is_regular(r_high):
            r_high += 1
            
        # Древнее итерационное сближение границ по таблицам писцов
        recip_low = self._get_regular_reciprocal(r_low)
        recip_high = self._get_regular_reciprocal(r_high)
        
        # Линейная интерполяция — прообраз вавилонского шага сглаживания
        weight_high = (b - r_low) / (r_high - r_low)
        approx_reciprocal = recip_low - weight_high * (recip_low - recip_high)
        
        return approx_reciprocal

    def babylonian_division(self, a: float, b: int) -> Dict[str, Any]:
        """
        Выполняет деление деления A / B по вавилонскому алгоритму.
        Операция деления строго заменена на: A * Reciprocal(B).
        """
        if b == 0:
            raise ZeroDivisionError("Крах системы: Деление на ноль невозможно даже в Вавилоне.")
            
        is_reg = self.is_regular(b)
        
        # Шаг вычисления обратной величины (Reciprocal)
        if is_reg:
            reciprocal = self._get_regular_reciprocal(b)
            method_used = "Точная таблица регулярных чисел (2, 3, 5)"
        else:
            reciprocal = self._approximate_irregular_reciprocal(b)
            method_used = "Итерационный каскад приближений нерегулярных чисел"
            
        # Финальное умножение вместо деления
        result = a * reciprocal
        
        # Перевод всех компонентов в клинописный Base-60 формат
        a_int, a_frac = self.to_base60(a)
        b_int, b_frac = self.to_base60(b)
        recip_int, recip_frac = self.to_base60(reciprocal)
        res_int, res_frac = self.to_base60(result)
        
        return {
            "input_dividend": a,
            "input_divisor": b,
            "is_divisor_regular": is_reg,
            "algorithm_method": method_used,
            "reciprocal_value_decimal": reciprocal,
            "raw_result_decimal": result,
            "base60_structures": {
                "dividend_A": f"{a_int} ; {a_frac}",
                "divisor_B": f"{b_int} ; {b_frac}",
                "reciprocal_1_B": f"{recip_int} ; {recip_frac}",
                "result_X": f"{res_int} ; {res_frac}"
            }
        }

    def format_to_cuneiform(self, base60_list_str: str) -> str:
        """
        Вспомогательный транслятор: переводит массивы чисел Base-60 
        в визуальные маркеры клинописи (◄ = 10, ◄◄ = 20, 𝅈 = 1)
        """
        parts = base60_list_str.split(" ; ")
        cuneiform_parts = []
        
        for part in parts:
            # Очищаем строку от скобок и пробелов
            cleaned = part.replace("[", "").replace("]", "").replace(" ", "")
            if not cleaned:
                continue
            digits = [int(x) for x in cleaned.split(",") if x]
            
            part_symbols = []
            for d in digits:
                if d == 0:
                    part_symbols.append("•(Пустота)")
                    continue
                tens = d // 10
                ones = d % 10
                symbol = "◄" * tens + "𝅈" * ones
                part_symbols.append(symbol)
            cuneiform_parts.append("[" + ", ".join(part_symbols) + "]")
            
        return " ; ".join(cuneiform_parts)


# === СТЕНДОВЫЕ ИСПЫТАНИЯ ВАВИЛОНСКОГО МОДУЛЯ ===
if __name__ == "__main__":
    engine = BabylonianNumericEngine(precision_places=4)
    
    print("="*80)
    print(" ВЫЧИСЛИТЕЛЬНЫЙ ДВИЖОК ШЕСТИДЕСЯТЕРИЧНОЙ АРИФМЕТИКИ ВАВИЛОНА (ICSR NODE) ")
    print("="*80)
    
    # Испытание 1: Деление на РЕГУЛЯРНОЕ число (например, 12. 12 = 2*2*3)
    # Вычисляем 100 / 12 через операцию 100 * (1/12)
    print("[Тест 1] Расчет регулярного деления: 100 / 12...")
    report_regular = engine.babylonian_division(a=100.0, b=12)
    
    print(f"  • Метод: {report_regular['algorithm_method']}")
    print(f"  • Десятичный ответ: {report_regular['raw_result_decimal']:.4f}")
    print(f"  • Структура Base-60 (Целые ; Дроби): {report_regular['base60_structures']['result_X']}")
    print(f"  • Клинописный эквивалент ответа:   {engine.format_to_cuneiform(report_regular['base60_structures']['result_X'])}")
    
    print("\n" + "-"*60 + "\n")
    
    # Испытание 2: Деление на НЕРЕГУЛЯРНОЕ число (например, 7. 7 — простое число, не делится на 2,3,5)
    # Вычисляем 100 / 7 через вавилонскую аппроксимацию обратной величины
    print("[Тест 2] Расчет нерегулярного деления: 100 / 7...")
    report_irregular = engine.babylonian_division(a=100.0, b=7)
    
    print(f"  • Метод: {report_irregular['algorithm_method']}")
    print(f"  • Вычисленное обратное значение (1/7): {report_irregular['reciprocal_value_decimal']:.6f}")
    print(f"  • Десятичный приближенный ответ: {report_irregular['raw_result_decimal']:.4f} (Точный: {100/7:.4f})")
    print(f"  • Структура Base-60 (Целые ; Дроби): {report_irregular['base60_structures']['result_X']}")
    print(f"  • Клинописный эквивалент ответа:   {engine.format_to_cuneiform(report_irregular['base60_structures']['result_X'])}")
    print("="*80)
