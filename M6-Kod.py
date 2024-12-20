import random
import json


def splash():
    print("-----------------------------------\n")
    print("\tWelcome to Flashbook")


def view_quizzes(quizzes):
    print("\nThese are your quizzes:\n")
    for keys in quizzes:
        print(keys)


def menu(x): #De 3 möjliga menyerna som kan dyka upp
    if x == 1:
        print("\nl) Login \nc) Create new account \nq) Quit")
    if x == 2:
        print("\nr) Retry \nq) Quit")
    if x == 3:
        print("\np) Practice flashcards \nc) Create new flashcards \nr) Remove flashcards\nl) Log out \nd) Delete account")
    choice = input("\nOption: ").lower()
    return choice


def practice_quiz(quiz, user, points):
    n = 0 # point counter
    repeat = {}
    shuffle = shuffle_quiz(quiz)
    for i in shuffle:
        answer = input(f'\n{i} = ')
        correct_answer = quiz[i]
        if answer == correct_answer:
            print("\nCorrect!")
            n = n+1
        else:
            print(f"\nIncorrect! Answer: {correct_answer}")
            repeat[i] = quiz[i]
    total_points = len(quiz)
    print(f"\nYour points this round: {n}/{total_points}") 
    points[user] = points[user] + n # lägger till samlade poäng i totala poäng
    if len(repeat) > 0:
        new_try = input("\nRepeat wrong answers? y/n ")
        if new_try == "y":
            return points, repeat
    return points, None


def shuffle_quiz(quiz): #Slumpmässig ordning på quizzen
    keys = list(quiz.keys()) #lägg alla "keys" i lista
    random.shuffle(keys)
    return keys


def quiz_option(quizzes):
    view_quizzes(quizzes)
    print("\nWrite the title of a new or existing quiz")
    title = input("\nTitle: ")
    return title  


def create_quiz(quizzes, title): # Funktion för att skapa nytt quiz, lägga till ord och svar
    if title not in quizzes:
        quizzes[title] = {}
    while True:
        word = input("\nWord: ")
        answer = input("\nAnswer: ")
        quizzes[title][word] = answer
        save = input("\nWrite s to save and quit: ")
        if save == "s":
            break
    return quizzes
    

def login(users): # logga in
    while True: 
        user = input("\nUsername: ")
        password = input("Password: ")
        if user not in users or password != users[user]:
            print("\nWrong password or username")
            retry = menu(2)
            if retry == "q": # körs om tills rätt lösen eller quit
                print("quitting.....")
                return retry
        else:
            return user


def create_account(users, points): # skapa nytt konto
    print("\nNew user")
    new_user = input("Username: ")
    new_user_pswrd = input("Password: ")
    users[new_user] = new_user_pswrd # skapar ny användare som tilldelas inskrivet lösenord
    points[new_user] = 0 # startpoäng 0
    return users, points

def remove_account(user, users, points): #
    print("\nRemove account")
    remove_accnt = input("Do you want to remove the account y/n: ")
    if remove_accnt == "y":
        users.pop(user) #ta bort INLOGGAD användare
        points.pop(user)
        print("\nThe account has been removed")
    else:
        print("\nAccount has not been removed")
        return points, users


def remove_words(quizzes):
    remove_wrds = input("\nDo you want to remove a word? y/n: ")
    if remove_wrds == "y":
        view_quizzes(quizzes)
        title = input("\nWhich quiz do you want to remove from? (title): ") # välj vilket quiz som ord ska tas bort från
        if title in quizzes:
            while True:
                word = input("\nWhich word do you want to remove? ")
                if word in quizzes[title]:
                    quizzes[title].pop(word) #ta bort ordet som finns nästlat i dictionary
                    #del quizzes[title][word] 
                    print(f"\nThe word {word} has been removed from {title}")
                else:
                    print(f"\nThe word {word} has not been removed from {title}")
                save = input("\nWrite s to save and quit: ")
                if save == "s":
                    break
        else:
            print(f"The quiz {title} does not exist")
    return quizzes


def leaderboard(points):
    p_sorted = sorted(points.items(), key = lambda x: x[1], reverse = True) # sorterar efter poäng, fallande, .items() retunerar en tuple på form (user, points)
    n = 1                                                                   # key = lambda x: x[1] sorterar utefter andra värdet i tuplen, poängen
    print("\n")
    for user, points in p_sorted: # Skriver ut leaderboarden på rätt sätt
        print("------------------")
        print(f"{n}) {user} {points} p")
        n = n + 1
    print("------------------")


def user_actions(user, quizzes, points, users): 
    print(f"\nWelcome {user}!\n")
    leaderboard(points)
    while True:
        choice = menu(3)
        if choice == "p": # kallar på akutell funktion efter val i meny 3
            view_quizzes(quizzes)
            quiz = input("\nChoose quiz: ")
            try:
                points, repeat = practice_quiz(quizzes[quiz], user, points)
                if type(repeat) == dict:
                    points, repeat = practice_quiz(repeat, user, points)
                leaderboard(points)
            except KeyError:
                 print("\nChoose existing quiz")
        elif choice == "c":
            title = quiz_option(quizzes)
            quizzes = create_quiz(quizzes, title)
        elif choice == "r":
            remove_words(quizzes)
        elif choice == "d":
            points, users = remove_account(user, users, points) 
        elif choice == "l":
            break


def save_data(users, quizzes, points):
    data = [users, quizzes, points]
    with open("FlashBook", 'w') as h:
        json.dump(data, h)


def open_data():
    with open("FlashBook", "r") as file:
        data = json.load(file)
    users = data[0]
    quizzes = data[1]
    points = data[2]
    return users, quizzes, points


def main(): # huvudfunktion
    users, quizzes, points = open_data() # läser av innehållet i flashbook filen
    splash()
    while True:
        choice = menu(1)
        if choice == "q":
            break
        elif choice == "l":
            user = login(users)
            if user == "q":
                break
            user_actions(user, quizzes, points, users)
        elif choice == "c":
            users, points = create_account(users, points)
            continue
    print("Quitting and saving...")
    save_data(users, quizzes, points) # sparar in ändringar i användare, quiz, poäng och lagrar det i flashbookfilen


main()