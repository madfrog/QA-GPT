# coding=utf-8
import os


class FileHelper(object):

    @classmethod
    def get_all_file_names(cls, folder_path):
        '''Get all file names in docs folder'''
        all_file_names = os.listdir(folder_path)
        # all_file_names = ["uber-2019.html", "uber-2020.html"]
        return all_file_names

    @classmethod
    def filter_file_by_type(cls, file_name_list, type_str):
        '''
        Filter out file with its type.
        @file_name_list
        @type_str: .pdf, .txt
        '''
        files = []
        for name in file_name_list:
            if name.endswith(type_str):
                files.append(name)
        return files
        
    @classmethod 
    def get_company_name_and_year(cls, file_name):
        """Parsing 10-k file name to get company name and year."""
        # TODO: check the file_name if valid
        first_split_results = file_name.split("-")
        second_split_results = first_split_results[1].split(".")
        print(first_split_results[1])
        return first_split_results[0], first_split_results[1][0:4], f'{first_split_results[0]}-{second_split_results[0]}'
