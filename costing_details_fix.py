import csv
import sys
import argparse as arg
import os
from pathlib import Path


if getattr(sys, 'frozen', False):
    script_dir = Path(sys.executable).resolve().parent
else:
    script_dir = Path(__file__).resolve().parent

files = [file.name for file in script_dir.iterdir() if file.is_file()]

output_file = script_dir / 'output_data.csv'

stock_files = []
for item in files:
    if item == output_file.name:
        continue
    if item[-3:] == 'csv':
        stock_files.append(item)

class LineItem:
    def __init__(self, sku, description, vendor, uom, unit_cost):
        self.sku = sku
        
        self.description = description
        self.vendor = vendor
        if uom == 'Box':
            self.uom = 'Each'
            self.unit_cost = float(unit_cost)


        elif uom == 'Bottle':
            self.uom = 'Each'
            self.unit_cost = float(unit_cost)

        elif uom == 'Gallon':
            self.uom = 'Liter'
            self.unit_cost = round(float(unit_cost) / 3.78541, 2)

        elif uom == 'Gram':
            self.uom = 'Kilogram'
            self.unit_cost = round(float(unit_cost) * 1000, 2)

        elif uom == 'Pound':
            self.uom = 'Kilogram'
            self.unit_cost = round(float(unit_cost) / 0.453592, 2)

        else:
            self.uom = uom
            self.unit_cost = unit_cost


    
    def __repr__(self):
        return f'{self.sku} <{self.description}, {self.vendor}, {self.uom}, {self.unit_cost}>'

def sku_finder(line_item:LineItem):
    return line_item.sku

def find_correct_file(input_files: list[str]):
    chosen_file = None
    file_counts = {}

    for file in input_files:

        with open(script_dir / file) as data_set:
            data_reader = csv.reader(data_set)
            purchase_orders = []
            for row in list(data_reader)[1:]:
                try:
                    purchase_orders.append(int(row[6]))
                except:
                    continue
            file_counts[max(purchase_orders)] = file

    highest = max(list(file_counts.keys()))

    chosen_file = file_counts[highest]
    print(chosen_file)
    return chosen_file

def main():
    correct_file = find_correct_file(stock_files)
    all_line_items_unsorted = []
    with open(script_dir / correct_file) as read_file:
        reader = csv.reader(read_file)
        
        for item in list(reader)[1:]:
            all_line_items_unsorted.append(LineItem(item[0], item[1], item[2], item[3], item[4]))

    all_line_items_sorted = sorted(all_line_items_unsorted, key=sku_finder)
    with open(output_file, 'w', newline = '') as output:

        writer = csv.writer(output)
        writer.writerow(['SKU Number', 'Description', 'Vendor', 'PO Unit of Measure', 'Unit Cost'])
        for item in all_line_items_sorted:
            writer.writerow([item.sku, item.description, item.vendor, item.uom, item.unit_cost])
    os.startfile(output_file)


if __name__ == '__main__':

    if getattr(sys, 'frozen', False):
        try:
            main()
            print('Done. Wrote', output_file)
        except Exception as e:
            print('Error:', e)
        input('Press Enter to close...')
    else:
        main()
