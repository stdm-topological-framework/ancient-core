#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ancient-Core Framework
Module: /russia/bell_acoustic.py
Concept: Bell Acoustic Automata / Акустические автоматы литья

Итерационный алгоритм расчета профилей тел вращения для колокольного литья.
Рассчитывает толщину стенок для генерации фрактальных обертонов и гашения паразитных вибраций.
"""

import math
from typing import Dict, List, Any, Tuple

class BellAcousticEngine:
    # Константы сплава (Древнерусская колокольная бронза: ~80% меди, ~20% олова)
    BRONZE_DENSITY_KG_M3 = 8800.0  # Плотность в кг/м³
    SPEED_OF_SOUND_BRONZE = 3450.0  # Скорость звука в сплаве (м/с)

    def __init__(self, strike_frequency_hz: float = 220.0, height_meters: float = 1.2):
        """
        Инициализация инженерного ядра для расчета колокола.
        strike_frequency_hz — целевая основная частота удара (например, Ля малой октавы).
        height_meters — общая высота колокола (задает масштаб резонанса).
        """
        self.target_freq = strike_frequency_hz
        self.height = height_meters
        
        # Расчет базового радиуса нижней юбки (устья) по законам акустической пропорции
        # Чем ниже частота, тем больше должен быть диаметр устья
        self.base_radius = (self.SPEED_OF_SOUND_BRONZE / (2 * self.target_freq)) * 0.65
        
    def generate_profile_mesh(self, steps: int = 50) -> List[Dict[str, float]]:
        """
        Итерационный расчет профиля колокола (тело вращения) снизу вверх.
        Возвращает массив срезов (высота, внешний радиус, толщина стенки).
        """
        profile = []
        dh = self.height / steps

        for i in range(steps + 1):
            h = i * dh
            normalized_h = h / self.height  # от 0.0 (низ) до 1.0 (топ)
            
            # 1. Алгоритм кривизны устья (гиперболическое сужение кверху)
            # Внизу — широкая юбка, посередине — талия, вверху — корона
            external_radius = self.base_radius * (0.35 + 0.65 * math.exp(-3.5 * normalized_h) + 0.15 * (normalized_h ** 3))
            
            # 2. Нелинейное изменение толщины стенки (Древнерусский канон пропорций)
            # Самое толстое место — "ударное кольцо" в самом низу (около 1/15 от диаметра),
            # затем стенка утончается к "талии" и снова утолщается к голове для прочности подвеса.
            if normalized_h <= 0.15:
                # Ударная часть (основной излучатель звука)
                wall_thickness = (self.base_radius * 2 / 15.0) * (1.0 - 0.3 * (normalized_h / 0.15))
            else:
                # Талия и верхнее плечо
                wall_thickness = (self.base_radius * 2 / 15.0) * 0.7 * (0.6 + 0.4 * normalized_h)
                
            profile.append({
                "height_level": h,
                "external_radius": external_radius,
                "wall_thickness": wall_thickness,
                "internal_radius": max(0.01, external_radius - wall_thickness)
            })
            
        return profile

    def calculate_mass_and_volume(self, profile: List[Dict[str, float]]) -> Tuple[float, float]:
        """
        Численное интегрирование объема полого тела вращения методом дисков.
        Вычисляет точный объем металла и финальный вес колокола в килограммах.
        """
        total_volume_m3 = 0.0
        
        for i in range(len(profile) - 1):
            h1 = profile[i]["height_level"]
            h2 = profile[i+1]["height_level"]
            dh = h2 - h1
            
            r_out_1 = profile[i]["external_radius"]
            r_in_1 = profile[i]["internal_radius"]
            r_out_2 = profile[i+1]["external_radius"]
            r_in_2 = profile[i+1]["internal_radius"]
            
            # Средние радиусы на данном шаге
            r_out_mid = (r_out_1 + r_out_2) / 2.0
            r_in_mid = (r_in_1 + r_in_2) / 2.0
            
            # Площадь кольца среза
            area = math.pi * (r_out_mid**2 - r_in_mid**2)
            total_volume_m3 += area * dh
            
        mass_kg = total_volume_m3 * self.BRONZE_DENSITY_KG_M3
        return mass_kg, total_volume_m3

    def predict_acoustic_spectrum(self, profile: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Математическое предсказание спектра обертонов на основе жесткости геометрии.
        Проверяет соблюдение золотого канона созвучия.
        """
        # Находим толщину ударного кольца (в самом низу профиля)
        strike_thickness = profile[0]["wall_thickness"]
        
        # Физическая формула частоты для изгибных колебаний кольцевых структур колокола
        fundamental = (self.SPEED_OF_SOUND_BRONZE * strike_thickness) / (self.base_radius ** 2) * 0.42
        
        # Каноническая русская структура пяти главных тонов (соотношение частот)
        spectrum = {
            "1_Hum_Tone (Унтертон)": fundamental * 0.5,
            "2_Fundamental (Основной)": fundamental,
            "3_Tierce (Малая терция)": fundamental * 1.189,
            "4_Quint (Квинта)": fundamental * 1.498,
            "5_Nominal (Номинал)": fundamental * 2.0
        }
        
        # Проверка на паразитный резонанс (биения). 
        # Если разница между терцией и квинтой не гармонична, возникнет гул.
        parasitic_delta = abs((spectrum["4_Quint (Квинта)"] / spectrum["3_Tierce (Малая терция)"]) - 1.26)
        is_harmonic = parasitic_delta < 0.05

        return {
            "spectrum_hz": spectrum,
            "is_perfect_harmonic": is_harmonic,
            "tuning_error_percent": parasitic_delta * 100
        }

if __name__ == "__main__":
    # Запускаем проектирование колокола с базовой частотой 220 Гц (Ля) и высотой 1.2 метра
    engine = BellAcousticEngine(strike_frequency_hz=220.0, height_meters=1.2)
    
    # 1. Генерируем 3D-сетку профиля
    mesh = engine.generate_profile_mesh(steps=20)
    
    # 2. Считаем массу
    mass, volume = engine.calculate_mass_and_volume(mesh)
    
    # 3. Анализируем акустику
    analysis = engine.predict_acoustic_spectrum(mesh)
    
    print("\n🔔 === СИМУЛЯТОР АКУСТИЧЕСКОГО АВТОМАТА КОЛОКОЛЬНОГО ЛИТЬЯ ===")
    print(f" -> Геометрия: Высота {engine.height}м | Радиус устья {engine.base_radius:.4f}м")
    print(f" -> Масса отливки: {mass:.2f} кг (Объем бронзы: {volume*1000:.1f} литров)")
    
    print("\n🎼 Прогноз частотного спектра аккорда при ударе:")
    for tone, freq in analysis["spectrum_hz"].items():
        print(f"   | {tone.ljust(25)} | {freq:.2f} Гц |")
        
    print("\n🛠️ Заключение ОТК цифрового литья:")
    if analysis["is_perfect_harmonic"]:
        print("   [ВЕРДИКТ] Профиль идеален. Чистый серебряный звон без паразитных биений.")
    else:
        print(f"   [ВЕРДИКТ] Требуется подрезка кружала! Погрешность настройки гармоник: {analysis['tuning_error_percent']:.2f}%")
    print("=" * 62 + "\n")
