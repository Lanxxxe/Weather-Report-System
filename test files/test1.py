import random
import time

def generate_random_dtmf():
    dtmf_values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', '*', '#']
    return random.choice(dtmf_values)

dtmf_mapping = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, '*': 14, '#': 15}

while True:
    time.sleep(5)
    
    dtmf_tone = generate_random_dtmf()

    if dtmf_tone != '#':
        decimaal = dtmf_mapping[dtmf_tone]

        print("\033c")  # Clear the screen
        print("\033[1;33;40m  MT8870 - DTMF tone detector")
        print("===============================\033[0m")
        print("The DTMF tone is (" + dtmf_tone + ") =", decimaal)
        print("")

    else:
        print("\033c")  # Clear the screen
        print("\033[1;33;40m  MT8870 - DTMF tone detector")
        print("===============================\033[0m")
        print("The DTMF tone is 'silence'")
        print("")
