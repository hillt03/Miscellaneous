import os
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import argparse
import sys


class PyEZBackup:
    def __init__(self, filepath_file, backup_location):
        self.filepath_list = [] # Stores filepaths that will be backed up
        self.filenames = []  # Excludes path apart from filename
        self.filepath_file = filepath_file # Path to the file containing filepaths to backup
        self.backup_location = backup_location # Path to where folders/files will be backed up
        self.main_dir = os.getcwd() # Stores PyEZBackup location
        if not os.path.exists(self.backup_location):
            os.mkdir(backup_location) # Creates the backup location if it doesn't exist

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
                if "*" in file: # Check for wildcard paths
                    self.add_wildcard_filepaths(file)
                else:
                    print(f"File: {self.get_filename(file)}")
            else:
                print(f"Folder: {self.get_filename(file)}")
        print("=============================================")
        if not self.filepath_list:
            print("Empty filepath list.")
            sys.exit(0)
        for file in self.filepath_list:
            self.filenames.append(self.get_filename(file))
        return self.filepath_list

    def backup_filepaths(self):
        """
        Backs up each file in self.filepath_list to self.backup_location.
        """
        for filepath in self.filepath_list:
            print("Backing up " + self.get_filename(filepath))
            if os.path.isfile(filepath):
                copy_file(filepath, self.backup_location)
            elif os.path.isdir(filepath):
                self.copytree(filepath, self.backup_location)
            else:
                print(f"Invalid filepath: {filepath}")
        self._check_backup()

    def add_wildcard_filepaths(self, filepath):
        extension = os.path.splitext(self.get_filename(filepath))[1]
        for dir_file in self.listdir_fullpath(os.path.dirname(filepath)):
            if dir_file.endswith(extension):
                self.filepath_list.append(dir_file)
        self.filepath_list.remove(filepath)

    def listdir_fullpath(self, d):
        return [os.path.join(d, f) for f in os.listdir(d)]

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
        """
        Removes path from filename.
        """
        return os.path.basename(filepath)

    def _check_backup(self):
        """
        Ensures backup completed successfully.
        """
        print("---------------------------------------------")
        print("Backup results:")
        os.chdir(self.backup_location)
        backup_list = os.listdir()
        backup_failed = False
        for file in self.filenames:
            if file not in backup_list:
                print(f"Failed to backup file: {file}")
                backup_failed = True
        if not backup_failed:
            print("Backup successful.")
        print("---------------------------------------------")
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
