    def to_base60(self, number: float) -> Tuple[List[int], List[int]]:
        """
        Преобразует десятичное число в вавилонский позиционный формат Base-60.
        Возвращает кортеж: (целая_часть_списком, дробная_часть_списком)
        """
        # Извлекаем целую и дробную часть, работая с абсолютным значением
        abs_number = abs(number)
        integer_part = int(abs_number)
        fractional_part = abs_number - integer_part

        # 1. Расчет целой части в Base-60 (делением на 60)
        base60_int = []
        if integer_part == 0:
            base60_int = [0]
        else:
            temp_int = integer_part
            while temp_int > 0:
                base60_int.append(temp_int % 60)
                temp_int //= 60
            # Разряды получились задом наперед (от младшего к старшему), разворачиваем:
            base60_int.reverse()

        # 2. Расчет дробной части в Base-60 (умножением на 60)
        base60_frac = []
        temp_frac = fractional_part
        
        # Генерируем столько разрядов, сколько задано в self.precision
        for _ in range(self.precision):
            # Если дробный хвост обнулился, можно закончить раньше
            if temp_frac == 0:
                break
            temp_frac *= 60
            digit = int(temp_frac)
            base60_frac.append(digit)
            temp_frac -= digit

        return base60_int, base60_frac
