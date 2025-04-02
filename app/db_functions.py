import csv

def read_data(csv_file):
    with open(csv_file, 'r') as file:
        header = file.readline()
        body = file.readlines()
        print(header)
        print(body)
        
read_data('customers.csv')