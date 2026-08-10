import datetime
from typing import Dict, Tuple

class KirikTimeEngine:
    """
    Вычислительный движок фрактального времени Кирика Новгородца (1136 г.).
    Переводит современное системное время в древнерусские пятеричные дробные доли часа.
    
    Математическая основа:
    - 1 сутки = 24 часа (12 дневных, 12 ночных)
    - 1 час = 5 'часцев' (1-й порядок)
    - 1 часец = 5 долей 2-го порядка
    - ...
    - 1 час = 5^5 = 3125 'дробь пятая' (минимальная базовая единица счета Кирика)
    - 1 сутки = 24 * 3125 = 75,000 минимальных фрактальных долей.
    """
    
    # Константы пятеричного деления по Кирику Новгородцу
    FRACTION_BASE = 5
    MAX_ORDER = 5  # Трактат подробно описывает деление до 5-го порядка ("дробь пятая")
    TOTAL_SHARES_PER_HOUR = 3125  # 5^5
    TOTAL_SHARES_PER_DAY = 75000  # 24 * 3125
    
    def __init__(self):
        # Названия порядков долей на древнерусском языке
        self.order_names = {
            1: "Часцы (1-й порядок)",
            2: "Вторые дроби",
            3: "Третьи дроби",
            4: "Четвертые дроби",
            5: "Пятые дроби (Микро-доли Кирика)"
        }

    def from_datetime(self, dt: datetime.datetime) -> Dict[str, any]:
        """
        Преобразует объект datetime в структуру фрактального времени Кирика.
        """
        # Считаем, сколько секунд прошло с начала текущих суток
        seconds_since_midnight = (dt.hour * 3600) + (dt.minute * 60) + dt.second + (dt.microsecond / 1_000_000)
        
        # Переводим общие секунды суток в микро-доли Кирика (75000 долей в 86400 секундах)
        # Одна доля Кирика = 86400 / 75000 = 1.152 секунды
        total_kirik_shares = int((seconds_since_midnight / 86400) * self.TOTAL_SHARES_PER_DAY)
        
        # Вычисляем текущий древнерусский час (от 0 до 23)
        kirik_hour = total_kirik_shares // self.TOTAL_SHARES_PER_HOUR
        remainder_shares = total_kirik_shares % self.TOTAL_SHARES_PER_HOUR
        
        # Разворачиваем остаток часа в каскад пятеричных фрактальных долей
        fractions = {}
        temp_shares = remainder_shares
        
        # Пошагово извлекаем коэффициенты пятеричной системы счисления
        for order in range(self.MAX_ORDER, 0, -1):
            weight = self.FRACTION_BASE ** (order - 1)
            val = temp_shares // weight
            fractions[order] = val
            temp_shares %= weight
            
        return {
            "civil_time": dt.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "ancient_hour": kirik_hour,
            "total_day_shares": total_kirik_shares,
            "fractal_cascade": {self.order_names[k]: v for k, v in sorted(fractions.items())}
        }

    def to_standard_time(self, hour: int, cascade: Tuple[int, int, int, int, int]) -> str:
        """
        Обратный расчет: собирает стандартное время из часа и пятеричного каскада долей.
        cascade: кортеж из 5 элементов (часцы, 2-я, 3-я, 4-я, 5-я дробь)
        """
        if not (0 <= hour < 24):
            raise ValueError("Час должен быть в диапазоне от 0 до 23")
            
        # Проверяем, что все доли находятся в рамках пятеричной логики (0-4)
        for i, val in enumerate(cascade):
            if not (0 <= val < 5):
                raise ValueError(f"Доля порядка {i+1} выходит за рамки пятеричной логики (значение: {val})")

        # Вычисляем сумму долей внутри часа
        hour_shares = 0
        for i, val in enumerate(cascade):
            order = i + 1
            weight = self.FRACTION_BASE ** (self.MAX_ORDER - order)
            hour_shares += val * weight
            
        # Общее количество долей с начала суток
        total_shares = (hour * self.TOTAL_SHARES_PER_HOUR) + hour_shares
        
        # Переводим доли обратно в секунды суток
        total_seconds = (total_shares / self.TOTAL_SHARES_PER_DAY) * 86400
        
        # Форматируем в строку времени
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = int(total_seconds % 60)
        ms = int((total_seconds % 1) * 1000)
        
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


# === ДЕМОНСТРАЦИЯ И СТЕНДОВЫЕ ИСПЫТАНИЯ ===
if __name__ == "__main__":
    engine = KirikTimeEngine()
    
    print("================================================================")
    print(" ДВИЖОК ФРАКТАЛЬНОГО ВРЕМЕНИ КИРИКА НОВГОРОДЦА (ICSR NODE)      ")
    print("================================================================")
    
    # Тест 1: Перевод текущего времени
    now = datetime.datetime.now()
    kirik_data = engine.from_datetime(now)
    
    print(f"\n[+] Системное время: {kirik_data['civil_time']}")
    print(f"[+] Древнерусский час суток: {kirik_data['ancient_hour']}")
    print(f"[+] Общее число микро-долей с полуночи: {kirik_data['total_day_shares']} / 75000")
    print("\nФрактальный каскад часа по Кирику (система основания 5):")
    for name, val in kirik_data['fractal_cascade'].items():
        print(f"  • {name}: {val}")
        
    # Тест 2: Реконструкция времени по летописи
    # Допустим, в летописи указан 14-й час суток, 2 часца, 4 вторых дроби, 1 третья, 0 четвертых, 3 пятых.
    test_cascade = (2, 4, 1, 0, 3)
    restored_time = engine.to_standard_time(hour=14, cascade=test_cascade)
    
    print("\n[+] Обратный расчет исторической хронологии:")
    print(f"  Входные данные рукописи: 14-й час, каскад долей {test_cascade}")
    print(f"  Реконструированное современное время: {restored_time}")
    print("================================================================")
