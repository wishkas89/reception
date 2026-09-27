import os


# =====================================================================
# Задача №1: Чтение кулинарной книги из файла
# =====================================================================
def read_cook_book(file_path):
    """Читает файл с рецептами и возвращает словарь cook_book."""
    cook_book = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            # Читаем название блюда
            dish_name = file.readline().strip()
            if not dish_name:
                break  # Конец файла
                
            # Читаем количество ингредиентов
            ingredients_count = int(file.readline().strip())
            
            ingredients_list = []
            for _ in range(ingredients_count):
                ingredient_line = file.readline().strip()
                # Разбираем строку по разделителю "|"
                name, quantity, measure = ingredient_line.split(' | ')
                
                ingredients_list.append({
                    'ingredient_name': name,
                    'quantity': int(quantity),
                    'measure': measure
                })
            
            # Сохраняем блюдо в книгу
            cook_book[dish_name] = ingredients_list
            
            # Пропускаем пустую строку между блюдами, если она есть
            file.readline()
            
    return cook_book


# =====================================================================
# Задача №2: Подсчет ингредиентов для списка блюд и персон
# =====================================================================
def get_shop_list_by_dishes(dishes, person_count, cook_book):
    """Считает количество ингредиентов для заданного списка блюд и гостей."""
    shop_list = {}
    
    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                measure = ingredient['measure']
                # Считаем количество на всех персон
                total_quantity = ingredient['quantity'] * person_count
                
                # Если ингредиент уже есть в списке, суммируем его
                if name in shop_list:
                    shop_list[name]['quantity'] += total_quantity
                else:
                    shop_list[name] = {
                        'measure': measure,
                        'quantity': total_quantity
                    }
        else:
            print(f"Предупреждение: Блюда '{dish}' нет в кулинарной книге!")
            
    return shop_list


# =====================================================================
# Задача №3: Слияние файлов, отсортированных по количеству строк
# =====================================================================
def merge_files(file_names, result_file_path):
    """Считает строки в файлах, сортирует их и объединяет в один файл."""
    files_info = []
    
    # 1. Собираем информацию о количестве строк в каждом файле
    for file_name in file_names:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                files_info.append({
                    'name': file_name,
                    'count': len(lines),
                    'content': lines
                })
        else:
            print(f"Ошибка: Файл '{file_name}' не найден для слияния.")
            
    # 2. Сортируем список файлов по возрастанию количества строк
    files_info.sort(key=lambda x: x['count'])
    
    # 3. Записываем отсортированные данные в результирующий файл
    with open(result_file_path, 'w', encoding='utf-8') as result_file:
        for file_data in files_info:
            result_file.write(f"{file_data['name']}\n")
            result_file.write(f"{file_data['count']}\n")
            
            # Записываем строки содержимого
            for line in file_data['content']:
                result_file.write(line)
                
            # Гарантируем перенос строки в конце контента файла, если его не было
            if file_data['content'] and not file_data['content'][-1].endswith('\n'):
                result_file.write('\n')


# =====================================================================
# Главная управляющая функция
# =====================================================================
def main():
    # Имя файла с рецептами
    recipes_file = 'recipes.txt'
    
    if not os.path.exists(recipes_file):
        print(f"Пожалуйста, создайте файл '{recipes_file}' рядом с кодом!")
        return

    print("--- Задача №1: Чтение кулинарной книги ---")
    cook_book = read_cook_book(recipes_file)
    import pprint
    pprint.pprint(cook_book, sort_dicts=False)
    print("\n" + "="*50 + "\n")

    print("--- Задача №2: Список покупок (Омлет и Запеченный картофель на 2 персоны) ---")
    dishes_to_cook = ['Запеченный картофель', 'Омлет']
    persons = 2
    shop_list = get_shop_list_by_dishes(dishes_to_cook, persons, cook_book)
    pprint.pprint(shop_list, sort_dicts=False)
    print("\n" + "="*50 + "\n")

    print("--- Задача №3: Слияние файлов 1.txt, 2.txt ---")
    # Для демонстрации создадим тестовые файлы, если их нет
    for name, lines_cnt in [('1.txt', 2), ('2.txt', 1)]:
        if not os.path.exists(name):
            with open(name, 'w', encoding='utf-8') as f:
                for i in range(1, lines_cnt + 1):
                    f.write(f"Строка номер {i} файла номер {name[0]}\n")
                    
    files_to_merge = ['1.txt', '2.txt']
    output_file = 'merged_result.txt'
    merge_files(files_to_merge, output_file)
    print(f"Файлы успешно объединены в '{output_file}'!")


if __name__ == '__main__':
    main()

