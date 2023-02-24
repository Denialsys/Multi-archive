import zipfile
import os
# from dotenv import load_dotenv
import random_string
import subprocess


class Archiver:
    def __init__(self, main_password="SuperSecretMainPassword"):
        self.__base_dir = os.getcwd()
        self.__extraction_path = 'Extracted'
        self.__archival_path = 'Archived'
        self.__archival_path_protected = 'Protected_Archive'
        self.__main_password = main_password

    def set_extraction_path(self, extraction_path):
        self.__extraction_path = extraction_path

    def set_archival_path(self, archival_path):
        self.__archival_path = archival_path

    def unzip_archives(
            self,
            target_path,
            is_path_relative = True,
            in_file_ext='.zip',
            out_file_ext='.zip',
            pwd=None):

        """
        Will collect and extract all the archive file from the specified path.
        Will create a directory for the output extracted files

        Example usage:
            unzip_archives('targ\\items')
            unzip_archives('h:\\Desktop\\test', False)

            :param target_path: The target location where archive files are located
                    (if nested use double slash '\\' for windows).
            :param is_path_relative: Meaning the archive file/s path are relative to script path
                    If set to false, the target_path value must be absolute
            :param in_file_ext: The input archive file extension
            :param out_file_ext: The output archive file extension
            :param pwd: Password in string format, Note that this password will be used to all archives

            :return: None
        """

        zip_list = []

        if is_path_relative:
            target_extraction_path = os.path.join(base_dir, target_path, self.__extraction_path)
            zip_file_path = os.path.join(base_dir, target_path)
        else:
            target_extraction_path = os.path.join(target_path, self.__extraction_path)
            zip_file_path = target_path

        print(f'\nBase Directory {self.__base_dir}')
        print(f'Target extraction path {target_extraction_path}')

        # Gather the files to extract
        for fyl in os.listdir(zip_file_path):
            if fyl.endswith(in_file_ext):
                zip_list.append(os.path.join(zip_file_path, fyl))

        # If the target directory does not exist yet
        if zip_list:
            if not os.path.exists(target_extraction_path):
                print(f'Creating output directory: {target_extraction_path}')
                os.makedirs(target_extraction_path)

        print('-----------')

        # Begin the extraction
        for fyl in zip_list:
            print(f'Extracting: {fyl}')

            zip_filename = fyl.split(os.sep)[-1].replace(out_file_ext, '')
            current_zip_extraction_path = os.path.join(target_extraction_path, zip_filename)

            # Extract all the contents of zip file into target directory
            # Use password if password was specified
            with zipfile.ZipFile(fyl, 'r') as zipObj:
                if pwd:
                    zipObj.extractall(current_zip_extraction_path, pwd=bytes(pwd, 'utf-8'))
                else:
                    zipObj.extractall(current_zip_extraction_path)



