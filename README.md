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
To enable creation of password file containing the archive and their corresponding 
password as well as setting the verbosity
```python
import multiarchive

archiver_obj = multiarchive.Archiver('skivyttes')
archiver_obj.set_password_file_creation(True)
archiver_obj.set_verbose(True)
```


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

Password setting for the extraction or archiving, the following are applicable for _unzip_archives_ and _zip_with_dynamic_password_
```python
import multiarchive

archiver_obj = multiarchive.Archiver('skivyttes')

#Example 1: Automatically generate password for each file
archiver_obj.zip_with_dynamic_password('archive_files', pwd=0)

#Example 2: Use a list of password, setting of password will cycle through (see itertools.cycle)
passwords = ['one', 'two', 'three']
archiver_obj.zip_with_dynamic_password('archive_files', pwd=passwords)

#Example 3: Use a single password for all archives
archiver_obj.zip_with_dynamic_password('archive_files', pwd='thisw1llb3th3passw0rd')

#Example 4: Using a password mapping create a json object with the filename and password
#note that if a filename is not found in the mapping, dynamic password will be created instead
pass_map = {'foo.zip': 'fumi', 'bar.zip': 'calter'}
archiver_obj.zip_with_dynamic_password('archive_files', pwd=pass_map)


```

## To do:
- [x] Add Filename and password mapping functionality for customized archive passwords for _zip_with_dynamic_password_
- [x] Add Filename and password mapping functionality for customized archive passwords for _unzip_archives_
- [x] Add functionality for targeting non-archive files (except directories)