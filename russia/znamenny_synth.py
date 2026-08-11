#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ancient-Core Framework
Module: /russia/znamenny_synth.py
Concept: Combinatorial Sound Synthesis / Комбинаторный синтез звука

Графический синтезатор звука на основе древнерусской крюковой (знаменной) нотации.
Переводит комбинаторные траектории знамен в динамические аудио-волны.
"""

import math
import struct
from typing import List, Tuple, Dict

class ZnamennySynthesizer:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
        # 1. Строим древнерусский ОБИХОДНЫЙ ЗВУКОРЯД (инварианты частот в Гц) [1]
        # Он делится на Прогрессии (Согласия): Простое, Мрачное, Светлое, Тресветлое
        self.PITCH_SPACE: Dict[str, float] = {
            # Простые (низкие)
            "простая_низкая": 110.00,  # A2
            "простая_средняя": 123.47, # B2
            "простая_высокая": 130.81, # C3
            # Мрачные
            "мрачная_низкая": 146.83,  # D3
            "мрачная_средняя": 164.81, # E3
            "мрачная_высокая": 174.61, # F3
            # Светлые (основные)
            "светлая_низкая": 196.00,  # G3
            "светлая_средняя": 220.00, # A3
            "светлая_высокая": 246.94, # B3
            # Тресветлые (высокие)
            "тресветлая_низкая": 261.63,  # C4
            "тресветлая_средняя": 293.66, # D4
            "тресветлая_высокая": 329.63, # E4
        }

        # 2. Матрица траекторий КРЮКОВ (Векторы изменения частоты и громкости во времени)
        # Каждое знамя — это микро-алгоритм для генератора волновой формы
        self.HOOK_ALGORITHMS: Dict[str, dict] = {
            "крюк_простой": {
                "desc": "Ровный тон с мягкой атакой и затуханием",
                "pitch_curve": lambda f, t: f,
                "amp_curve": lambda t: math.sin(math.pi * t)  # Купольная огибающая
            },
            "стопица": {
                "desc": "Короткий, отрывистый квант звука",
                "pitch_curve": lambda f, t: f,
                "amp_curve": lambda t: math.exp(-5.0 * t)     # Резкое экспоненциальное затухание
            },
            "запятая": {
                "desc": "Плавный восходящий изгиб в конце звука",
                "pitch_curve": lambda f, t: f * (1.0 + 0.12 * (t ** 2)),  # Уход вверх на полтона
                "amp_curve": lambda t: math.sin(math.pi * t * 0.8)
            },
            "стрела_светлая": {
                "desc": "Импульсный взлет частоты с последующим удержанием",
                "pitch_curve": lambda f, t: f * (1.15 if t > 0.3 else 1.0 + 0.5 * math.sin(t * 5)),
                "amp_curve": lambda t: 1.0 - t
            },
            "голубчик": {
                "desc": "Быстрый волновой перескок снизу вверх (орнаментальный глиссандирующий шаг)",
                "pitch_curve": lambda f, t: f * (1.0 if t < 0.4 else 1.25), # Прыжок на кварту вверх
                "amp_curve": lambda t: math.sin(math.pi * t)
            }
        }

    def _generate_tone(self, base_freq: float, hook_name: str, duration_sec: float) -> List[float]:
        """Генерация массива сэмплов для одного крюка на основе его внутренней функции-траектории."""
        num_samples = int(self.sample_rate * duration_sec)
        samples = []
        phase = 0.0
        
        hook = self.HOOK_ALGORITHMS[hook_name]
        pitch_fn = hook["pitch_curve"]
        amp_fn = hook["amp_curve"]

        for i in range(num_samples):
            t = i / num_samples  # Нормализованное время от 0.0 до 1.0
            
            # Динамически вычисляем текущую частоту и амплитуду по формуле крюка
            current_freq = pitch_fn(base_freq, t)
            current_amp = amp_fn(t)
            
            # Инкремент фазы с учетом изменяющейся частоты
            phase += 2.0 * math.pi * current_freq / self.sample_rate
            
            # Генерируем чистую синусоиду (можно усложнить обертонами для плотности)
            sample = math.sin(phase) * current_amp
            samples.append(sample)
            
        return samples

    def synthesize_sequence(self, score: List[Tuple[str, str, float]], output_filename: str = "znamenny_output.wav"):
        """
        Компиляция последовательности крюков в финальный аудиофайл WAVE.
        score: список кортежей вида [("название_ноты", "название_крюка", длительность_в_сек)]
        """
        raw_audio: List[float] = []
        
        print(f"\n[🎙️] Запуск синтеза крюковой последовательности...")
        for idx, (pitch_key, hook_key, duration) in enumerate(score):
            if pitch_key not in self.PITCH_SPACE or hook_key not in self.HOOK_ALGORITHMS:
                print(f" -> [Ошибка] Пропуск некорректного шага {idx}")
                continue
                
            freq = self.PITCH_SPACE[pitch_key]
            desc = self.HOOK_ALGORITHMS[hook_key]["desc"]
            print(f" -> Шаг {idx}: Нота {pitch_key} ({freq} Hz) -> Огибающая '{hook_key}' ({desc})")
            
            # Генерируем сэмплы для этого шага и склеиваем в общий поток
            tone_samples = self._generate_tone(freq, hook_key, duration)
            raw_audio.extend(tone_samples)

        # Нормализация и конвертация аудиопотока в 16-битные целые числа (PCM)
        max_val = max(abs(x) for x in raw_audio) if raw_audio else 1.0
        normalized_pcm = [int((x / max_val) * 32767) for x in raw_audio]

        # Запись бинарного заголовка WAVE и данных на диск
        self._write_wav(output_filename, normalized_pcm)
        print(f"[✅] Синтез завершен! Файл сохранен как: {output_filename}\n")

    def _write_wav(self, filename: str, pcm_data: List[int]):
        """Низкоуровневая сборка PCM WAVE файла без сторонних библиотек."""
        num_channels = 1
        bytes_per_sample = 2
        data_size = len(pcm_data) * bytes_per_sample
        
        with open(filename, "wb") as f:
            # RIFF Header
            f.write(b"RIFF")
            f.write(struct.pack("<I", 36 + data_size))
            f.write(b"WAVE")
            # Subchunk 1 (fmt )
            f.write(b"fmt ")
            f.write(struct.pack("<I", 16)) # Размер подчанка
            f.write(struct.pack("<H", 1))  # Аудио-формат (1 = PCM)
            f.write(struct.pack("<H", num_channels))
            f.write(struct.pack("<I", self.sample_rate))
            f.write(struct.pack("<I", self.sample_rate * num_channels * bytes_per_sample))
            f.write(struct.pack("<H", num_channels * bytes_per_sample))
            f.write(struct.pack("<H", bytes_per_sample * 8)) # Бит на сэмпл
            # Subchunk 2 (data)
            f.write(b"data")
            f.write(struct.pack("<I", data_size))
            # Запись сэмплов
            for sample in pcm_data:
                f.write(struct.pack("<h", sample))

if __name__ == "__main__":
    synth = ZnamennySynthesizer()
    
    # Партитура древнерусского распева (Нота, Крюк/Траектория, Длительность в сек)
    ancient_score = [
        ("светлая_низкая", "крюк_простой", 1.5),
        ("светлая_средняя", "голубчик", 1.2),
        ("светлая_высокая", "запятая", 1.8),
        ("мрачная_высокая", "стрела_светлая", 2.0),
        ("простая_высокая", "стопица", 0.5),
        ("светлая_низкая", "крюк_простой", 2.5)
    ]
    
    synth.synthesize_sequence(ancient_score, "ancient_chant.wav")
