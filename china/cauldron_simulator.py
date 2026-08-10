import time

class AlchemyCauldron:
    def __init__(self, lead_yang: float, mercury_yin: float):
        self.yang = lead_yang  # Свинец (активная сила)
        self.yin = mercury_yin   # Ртуть (пассивная субстанция)
        self.temperature = 20.0  # Начальная температура котла
        self.elixir_ready = False
        self.exploded = False

    def get_hexagram_force(self, hour: int) -> float:
        """
        Древнее правило: в первые 6 часов дня растет Ян (сила 1.5).
        В следующие 6 часов дня растет Инь (сила 0.5).
        """
        if 1 <= hour <= 6:
            return 1.5  # Растущий Ян (время раздувать огонь)
        elif 7 <= hour <= 12:
            return 0.5  # Растущий Инь (время охлаждать)
        return 1.0

    def heat_cycle(self, hour: int, bellows_strokes: int):
        """ Один шаг (оборот) нагревания котла """
        if self.exploded:
            print("Котел уже взорван. Соберите осколки.")
            return

        # Расчет влияния времени (гексаграммы) и действий алхимика (меха раздувания)
        force = self.get_hexagram_force(hour)
        heat_impulse = bellows_strokes * force
        
        # Физика котелка по даосским правилам
        self.temperature += heat_impulse * 2.5
        
        # Изменение пропорций Инь и Ян под действием жара
        self.yang -= (self.temperature * 0.01)
        self.yin += (self.temperature * 0.005) * force

        print(f"--- Час {hour}-й ---")
        print(f"Температура: {self.temperature:.1f}°C")
        print(f"Баланс элементов -> Свинец (Ян): {self.yang:.2f} | Ртуть (Инь): {self.yin:.2f}")

        # Проверка критических условий (границы алгоритма)
        if self.temperature > 300:
            self.exploded = True
            print("💥 БУМ! Котел перегрелся и взорвался! Алхимик остался без бровей.")
            return

        if self.yang <= 0:
            print("💨 Свинец полностью испарился. Пилюля превратилась в пепел.")
            return

        # Условие идеального золотого сечения Инь-Ян
        if 100 <= self.temperature <= 150 and abs(self.yang - self.yin) < 2.0:
            self.elixir_ready = True
            print("✨ Чудо! Элементы вошли в резонанс. Дань (Пилюля Бессмертия) создана!")

# === Запуск симулятора первого оборота ===
cauldron = AlchemyCauldron(lead_yang=50.0, mercury_yin=40.0)

# Алхимик делает 3 шага нагрева в правильные часы
cauldron.heat_cycle(hour=2, bellows_strokes=5)   # Растущий огонь
cauldron.heat_cycle(hour=4, bellows_strokes=6)   # Пик жара
cauldron.heat_cycle(hour=8, bellows_strokes=2)   # Охлаждение на Иньском часе
