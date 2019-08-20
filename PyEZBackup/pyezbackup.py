import os
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import argparse


class PyEZBackup:
    def __init__(self, filepath_file, backup_location):
        self.filepath_list = []
        self.filenames = []  # Excludes path apart from filename
        self.filepath_file = filepath_file
        self.backup_location = backup_location
        self.main_dir = os.getcwd()
        if not os.path.exists(self.backup_location):
            os.mkdir(backup_location)

    def read_filepaths(self):
        """
        Reads filepaths txt doc, updates self.filepaths_list and returns a list of filepaths.
        """
        with open(self.filepath_file, "r") as filepath_txt:
            self.filepath_list = filepath_txt.read().splitlines()
        print("=============================================")
        print("Filepath backup list:")
        for file in self.filepath_list:
            if "." in file:
                print(f"File: {self.get_filename(file)}")
            else:
                print(f"Folder: {self.get_filename(file)}")
        print("=============================================")
        if not self.filepath_list:
            raise Exception("Empty filepath list.")
        for file in self.filepath_list:
            self.filenames.append(self.get_filename(file))
        return self.filepath_list

    def backup_filepaths(self):
        for filepath in self.filepath_list:
            print("Backing up " + self.get_filename(filepath))
            if os.path.isfile(filepath):
                copy_file(filepath, self.backup_location)
            elif os.path.isdir(filepath):
                # self.copytree(filepath, self.backup_location)
                self.copytree(filepath, self.backup_location)
            else:
                print(f"Invalid filepath: {filepath}")

        self._check_backup()

    def copytree(self, src, dst):
        """
        Copies a whole folder and its contents to a destination, creates the directory if it doesn't exist before copying folder contents.
        """
        folder = self.get_filename(src)
        os.chdir(self.backup_location)
        if folder not in os.listdir():
            os.mkdir(self.get_filename(src))
        os.chdir(self.main_dir)
        copy_tree(src, dst + "/" + folder)

    def get_filename(self, filepath):
        return os.path.basename(filepath)

    def _check_backup(self):
        os.chdir(self.backup_location)
        backup_list = os.listdir()
        backup_failed = False
        for file in self.filenames:
            if file not in backup_list:
                print(f"Failed to backup file: {file}")
                backup_failed = True
        if not backup_failed:
            print("Backup successful.")
        os.chdir(self.main_dir)


def main():
    parser = argparse.ArgumentParser(description="Easily backup files and folders.")
    parser.add_argument(
        "-f",
        "--filepath_file",
        metavar="",
        type=str,
        help="Specify path to the text file that contains filepaths which will be backed up.",
    )
    parser.add_argument(
        "-b",
        "--backup_location",
        metavar="",
        type=str,
        help="Specify folder where files will be backed up. The folder will be created if it doesn't exist.",
    )
    args = parser.parse_args()
    filepath_file = (
        args.filepath_file
        if args.filepath_file is not None
        else "config/put_filepath_URLS_here.txt"
    )
    backup_location = (
        args.backup_location if args.backup_location is not None else "backup"
    )
    test = PyEZBackup(filepath_file=filepath_file, backup_location=backup_location)
    test.read_filepaths()
    test.backup_filepaths()


if __name__ == "__main__":
    main()
