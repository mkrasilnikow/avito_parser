import os
import csv

from storages.storage import Storage


class FileStorage(Storage):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        if not os.path.exists(self.file_name):
            raise StopIteration

        with open(self.file_name) as f:
            for line in f:
                yield line.strip()

    def write_data(self, data_array):
        """
        :param data_array: collection of dictionaries that
        should be written as lines
        """
        with open(self.file_name, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow((
                'type_of_flat',
                'area',
                'floor',
                'total_floors',
                'subway',
                'distance_to_subway',
                'price',
            ))
            if data_array:
                for data_elem in data_array:
                    writer.writerow((
                        data_elem['type_of_flat'],
                        data_elem['area'],
                        data_elem['floor'],
                        data_elem['total_floors'],
                        data_elem['subway'],
                        data_elem['distance_to_subway'],
                        data_elem['price'],
                    ))


    def append_data(self, data):
        """
        :param data: collection of dictionaries that
        should be written as lines
        """
        with open(self.file_name, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for data_elem in data:
                writer.writerow((
                    data_elem['type_of_flat'],
                    data_elem['area'],
                    data_elem['floor'],
                    data_elem['total_floors'],
                    data_elem['subway'],
                    data_elem['distance_to_subway'],
                    data_elem['price'],
                ))
