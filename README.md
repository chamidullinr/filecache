# FileCache
Simple caching method for storing cached objects into pickle files.

In Python, there are several useful packages or methods for caching (for example `functools.cache` or `cachetools`).
However, they are focused on in-memory caching.
This means, that the output of the method that is cached is stored only in the memory (RAM),
and it is deleted when Python program stops.
However, in my experience I had a use-case where it was desirable to access outputs of cached methods
after restarting python kernel or a computer. And unfortunately, I couldn't find any package for such a use-case.
Therefore, I have decided to create a simple file caching method myself and share it in this repository.

The main goal of this repository is to provide an example of file caching in Python.
Anyone who is interested, can fork this repository and adjust it based on their needs.

## Usage
In this section, there is described a simple usage of the `filecache` package.

First import the `FileCache` class and create an instance. Parameter `path` defines location
where the pickle files will be stored. 

```python
from filecache import FileCache 
fc = FileCache(path='/tmp')
```

Then apply decorator `fc.cache()` to some method that takes long to compute and needs to be cached.

```python
@fc.cache()
def slow_method(arg1, arg2, arg3=None):
    # makes a long computation or a fetch request
    out = ...
    return out
```

And that is it!

### Methods with mutable or unhashable arguments

For a caching mechanism, it is needed to compute a unique identifier of arguments (args) and 
key arguments (kwargs). And for this, there is used hashing function that by default hashes
all arguments and key arguments that are passed to the method.
However, an issue can arise in cases when some arguments or key arguments are mutable or unhashabele. 

To overcome this, it is possible to pass `key` argument with `hashkey` method and select only
arguments that will hashed.

```python
from filecache import hashkey

@fc.cache(key=lambda arg1, mutable_arg, arg_to_ignore: hashkey(arg1))
def slow_method(arg1, mutable_arg, arg_to_ignore=None):
    # makes a long computation or a fetch request
    out = ...
    return out
```


### Decorator for class methods

When caching a class method, there can be a situation when class instance `self` (passed as an argument) 
is not hashable, or it is not desired to hash that argument. And to ignore `self` argument, 
simply set `ignore_self=True` in `fc.cache` function.

```python
class MyClass:
    @fc.cache(ignore_self=True)
    def slow_method(self, arg1, arg2, arg3=None):
        # makes a long computation or a fetch request
        out = ...
        return out
```

The same functionality as above, only with using `hashkey` method. The outcomes will be the same.

```python
from filecache import hashkey

class MyClass:
    @fc.cache(key=lambda self, *a, **k: hashkey(*a, **k))
    def slow_method(self, arg1, arg2, arg3=None):
        # makes a long computation or a fetch request
        out = ...
        return out
```


### List and remove cached objects
In the code below, there are shown examples for listing all objects that are currently stored
and examples for removing cached files.

```python
# list all objects that are currently cached
fc.list_cache()

# remove cached files till date 30/04/2021
fc.clear_cache(day=30, month=4, year=2021)

# remove all cached files
fc.clear_cache()
```


## Installation
To utilize this package, one needs to create a wheel file that can be installed through ``pip`` package manager.
To compile the `filecache` package, run the following command. It will create a wheel file ``.whl`` in directory ``dist/``.
``` bash
python setup.py bdist_wheel
```

Then, the package can be installed as easy as
``` bash
pip install dist/[GENERATED_FILE_NAME].whl
```

## Requirements
This package requires Python 3.6 or higher.
It uses modules that are part of the main python package,
i.e. modules such as hashlib, pickle, json, ect.


## Authors
**Rail Chamidullin** - chamidullinr@gmail.com  - [Github account](https://github.com/chamidullinr)
