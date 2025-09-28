import os
import re
import csv

folder_pattern = re.compile(r'pallet_(\d+)_(\d+)_(\d+)$')
images_dir = './images'
results_dir = './results'

def get_entries():
    valid_entries = []
    for item in os.listdir(images_dir):
        item_path = os.path.join(images_dir, item)
        if os.path.isdir(item_path):
            match = folder_pattern.match(item)
            if match:
                left_path = os.path.join(item_path, 'left.png')
                right_path = os.path.join(item_path, 'right.png')
                if os.path.exists(left_path) and os.path.exists(right_path):
                    laptop, tablet, group_box = match.groups()
                    valid_entries.append({'name': item, 'values': (laptop, tablet, group_box), 'dpath': item_path})
    return valid_entries

def get_dataset():
    ve = get_entries()
    dataset = [(e['dpath'], e['name'], e['values']) for e in ve]
    return dataset

def write_to_csv(fname):
    with open(results_dir+'/'+fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['dir_name', 'laptop', 'tablet', 'group_box'])
        for entry in valid_entries:
            writer.writerow([entry['name'], *entry['values']])

if __name__ == '__main__':
    valid_entries = get_entries()
    write_to_csv('result.csv')
    print(get_dataset())
    print(f'Найдено валидных пар: {len(valid_entries)}')
    print('Результат сохранён в result.csv')
