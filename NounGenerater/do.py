import csv
import pprint

first = True
dic = {}
key = 0
UP_LIMIT = 1

def read_dic(row):
    key = 0
    res = {}
    for x in row:
        res[x] = key
        key += 1
    return res


with open('7282_1.csv') as f:
    reader = csv.reader(f)
    cnt = 0
    for row in reader:
        if first:
            first = False
            dic = read_dic(row)
            continue
        cnt += 1
        print(row[dic['reviews.text']])
        if cnt == UP_LIMIT:
            break
