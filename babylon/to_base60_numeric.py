import numpy as np

# 1. Настройки симуляции
STEPS = 1_000_000
IDEAL_RESULT = STEPS / 3  # Теоретический точный результат: 333333.3333333333...

print(f"=== ЗАПУСК СИМУЛЯЦИИ НА {STEPS:,} ИТЕРАЦИЙ ===")
print(f"Идеальное математическое значение: {IDEAL_RESULT}\n")

# 2. Тест Float32 (Одинарная точность - как в видеокартах и старых движках)
f32_sum = np.float32(0.0)
f32_increment = np.float32(1.0 / 3.0)

for _ in range(STEPS):
    f32_sum += f32_increment

f32_error = f32_sum - IDEAL_RESULT
print(f"[!] Результат Float32 (32-bit):  {f32_sum}")
print(f"    Накопленная погрешность:     {f32_error:+.9f}")
print("-" * 50)

# 3. Тест Float64 (Двойная точность - стандартный float в Python)
f64_sum = 0.0
f64_increment = 1.0 / 3.0

for _ in range(STEPS):
    f64_sum += f64_increment

f64_error = f64_sum - IDEAL_RESULT
print(f"[!] Результат Float64 (64-bit):  {f64_sum}")
print(f"    Накопленная погрешность:     {f64_error:+.9f}")
print("-" * 50)

# 4. Вавилонская логика (Base-60 на базе целых чисел)
# В системе Base-60 число 1/3 представляется как 0 целых и 20 шестидесятых долей.
# Мы складываем только целые шестидесятые доли (чистые двадцатки), защищаясь от дробей.
vavilon_sixtieths = 0
vavilon_increment = 20  # 20/60 это ровно 1/3

for _ in range(STEPS):
    vavilon_sixtieths += vavilon_increment

# Переводим итоговые шестидесятые доли назад в привычный вид:
# Разделение на целую часть и остаток через целочисленный оператор %
vavilon_whole = vavilon_sixtieths // 60
vavilon_fraction = vavilon_sixtieths % 60

# Считаем итоговое значение для вывода на экран
vavilon_final_value = vavilon_whole + (vavilon_fraction / 60)
vavilon_error = vavilon_final_value - IDEAL_RESULT

print(f"[#] Вавилонская логика (Base-60): Целых: {vavilon_whole}, Дробных долей (1/60): {vavilon_fraction}")
print(f"    Итоговое значение:           {vavilon_final_value}")
print(f"    Накопленная погрешность:     {vavilon_error:+.9f} (АБСОЛЮТНЫЙ НОЛЬ)")
print("=" * 50)
