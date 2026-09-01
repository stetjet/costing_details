import csv
import argparse as arg
from favorite_functions import *
from pathlib import Path


script_dir = Path(__file__).resolve().parent
files = [file.name for file in script_dir.iterdir() if file.is_file()]
debug_print(files)
output_file = 'output_data.csv'

stock_files = []
for item in files:
    if item == output_file:
        continue
    if item[-3:] == 'csv':
        stock_files.append(item)


debug_print(stock_files)


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

        with open(file) as data_set:
            data_reader = csv.reader(data_set)
            purchase_orders = []
            for row in list(data_reader)[1:]:
                purchase_orders.append(int(row[6]))
            file_counts[max(purchase_orders)] = file

    highest = max(list(file_counts.keys()))

    chosen_file = file_counts[highest]

    return chosen_file




def main():
    correct_file = find_correct_file(stock_files)
    all_line_items_unsorted = []
    with open(correct_file) as read_file:
        reader = csv.reader(read_file)
        
        for item in list(reader)[1:]:
            all_line_items_unsorted.append(LineItem(item[0], item[1], item[2], item[3], item[4]))

    debug_print(all_line_items_unsorted)
    all_line_items_sorted = sorted(all_line_items_unsorted, key=sku_finder)
    debug_print(all_line_items_sorted)
    with open(output_file, 'w', newline = '') as output:

        writer = csv.writer(output)
        writer.writerow(['SKU Number', 'Description', 'Vendor', 'PO Unit of Measure', 'Unit Cost'])
        for item in all_line_items_sorted:
            writer.writerow([item.sku, item.description, item.vendor, item.uom, item.unit_cost])

if __name__ == '__main__':

    main()
    pass