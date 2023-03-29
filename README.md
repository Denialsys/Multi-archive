# Multi archive

Package for archiving and decompression of multiple archive files. Can be used for exported functions from cloud infrastructure

## Installation

```console
$ pip install git+https://github.com/Denialsys/Multi-archive.git#egg=Multi-archive
```

You can also install using the Pipenv virtualization, or virtual environment of your liking

```console
$ pipenv install git+https://github.com/Denialsys/Multi-archive.git#egg=Multi-archive
```


## Example usage:

Example usage for the package

```python
import multiarchive

# This will initialize the seed for creating a random password
multiarchiver_obj = multiarchive('tuelzoJheKlIp2.t652')

# OR, initialize the module with the default password
multiarchiver_obj = multiarchive()

# See help for each member function to check the sample usage
# Example:
print(dir(multiarchiver_obj))
help(multiarchiver_objunzip_archives)
```

For compressing with password, the function will target archive files (zip)
```python
import multiarchive

archiver_obj = multiarchive.Archiver('skivyttes')

print(multiarchive.VERSION)

# Using relative file path, archive files within the directory will be password protected
# The output files will be placed inside 'archive_files\Protected_Archive'
# Each file will have different passwords based from 'skivyttes' and filename
archiver_obj.zip_with_dynamic_password('archive_files')

# This will reverse the process, and store the
# output files to 'test_files\\Protected_Archive\\Extracted' 
archiver_obj.unzip_archives('archive_files\\Protected_Archive\\Extracted')
```

