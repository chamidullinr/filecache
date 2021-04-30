import os
import re
import pickle


def get_filenames_in_dir(dir_path, file_type=None, include_path=True):
    try:
        files = [os.path.join(dir_path, item) if include_path else item
                 for item in os.listdir(dir_path)]
    except FileNotFoundError:
        files = []

    if file_type is not None:
        files = [item for item in files
                 if re.search(r'(\.{})$'.format(file_type), item)]
    return files


def create_path(path):
    dir_path = os.path.dirname(path)
    if len(dir_path) > 0:
        os.makedirs(dir_path, exist_ok=True)


def save_pickle(obj, filename):
    create_path(filename)
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
