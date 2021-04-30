from functools import wraps
import os
import json
import hashlib
from datetime import datetime

from . import io


def hashkey(*args, **kwargs):
    """
    Converts arguments (args) and key arguments (kwargs) into hash values.

    The method applies the following steps:
        1. convert args and kwargs into two json strings and concatenate them into one string
        2. convert string into bytes using ascii encoding
        3. convert bytes into hash value using sha256 hash function
    """
    str_key = json.dumps(args, sort_keys=True) + json.dumps(kwargs, sort_keys=True)
    bytes_key = bytes(str_key, 'ascii')  # utf-8
    hash_key = hashlib.sha256(bytes_key).hexdigest()
    return hash_key


class FileCache:
    def __init__(self, path='/tmp'):
        io.create_path(path)
        self.path = path

    def clear_cache(self, *, day=None, month=None, year=None):
        """
        Removes files in cache directory.

        If params day, month and year are specified the method removes only cache files
        that were created or modified before the specified date.
        """
        files = io.get_filenames_in_dir(self.path, file_type='pkl', include_path=True)

        if day is not None and month is not None and year is not None:
            files_to_remove = []
            till_date = datetime(day=day, month=month, year=year)
            for item in files:
                item_date = datetime.fromtimestamp(os.stat(item).st_mtime)
                if item_date < till_date:
                    files_to_remove.append(item)
        else:
            files_to_remove = files

        for item in files_to_remove:
            if os.path.isfile(item):
                os.remove(item)

    def list_cache(self):
        """
        Lists all items stored in cache.

        The method returns names of cached files without `path` as a prefix and `.pkl` as a suffix.
        """
        out = io.get_filenames_in_dir(self.path, file_type='pkl', include_path=False)
        out = [item.replace('.pkl', '') for item in out]
        return out

    def save_file(self, obj, filename):
        """Saves object to pickle file."""
        file_path = os.path.join(self.path, filename + '.pkl')
        io.save_pickle(obj, file_path)

    def load_file(self, filename):
        """Loads object from pickle file."""
        file_path = os.path.join(self.path, filename + '.pkl')
        return io.load_pickle(file_path)

    def cache(self, key=hashkey, ignore_self=False):
        """Decorator method used for caching outputs of methods in file cache."""
        def wrapper(func):  # decorator with args and kwargs
            @wraps(func)
            def decorator(*args, **kwargs):
                # hash args and kwargs
                _args = args[1:] if ignore_self else args
                filename = f'{func.__name__}-{key(*_args, **kwargs)}'

                # check if the file exists
                exists = filename in self.list_cache()
                if exists:
                    # load function output from pickle file
                    out = self.load_file(filename)
                else:
                    # apply function and save output to pickle file
                    out = func(*args, **kwargs)
                    self.save_file(out, filename)

                return out

            return decorator
        return wrapper
