"""
A script to automate folder creation.
"""
import os

def get_initial_path():
    invalid_initial_path = True
    initial_path = ''
    while invalid_initial_path:
        initial_path = input('Folder path: ')
        if os.path.isdir(initial_path):
            invalid_initial_path = False
        else:
            print("That directory doesn't exist, enter a valid path.")
    return initial_path


def get_subfolder_names():
    invalid_number = True
    folder_names = []
    number_of_subfolders = ''
    while invalid_number:
        number_of_subfolders = input("Number of subfolders: ")
        if not number_of_subfolders.isdigit():
            print("That's not a valid number. Try again.")
            continue
        else:
            invalid_number = False
    for folder in range(int(number_of_subfolders)):
        folder_names.append(input(f"Enter the name of subfolder {folder+1}: "))
    return folder_names


def create_folder_structure(path, root_name, sub_names):
    os.chdir(path)
    os.mkdir(root_name)
    os.chdir(root_name)
    for folder in sub_names:
        os.mkdir(folder)


print("Welcome to PyjectX\n")

print("Enter the folder path where you'd like to begin your project.")
print(r"Example: C:\Users\Tim\Desktop\Python")
project_path = get_initial_path()

print("Enter the name of the folder your project will be stored in.")
project_name = input("Project name: ")

print("How many subfolders would you like?")
subfolder_names = get_subfolder_names()

print("Working...")
create_folder_structure(project_path, project_name, subfolder_names)


input("Completed successfully. Press enter to exit.")
