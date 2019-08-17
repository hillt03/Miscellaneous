def ask(question):
    question = question + " "
    confirmation = ["y", "yes"]
    user_input = input(question)
    return True if user_input.lower() in confirmation else False


if __name__ == "__main__":
    number_of_questions = 0
    chapters_in_use = False
    different_number_of_questions_in_chapters = False
    custom_chapter_numbers = False
    amount_of_chapters = 0
    chapters_and_number_of_questions = {}
    custom_chapter_numbers_list = [] # Used if there's not a different amount of questions
    custom_chapter_numbers_dict = {} # Contains chapter number as key and number of questions as value

    if ask("Would you like to separate the questions into chapters? (Yes/No):"):
        chapters_in_use = True
        if ask("Is there a different amount of questions in each chapter?"):
            different_number_of_questions_in_chapters = True

        if ask("Custom chapter numbers? (e.g. not 1,2,3 but 5,13,15, etc.):"):
            custom_chapter_numbers = True
            if not different_number_of_questions_in_chapters:
                adding_chapters = True
                print("===Enter your chapter numbers, enter 'x' when done===")
                while adding_chapters:
                    chapter_number = input()
                    if chapter_number != "x":
                        custom_chapter_numbers_list.append(chapter_number)
                    else:
                        adding_chapters = False

        if not custom_chapter_numbers:
            amount_of_chapters = int(input("Enter the amount of chapters: "))

        if not different_number_of_questions_in_chapters:
            number_of_questions = int(
                input("Enter how many questions are in each chapter: ")
            )
        else:
            if custom_chapter_numbers:
                print(
                    "Enter your chapter numbers and number of questions in the chapter, enter 'x' for chapter number when done"
                )
                adding_chapters = True

                while adding_chapters:
                    print("========")
                    chapter_number = input("Chapter number: ")
                    if chapter_number == "x":
                        adding_chapters = False
                        break
                    questions_in_chapter = input("Questions in chapter: ")
                    print("========")
                    custom_chapter_numbers_dict[chapter_number] = int(
                        questions_in_chapter
                    )
            else:
                for chapter in range(1, amount_of_chapters + 1):
                    chapters_and_number_of_questions[chapter] = int(
                        input(f"Enter the amount of questions in chapter {chapter}: ")
                    )
    else:
        number_of_questions = int(input("Enter the number of questions: "))

    with open("your_quiz.txt", "w") as file:
        if (
            chapters_in_use
            and not different_number_of_questions_in_chapters
            and not custom_chapter_numbers
        ):
            for chapter in range(1, amount_of_chapters + 1):
                file.write("Chapter " + str(chapter) + "\n\n")
                for i in range(1, number_of_questions + 1):
                    file.write(str(i) + ". \n")
                file.write("\n")
        elif (
            chapters_in_use
            and different_number_of_questions_in_chapters
            and not custom_chapter_numbers
        ):
            for chapter, number_of_qs in chapters_and_number_of_questions.items():
                file.write("Chapter " + str(chapter) + "\n\n")
                for i in range(1, number_of_qs + 1):
                    file.write(str(i) + ". \n")
                file.write("\n")
        elif custom_chapter_numbers and different_number_of_questions_in_chapters:
            for chapter, number_of_qs in custom_chapter_numbers_dict.items():
                file.write("Chapter " + str(chapter) + "\n\n")
                for i in range(1, number_of_qs + 1):
                    file.write(str(i) + ". \n")
                file.write("\n")
        elif custom_chapter_numbers and not different_number_of_questions_in_chapters:
            for chapter in custom_chapter_numbers_list:
                file.write("Chapter " + str(chapter) + "\n\n")
                for i in range(1, number_of_questions + 1):
                    file.write(str(i) + ". \n")
                file.write("\n")
        else:
            for i in range(1, number_of_questions + 1):
                file.write(str(i) + ". \n")

    print("Finished.")
