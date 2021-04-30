from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = ''.join(f.readlines())

setup(
    name='filecache',
    version='0.1.0',
    description='Simple caching method for storing cached objects into pickle files.',
    long_description=long_description,
    author='Rail Chamidullin',
    author_email='chamidullinr@gmail.com',
    url='https://github.com/chamidullinr/filecache',
    packages=find_packages(),
    py_module=['filecache'],
    python_requires=">=3.6",
    install_requires=[]
)
