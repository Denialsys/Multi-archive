import zipfile
import os
# from dotenv import load_dotenv
from multiarchive.randomstr import Randomizer
import subprocess
import itertools


class Archiver:

    def __init__(self, main_password="SuperSecretMainPassword"):
        """
        Initialization for the archiver class

            :param main_password: Main password for which the dynamic password will be derived
                    on each archive
        """
        self.__base_dir = os.getcwd()
        self.__extraction_path = 'Extracted'
        self.__archival_path = 'Archived'
        self.__archival_path_protected = 'Protected_Archive'
        self.__password_file = 'Password list.txt'
        self.__main_password = main_password

        # 7zip command, 0 - archive name, 1 - target file, 2 - password
        self.__template_cmd = '7z\na\n{0}\n{1}\n-mx5\n-p{2}'
        self.__cmd_special_chars = '(){}&"><|^'

        # If over than 64 chars, it will be encrypted with SHA-1
        # if so, zip file may have two correct passwords
        self.__pwd_len = 62

    def unzip_archives(
            self,
            target_path,
            is_path_relative=True,
            in_file_ext='.zip',
            out_file_ext='.zip',
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
            :param out_file_ext: The output archive file extension
            :param pwd: Password in string or list format, rules:
                    - String type: The single password will be applied to all archive
                    - List type: The password will be mapped as to each archive files
                    - 0 (zero): The password will be dynamic based from the archived name and randomizer
            :return: None
        """
        try:

            # Check if the password type was compliant
            if type(pwd) == list:
                pwd = itertools.cycle(pwd)

            elif type(pwd) == str or pwd == 0 or pwd is None:
                pass

            else:
                print(f'Invalid type of password: {type(pwd)}')
                return

            zip_list = []
            Randomizer_obj = Randomizer()

            if is_path_relative:
                target_extraction_path = os.path.join(self.__base_dir, target_path, self.__extraction_path)
                zip_file_path = os.path.join(self.__base_dir, target_path)
            else:
                target_extraction_path = os.path.join(target_path, self.__extraction_path)
                zip_file_path = target_path

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
                    if type(pwd) == str:
                        zipObj.extractall(current_zip_extraction_path, pwd=bytes(pwd, 'utf-8'))

                    elif type(pwd) == itertools.cycle:
                        zipObj.extractall(current_zip_extraction_path, pwd=bytes(next(pwd), 'utf-8'))

                    elif pwd == 0:

                        dynamic_password = Randomizer_obj.create_random_str(
                            self.__main_password,
                            f'{zip_filename}{in_file_ext}',
                            self.__pwd_len
                        )

                        # Remove the command line special characters
                        for character in self.__cmd_special_chars:
                            dynamic_password = dynamic_password.replace(character, '')

                        try:
                            zipObj.extractall(current_zip_extraction_path, pwd=bytes(dynamic_password, 'utf-8'))
                        except Exception as e:
                            print(f'Failed to extract using password: {dynamic_password}  -- {e.args}')

                    else:
                        try:
                            zipObj.extractall(current_zip_extraction_path)
                        except Exception as e:
                            print(f'Unable to extract: -- {e.args}')

        except Exception as e:
            print(f'Error during decompression of archives: {e.args}')

    def zip_with_dynamic_password(
            self,
            target_path,
            is_path_relative=True,
            password_list=None,
            in_file_ext='.zip'):
        """
        Create multiple password-protected zip files with dynamic and random password
        The target files must be archived, file will be nested but easier to process

        Example usage:
            zip_with_dynamic_password('F:\\Desktop\\items', False)

            :param target_path: Target path where the directories to archive are located
            :param is_path_relative: Meaning the target directory/s path are relative to
                    script path. If set to false, the target_path value must be absolute
            :param password_list: list of password to feed on archiving files
            :param in_file_ext: File format for the archive file
            :return: None
        """

        # Check first if the 7z was on the system
        try:
            subprocess.Popen(['7z'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        except Exception as e:
            print(f'7zip is not available {e.args}')
            return

        # Check first if the list of password is a list type
        if password_list is not None and type(password_list) is not list:
            print(f'Check if the password is a list type')
            return

        Randomizer_obj = Randomizer()
        zip_list = []
        password_list = {}

        if is_path_relative:
            target_archival_path = os.path.join(self.__base_dir, target_path, self.__archival_path_protected)
            file_path = os.path.join(self.__base_dir, target_path)
        else:
            target_archival_path = os.path.join(target_path, self.__archival_path_protected)
            file_path = target_path

        # Gather the files to extract
        for fyl in os.listdir(file_path):
            if fyl.endswith(in_file_ext):
                zip_list.append(os.path.join(file_path, fyl))

        # If the target directory does not exist yet
        if zip_list:
            if not os.path.exists(target_archival_path):
                print(f'Creating output directory: {target_archival_path}')
                os.makedirs(target_archival_path)

        print('-----------')

        for fyl in zip_list:

            # Set the file name, output zip file, the password
            zip_filename = fyl.split(os.sep)[-1]
            output_zip = os.path.join(target_archival_path, zip_filename)
            dynamic_password = Randomizer_obj.create_random_str(
                self.__main_password,
                zip_filename,
                self.__pwd_len
            )

            # Remove the command line special characters
            for character in self.__cmd_special_chars:
                dynamic_password = dynamic_password.replace(character, '')

            # Construct the command to zip file
            print(f'Creating: {output_zip}, password: {dynamic_password}')
            process_cmd = self.__template_cmd.format(output_zip, fyl, dynamic_password)
            process_cmd = process_cmd.split('\n')

            password_list[zip_filename] = dynamic_password

            # Start the compression
            try:
                subprocess.Popen(
                    process_cmd,
                    stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE
                )
            except Exception as e:
                print(f'Error has occurred while archiving {e.args}')

        with open(os.path.join(target_archival_path, self.__password_file), 'w') as password_list_file:
            for file_name in password_list.keys():
                password_list_file.write(f'{file_name} : {password_list[file_name]}\n')

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
            target_archival_path = os.path.join(self.__base_dir, target_path, self.__archival_path)
            file_path = os.path.join(self.__base_dir, target_path)
        else:
            target_archival_path = os.path.join(target_path, self.__archival_path)
            file_path = target_path

        # Create target dir
        if not os.path.exists(target_archival_path):
            print(f'Creating output directory: {target_archival_path}')
            os.makedirs(target_archival_path)

        # Create each archive files
        for root, dirs, files in os.walk(file_path):
            if dirs:
                continue  # Wait the next traversal when target files are the root dirs
            else:
                lambda_package = root.split(os.sep)[-1]

                # Do not include the output directory
                if lambda_package == self.__archival_path:
                    continue

                package_path = os.path.join(target_archival_path, lambda_package)
                print(f'Archiving contents of {package_path}')

                # Use zipFile since multiple script can be inside a lambda package
                with zipfile.ZipFile(package_path + out_file_ext, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file in files:
                        zip_file.write(os.path.join(root, file), file)

    # Setters
    def set_extraction_path(self, extraction_path):
        self.__extraction_path = extraction_path

    def set_archival_path(self, archival_path):
        self.__archival_path = archival_path

    def set_protected_archival_path(self, archival_path):
        self.__archival_path_protected = archival_path
