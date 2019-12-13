import json
import os
import csv
from typing import List


def convert(json_path: str, csv_path: str, csv_name: str) -> bool:

    if json_path == '' or csv_path == '' or csv_name == '':
        return False

    if not os.path.exists(csv_path):
        os.mkdir(csv_path)


    src_path: str = json_path
    dst_path: str = csv_path
    if not json_path.endswith('/'): src_path += '/'
    if not csv_path.endswith('/'): dst_path += '/'
    dst_path += csv_name

    paths: List[str] = os.listdir(json_path)
    with open(dst_path, 'w+') as dst:
        dst_csv = csv.writer(dst)
        dst_csv.writerow(['Title', 'Link', 'Article'])

        for path in paths:
            if os.path.isdir(path): continue

            with open(src_path + path, 'r') as src:
                src_json = json.load(src)
                dst_csv.writerow([src_json['Title'], src_json['Link'], src_json['Article']])

    return True



if __name__ == '__main__':
    convert('./result/ABC/US/', './result_csv/', 'ABC_US.csv')
    convert('./result/ABC/Business/', './result_csv/', 'ABC_Business.csv')
    convert('./result/ABC/Politics/', './result_csv/', 'ABC_Politics.csv')

    convert('./result/BBC/US_and_canada/', './result_csv/', 'BBC_US_Canada.csv')
    convert('./result/BBC/Business/', './result_csv/', 'BBC_Business.csv')
    convert('./result/BBC/Politics/', './result_csv/', 'BBC_Politics.csv')

    convert('./result/CNN/US/', './result_csv/', 'CNN_US.csv')
    convert('./result/CNN/Business/', './result_csv/', 'CNN_Business.csv')
    convert('./result/CNN/Politics/', './result_csv/', 'CNN_Politics.csv')

