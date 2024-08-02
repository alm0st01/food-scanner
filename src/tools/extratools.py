import time

def mcq_input(prompt, choices):
    print(prompt,"\n")
    for i in range(len(choices)):
        print(mcq_starters[i]+". "+choices[i])
    while True:
        user_input = input("\nAnswer here: ")

        if user_input in mcq_starters[0:len(choices)]:
            return choices[mcq_starters.index(user_input)]
        elif user_input == "again":
            print(prompt, "\n")
            for i in range(len(choices)):
                print(mcq_starters[i] + ". " + choices[i])
        else:
            print("Please type the letter associated with the answer. Type \"again\" to refresh the question.")



def mcq_inputcor(prompt, choices, answer):
    user_input = mcq_input(prompt, choices)
    if user_input == answer:
        return True
    else:
        return False

def enter_to_continue():
    time.sleep(1)
    input("\n\nPress enter to continue.")
    time.sleep(0.25)

def type_to_continue(prompt, word):
    while True:
        user_input = input(prompt)

        if user_input.strip() == word:
            return True

mcq_starters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
mcq_starters = [*mcq_starters]