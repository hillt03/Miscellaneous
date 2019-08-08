number_of_questions = 0
chapters_in_use_prompt = input(
    "Would you like to separate the questions into chapters? (Yes/No): "
)
confirmation = ["y", "yes"]
chapters_in_use = False
different_number_of_questions_in_chapters = False
amount_of_chapters = 0
chapters_and_number_of_questions = {}
if chapters_in_use_prompt.lower() in confirmation:
    chapters_in_use = True
    if (
        input("Is there a different amount of questions in each chapter?").lower()
        in confirmation
    ):
        different_number_of_questions_in_chapters = True
    amount_of_chapters = int(input("Enter the amount of chapters: "))
    if not different_number_of_questions_in_chapters:
        number_of_questions = int(
            input("Enter how many questions are in each chapter: ")
        )
    else:
        for chapter in range(1, amount_of_chapters + 1):
            chapters_and_number_of_questions[chapter] = int(
                input(f"Enter the amount of questions in chapter {chapter}: ")
            )
else:
    number_of_questions = int(input("Enter the number of questions: "))


with open("your_quiz.txt", "w") as file:
    if chapters_in_use and not different_number_of_questions_in_chapters:
        for chapter in range(1, amount_of_chapters + 1):
            file.write("Chapter " + str(chapter) + "\n\n")
            for i in range(1, number_of_questions + 1):
                file.write(str(i) + ". \n")
            file.write("\n")

    elif chapters_in_use and different_number_of_questions_in_chapters:
        for chapter, number_of_qs in chapters_and_number_of_questions.items():
            file.write("Chapter " + str(chapter) + "\n\n")
            for i in range(1, number_of_qs + 1):
                file.write(str(i) + ". \n")
            file.write("\n")
    else:
        for i in range(1, number_of_questions + 1):
            file.write(str(i) + ". \n")

print("Finished.")
