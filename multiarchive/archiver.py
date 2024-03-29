import zipfile
import os
from multiarchive.randomstr import Randomizer
import subprocess
import itertools
import logging

class Archiver:

    def __init__(self, main_password="SuperSecretMainPassw0rd"):
        """
        Initialization for the archiver class

            :param main_password: Main password for which the dynamic password will be derived
                    on each archive

            Current supported platform: Windows
        """
        self.__base_dir = os.getcwd()
        self.__extraction_dir = 'Extracted'
        self.__archival_dir = 'Archived'
        self.__archival_dir_protected = 'Protected_Archive'
        self.__archive_output_extension = '.zip'
        self.__password_file = 'Password list.txt'
        self.__main_password = main_password

        # 7zip command, 0 - archive name, 1 - target file, 2 - password
        self.__template_cmd = '7z\na\n{0}\n{1}\n-mx5\n-p{2}'
        self.__cmd_special_chars = {ord(x): None for x in '(){}&\'"><|^'}

        # If over than 64 chars, it will be encrypted with SHA-1
        # if so, zip file may have two correct passwords
        self.__pwd_len = 62

        self.__generate_password_file = False
        self.__randomizer_obj = Randomizer()

    def __create_protected_archive(self, output_file, input_file, password):

        # Construct the command to zip file
        logging.debug(f'Creating: {output_file}, password: {password}')
        process_cmd = self.__template_cmd.format(output_file, input_file, password)
        process_cmd = process_cmd.split('\n')

        # Start the compression
        try:
            subprocess.Popen(
                process_cmd,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE
            )
        except Exception as e:
            logging.warning(f'Failed to archive {output_file} -- {e.args}')

    def __create_dynamic_password(self, zip_filename):
        dynamic_password = self.__randomizer_obj.create_random_str(
            self.__main_password,
            zip_filename,
            self.__pwd_len
        )

        # Remove the command line special characters
        dynamic_password = dynamic_password.translate(self.__cmd_special_chars)
        return dynamic_password

    def unzip_archives(
            self,
            target_path,
            is_path_relative=True,
            in_file_ext='.zip',
            pwd=None):

        """
        Will collect and extract all the archive file from the specified path.
        Will create a directory for the output extracted files
        This function can accept a single password or list of passwords for
        extraction of zip files with each their own password

        Example usage:
            unzip_archives('targ\\items')
            unzip_archives('h:\\Desktop\\test', False)
            unzip_archives('h:\\Desktop\\test', pwd=['junioe', 'caresui'])

            :param target_path: The target location where archive files are located
                    (if nested use double slash '\\' for windows).
            :param is_path_relative: Meaning the archive file/s path are relative to script path
                    If set to false, the target_path value must be absolute
            :param in_file_ext: The input archive file extension
            :param pwd: Password in string or list format, rules:
                    - String type: The single password will be applied to all archive
                    - List type: Each password will be cycled to each archive files
                    - Json type: Each file will be extracted using the password specified to its
                            filename
                    - 0 (zero): The password will be dynamic based from the archived name and randomizer
            :return: None
        """
        try:

            # Check if the password type was compliant
            if type(pwd) == list:
                pwd = itertools.cycle(pwd)

            elif type(pwd) == str or pwd == 0 or pwd is None or type(pwd) == dict:
                pass

            else:
                logging.error(f'Invalid type of password: {type(pwd)}')
                return

            zip_list = []

            if is_path_relative:
                target_extraction_path = os.path.join(self.__base_dir, target_path, self.__extraction_dir)
                zip_file_path = os.path.join(self.__base_dir, target_path)
            else:
                target_extraction_path = os.path.join(target_path, self.__extraction_dir)
                zip_file_path = target_path

            # Gather the files to extract
            for fyl in os.listdir(zip_file_path):
                if fyl.endswith(in_file_ext):
                    zip_list.append(os.path.join(zip_file_path, fyl))

            if not len(zip_list):
                logging.info('Nothing to archive')
                return

            if zip_list:
                if not os.path.exists(target_extraction_path):
                    logging.debug(f'Creating output directory: {target_extraction_path}')
                    os.makedirs(target_extraction_path)

            # Begin the extraction
            for fyl in zip_list:
                logging.debug(f'Extracting: {fyl}')
                zip_filename = os.path.splitext(os.path.basename(fyl))[0]

                # Extract all the contents of zip file into target directory
                with zipfile.ZipFile(fyl, 'r') as zipObj:
                    if type(pwd) == str:
                        zipObj.extractall(target_extraction_path, pwd=bytes(pwd, 'utf-8'))

                    elif type(pwd) == itertools.cycle:
                        zipObj.extractall(target_extraction_path, pwd=bytes(next(pwd), 'utf-8'))

                    elif pwd == 0:
                        dynamic_password = self.__create_dynamic_password(f'{zip_filename}{in_file_ext}')

                        try:
                            zipObj.extractall(target_extraction_path, pwd=bytes(dynamic_password, 'utf-8'))
                        except Exception as e:
                            logging.warning(f'Extraction failed with: {dynamic_password}  -- {e.args}')

                    elif type(pwd) == dict:
                        try:
                            assigned_password = pwd[f'{zip_filename}{in_file_ext}']

                        except KeyError:
                            assigned_password = self.__create_dynamic_password(f'{zip_filename}{in_file_ext}')

                        try:
                            zipObj.extractall(target_extraction_path, pwd=bytes(assigned_password, 'utf-8'))

                        except Exception as e:
                            logging.warning(f'Extraction failed with: {dynamic_password}  -- {e.args}')

                    else:
                        try:
                            zipObj.extractall(os.path.join(target_extraction_path, zip_filename))
                        except Exception as e:
                            logging.warning(f'Unable to extract: -- {e.args}')

        except Exception as e:
            logging.error(f'Error during extracting of archives: {e.args}')

    def zip_with_dynamic_password(
            self,
            target_path,
            is_path_relative=True,
            pwd=0,
            in_file_ext='*'):
        """
        Create multiple password-protected zip files with dynamic and random password
        The target files must be archived, file will be nested but easier to process

        Note: Gathered file to be archived are sorted alphabetically

        Example usage:
            zip_with_dynamic_password('F:\\Desktop\\items', False)

            :param target_path: Target path where the directories to archive are located
            :param is_path_relative: Meaning the target directory/s path are relative to
                    script path. If set to false, the target_path value must be absolute
            :param pwd: Password in string, json or list format, rules:
                    - String type: The single password will be applied to all archive, will be
                            sanitized for allowable characters
                    - List type: Each password will be cycled to each archive files, all
                            elements must be string and will be sanitized for allowable characters
                    - Json type: Each file will be archived using the password specified to its
                            filename, if no password was found, dynamic password will be generated,
                            each password must be string and will be sanitized for allowable characters
                    - 0 (zero): The password will be dynamic based from the archived name and randomizer
            :param in_file_ext: File format of the target files to archive
            :return: None
        """

        # Check first if the 7z was on the system
        try:
            subprocess.Popen(['7z'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        except Exception as e:
            logging.critical(f'7zip is not available {e.args}')
            return

        if pwd == 0:
            pass

        elif type(pwd) == str:
            pwd = pwd.translate(self.__cmd_special_chars)

        elif type(pwd) == list:
            raw_pass = [password.translate(self.__cmd_special_chars) for password in pwd]
            pwd = itertools.cycle(raw_pass)

        elif type(pwd) == dict:
            for pwd_key in pwd.keys():
                pwd[pwd_key] = pwd[pwd_key].translate(self.__cmd_special_chars)

        else:
            logging.error(f'Invalid type of password: {type(pwd)}')
            return

        zip_list = []
        pwd_list = {}

        if is_path_relative:
            target_archival_path = os.path.join(self.__base_dir, target_path, self.__archival_dir_protected)
            file_path = os.path.join(self.__base_dir, target_path)
        else:
            target_archival_path = os.path.join(target_path, self.__archival_dir_protected)
            file_path = target_path

        # Gather the files to archive
        for fyl in os.listdir(file_path):
            if in_file_ext == '*' or in_file_ext == '.*':
                if os.path.isfile(os.path.join(file_path, fyl)):
                    zip_list.append(os.path.join(file_path, fyl))

            else:
                if fyl.endswith(in_file_ext):
                    zip_list.append(os.path.join(file_path, fyl))

        # If the target directory does not exist yet
        if zip_list:
            if not os.path.exists(target_archival_path):
                logging.info(f'Creating output directory: {target_archival_path}')
                os.makedirs(target_archival_path)

        for fyl in zip_list:
            # Set the file type to output file
            zip_filename = os.path.splitext(os.path.basename(fyl))[0] + self.__archive_output_extension

            output_zip = os.path.join(target_archival_path, zip_filename)
            processed_password = ''

            if pwd == 0:
                processed_password = self.__create_dynamic_password(zip_filename)

            elif type(pwd) == str:
                processed_password = pwd

            elif type(pwd) == itertools.cycle:
                processed_password = next(pwd)

            elif type(pwd) == dict:
                try:
                    processed_password = pwd[os.path.basename(fyl)]

                except KeyError:
                    processed_password = self.__create_dynamic_password(zip_filename)

            self.__create_protected_archive(output_zip, fyl, processed_password)
            pwd_list[zip_filename] = processed_password

        if not len(zip_list):
            logging.info('Nothing to archive')
            return

        if self.__generate_password_file:
            with open(os.path.join(target_archival_path, self.__password_file), 'w') as pwd_list_file:
                for file_name in pwd_list.keys():
                    pwd_list_file.write(f'{file_name} : {pwd_list[file_name]}\n')

    def zip_lambdas(
            self,
            target_path,
            is_path_relative=True,
            out_file_ext='.zip'):

        """
        Compress the extracted lambda files, will create an archive file similar to the
        exported archive file of AWS Lambda (No password), the package must be a directory with
        lambda script inside. This can be used for AWS Lambda backup

        Example usage:
            zip_lambdas('targ\\items\\Extracted')
            zip_lambdas('h:\\Desktop\\test', False)

            :param target_path: Target path where the directories to archive are located
            :param is_path_relative: Meaning the target directory/s path are relative to
                    script path. If set to false, the target_path value must be absolute
            :param out_file_ext: File format for the archive file
            :return: None
        """

        if is_path_relative:
            target_archival_path = os.path.join(self.__base_dir, target_path, self.__archival_dir)
            file_path = os.path.join(self.__base_dir, target_path)
        else:
            target_archival_path = os.path.join(target_path, self.__archival_dir)
            file_path = target_path

        # Create target dir
        if not os.path.exists(target_archival_path):
            logging.debug(f'Creating output directory: {target_archival_path}')
            os.makedirs(target_archival_path)

        # Create each archive files
        for root, dirs, files in os.walk(file_path):
            if dirs:
                continue  # Wait the next traversal when target files are the root dirs
            else:
                lambda_package = root.split(os.sep)[-1]

                # Do not include the output directory
                if lambda_package == self.__archival_dir:
                    continue

                package_path = os.path.join(target_archival_path, lambda_package)
                logging.debug(f'Archiving contents of {package_path}')

                # Use zipFile since multiple script can be inside a lambda package
                with zipfile.ZipFile(package_path + out_file_ext, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file in files:
                        zip_file.write(os.path.join(root, file), file)

    # Setters
    def set_extraction_path(self, extraction_path):
        self.__extraction_dir = extraction_path

    def set_archival_path(self, archival_path):
        self.__archival_dir = archival_path

    def set_protected_archival_path(self, archival_path):
        self.__archival_dir_protected = archival_path

    def set_password_file_creation(self, is_enabled):
        self.__generate_password_file = is_enabled

    def set_archive_output_extension(self, extnsn):
        self.__archive_output_extension = extnsn

    def set_verbose(self, is_enabled):
        if is_enabled:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)
