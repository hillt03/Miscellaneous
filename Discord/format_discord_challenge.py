import pyperclip


def get_difficulty_string(difficulty):
    difficulty_rating = ""
    if difficulty == "very easy":
        difficulty_rating = "Difficulty Rating: [░░░░]"
    elif difficulty == "easy":
        difficulty_rating = "Difficulty Rating: [▓░░░]"
    elif difficulty == "medium":
        difficulty_rating = "Difficulty Rating: [▓▓░░]"
    elif difficulty == "hard":
        difficulty_rating = "Difficulty Rating: [▓▓▓░]"
    elif difficulty == "impossible":
        difficulty_rating = "Difficulty Rating: [▓▓▓▓]"
    return difficulty_rating

def get_separator():
    return ("-------------------------------------------------------------------------")

def main():
    challenge_number = input("Challenge number: ")
    challenge_title = input("Title: ")
    challenge_information = input("Enter challenge information: ")
    challenge_input = input("Input: ")
    challenge_output = input("Output: ")
    challenge_explanation = input("Explanation: ")
    challenge_difficulty = input("Difficulty (Very Easy/Easy/Medium/Hard/Impossible): ")
    difficulty = challenge_difficulty.lower()
    difficulty_rating = get_difficulty_string(difficulty)

    separator = get_separator()
    pyperclip.copy(f"```\nChallenge #{challenge_number} — {challenge_title}" +
                        f"\n{separator}\n{challenge_information}" +
                        f"\nExample Input:\n{challenge_input}" +
                        f"\nExample Output:\n{challenge_output}\nExplanation:\n{challenge_explanation}" +
                        f"\n{separator}\n\n{difficulty_rating}\n```")
    print("Copied to clipboard.")

if __name__ == "__main__":
    main()
