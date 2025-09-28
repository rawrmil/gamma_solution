import os
import re
import csv

folder_pattern = re.compile(r'pallet_(\d+)_(\d+)_(\d+)$')
images_dir = '../images'
results_dir = '.'

valid_entries = []

def get_dataset():
    dataset = [] # (dirpath, (laptop, tablet, group_box))
    for item in os.listdir(images_dir):
        item_path = os.path.join(images_dir, item)
        if os.path.isdir(item_path):
            match = folder_pattern.match(item)
            if match:
                left_path = os.path.join(item_path, 'left.png')
                right_path = os.path.join(item_path, 'right.png')
                if os.path.exists(left_path) and os.path.exists(right_path):
                    laptop, tablet, group_box = match.groups()
                    valid_entries.append({'name': item,'values': (laptop, tablet, group_box)})
                    dataset.append((item_path, (laptop, tablet, group_box)))
    return dataset

def write_to_csv(fname):
    with open(results_dir+'/'+fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['dir_name', 'laptop', 'tablet', 'group_box'])
        for entry in valid_entries:
            writer.writerow([entry['name'],*entry['values']])

if __name__ == '__main__':
    write_to_csv('/result.csv')
    print(f'Найдено валидных пар: {len(valid_entries)}')
    print('Результат сохранён в result.csv')
