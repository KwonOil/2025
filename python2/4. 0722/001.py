import os
import time

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

length = 20
half = length//2

outside = []

for i in range(1,length):
    k = i if i <= half else length - i
    bnk = [' ' for _ in range((half - i if i <= half else half - k))]
    star = ['*' for _ in range((2 * k - 1))]
    inside = bnk + star + bnk
    outside.append(inside)


while(True):
    clear_console()
    for i in outside:
        i.append(i.pop(0))
        print(''.join(i))
    time.sleep(0.1)


# for i in range(1,length):
#     k = i if i <= half else length - i
#     bnk = ' ' * (half - i if i <= half else half - k)
#     txt = '*' * (2 * k - 1)
#     outside.append(bnk + txt + bnk)

# while(True):
#     clear_console()
#     for i, val in enumerate(outside):
#         print(val)
#         outside[i] = val[1:] + val[0]
#     time.sleep(0.1)