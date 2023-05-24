import os

def search_files(directory, keyword):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                for line in f:
                    if keyword in line:
                        print("단어 '{}' 가 포함된 파일: {}".format(keyword, file_path))
                        break  # Exit the loop if keyword is found in the current file

# Specify the directory and keyword
directory = '/allnew/python/lessons'  # Replace with the directory path you want to search
keyword = 'axious'  # Replace with the keyword you want to search

# Call the search_files function
search_files(directory, keyword)