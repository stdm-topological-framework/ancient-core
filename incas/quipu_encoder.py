import math
from typing import Dict, List, Any, Optional

class QuipuEncoderEngine:
    """
    Вычислительный движок узелковой сериализации данных Инков 'Кипу' (ICSR Node).
    Преобразует структурированные объекты Python (dict) в топологические карты узлов и нитей.
    
    Поддерживает:
    - Разрядную десятичную позиционную систему инков.
    - Дифференциацию узлов: простые (10+), длинные (2-9 в разряде единиц), восьмерки (1 в разряде единиц).
    - Цветовое кодирование метаданных (свойств JSON-объекта).
    """
    
    # Традиционная евразийско-индейская кодировка цветов для метаданных инков
    COLOR_MAP = {
        "population": "Красная нить (Люди / Воины)",
        "gold": "Желтая нить (Золото / Священные металлы)",
        "corn": "Зеленая нить (Маис / Урожай)",
        "potatoes": "Бурая нить (Картофель / Склады)",
        "default": "Белая нить (Общие учетные данные)"
    }

    def __init__(self):
        pass

    def _encode_number_to_knots(self, num: int) -> List[Dict[str, Any]]:
        """
        Разбивает число по десятичным разрядам и определяет форму узлов.
        Нижний разряд (единицы) кодируется длинными узлами или восьмерками.
        Высшие разряды (10, 100...) кодируются простыми узлами.
        """
        if num == 0:
            return [{"tier": "Единицы [10^0]", "knot_type": "ПУСТОТА (Ноль / Пустая нить)", "count": 0}]

        knot_structure = []
        str_num = str(num)[::-1]  # Разворачиваем число, чтобы идти от единиц вверх
        
        for i, digit_str in enumerate(str_num):
            digit = int(digit_str)
            tier_name = f"Разряд 10^{i}"
            
            if digit == 0:
                # Нулевой разряд пропускается, оставляя физический зазор на нити
                continue
                
            if i == 0:  # Логика для разряда единиц (Специфика Кипу)
                if digit == 1:
                    knot_type = "Узел-Восьмерка (Figure-eight knot)"
                else:
                    knot_type = f"Длинный узел с {digit} витками (Long knot)"
                count = 1  # Длинный узел завязывается один раз, но имеет витки
            else:  # Логика для высших разрядов (Десятки, сотни, тысячи...)
                knot_type = "Простой петлевой узел (Overhand knot)"
                count = digit
                
            knot_structure.append({
                "tier_level": i,
                "tier_name": tier_name,
                "knot_type": knot_type,
                "count": count
            })
            
        # Возвращаем структуру, отсортированную от высших разрядов к низшим (сверху вниз по нити)
        return sorted(knot_structure, key=lambda x: x["tier_level"], reverse=True)

    def serialize_json_to_quipu(self, data: Dict[str, int]) -> Dict[str, Any]:
        """
        Главный метод сериализации. Принимает словарь с данными и возвращает 
        структурную схему текстильного узлового архива Кипу.
        """
        quipu_archive = {
            "main_cord": "Главный несущий шнур Кипу (Base Cord)",
            "total_pendents": len(data),
            "pendent_strings": []
        }
        
        for position, (key, value) in enumerate(data.items()):
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"Ошибка сериализации: Значение для '{key}' должно быть неотрицательным целым числом.")
            
            # Определяем цвет нити на основе ключа данных
            string_color = self.COLOR_MAP.get(key.lower(), self.COLOR_MAP["default"])
            
            # Генерируем узелковую топологию для значения
            knots_layout = self._encode_number_to_knots(value)
            
            quipu_archive["pendent_strings"].append({
                "string_position_index": position,
                "data_category_key": key,
                "string_color_code": string_color,
                "numerical_value": value,
                "knots_layout_top_to_bottom": knots_layout
            })
            
        return quipu_archive

    def print_quipu_blueprint(self, quipu_data: Dict[str, Any]):
        """ Выводит в консоль красивую, наглядную схему завязывания узелков Кипу """
        print("\n" + "="*80)
        print(" СХЕМА СЕРИАЛИЗАЦИИ ДАННЫХ В ТЕКСТИЛЬНЫЙ АРХИВ КИПУ (ИМПЕРИЯ ИНКОВ) ")
        print("="*80)
        print(f"🧬 СТАТУС: {quipu_data['main_cord']} успешно развернут.")
        print(f"🧵 Всего свисающих нитей привязано: {quipu_data['total_pendents']}\n")
        
        for s in quipu_data["pendent_strings"]:
            print(f" Позиция нити #{s['string_position_index']} | Категория: [{s['data_category_key']}] -> Значение: {s['numerical_value']}")
            print(f" 🎨 Окрас нити: {s['string_color_code']}")
            print(" 📍 Расположение узелков (сверху вниз от главного шнура):")
            
            for knot in s["knots_layout_top_to_bottom"]:
                if "count" in knot and knot["count"] > 1:
                    print(f"   └── [{knot['tier_name']}] -> {knot['knot_type']} x{knot['count']} шт.")
                else:
                    print(f"   └── [{knot['tier_name']}] -> {knot['knot_type']}")
            print(" ───" * 15)
        print("="*80 + "\n")


# === СТЕНДОВЫЕ ИСПЫТАНИЯ МОДУЛЯ ИНКА ===
if __name__ == "__main__":
    encoder = QuipuEncoderEngine()
    
    # Исходный JSON-объект с данными переписи провинции Куско
    # Данные содержат числа разных разрядов для проверки всех типов узлов
    cusco_inventory_data = {
        "gold": 352,        # Проверит простые узлы (3 сотни, 5 десятков) и длинный узел (2 единицы)
        "population": 1041, # Проверит ноль в разряде сотен (пропуск) и восьмерку (1 единица)
        "corn": 8,          # Проверит работу только в разряде единиц (длинный узел с 8 витками)
        "potatoes": 0       # Проверит кодирование абсолютного нуля (пустая нить)
    }
    
    # Запускаем трансляцию данных в узлы Кипу
    quipu_blueprint = encoder.serialize_json_to_quipu(cusco_inventory_data)
    
    # Печатаем технологическую карту для Кипукамайока
    encoder.print_quipu_blueprint(quipu_blueprint)
