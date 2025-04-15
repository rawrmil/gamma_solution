import os
import re
import csv

# Регулярное выражение для проверки имени папки
folder_pattern = re.compile(r'pallet_(\d+)_(\d+)_(\d+)$')

# Путь к директории с изображениями
images_dir = 'images'
results_dir = 'results'

# Список для валидных записей
valid_entries = []

# Проходим по всем элементам в папке images
for item in os.listdir(images_dir):
    item_path = os.path.join(images_dir, item)

    # Проверяем, что это директория и имя соответствует шаблону
    if os.path.isdir(item_path):
        match = folder_pattern.match(item)
        if match:
            # Проверяем наличие файлов
            left_path = os.path.join(item_path, 'left.png')
            right_path = os.path.join(item_path, 'right.png')

            if os.path.exists(left_path) and os.path.exists(right_path):
                # Извлекаем числа из имени папки
                laptop, tablet, group_box = match.groups()
                valid_entries.append({'name': item,'values': (laptop, tablet, group_box)})

# Записываем результат в CS
with open(results_dir + '/result.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['dir_name', 'laptop', 'tablet', 'group_box'])

    for entry in valid_entries:
        writer.writerow([entry['name'],*entry['values']])

print(f'Найдено валидных пар: {len(valid_entries)}')
print('Результат сохранён в result.csv')