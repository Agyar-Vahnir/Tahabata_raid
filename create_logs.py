import pyautogui
import time

def process_name(delay):
    time.sleep(delay)
    pyautogui.click()
    pyautogui.click()
    pyautogui.click()
    time.sleep(delay)
    pyautogui.hotkey("ctrl","c")
    pyautogui.hotkey("ctrl","c")
    pyautogui.hotkey("ctrl","c")
    time.sleep(delay)
    pyautogui.hotkey("alt","tab")
    time.sleep(delay)
    pyautogui.hotkey("ctrl","v")
    time.sleep(delay)
    pyautogui.hotkey("enter")
    time.sleep(delay)


def process_log(delay):
    time.sleep(delay)
    pyautogui.click()
    pyautogui.click()
    pyautogui.click()
    time.sleep(delay)
    pyautogui.hotkey("ctrl","a")
    time.sleep(delay)
    pyautogui.hotkey("ctrl","c")
    pyautogui.hotkey("ctrl","c")
    pyautogui.hotkey("ctrl","c")
    time.sleep(delay)
    pyautogui.hotkey("alt","tab")
    time.sleep(delay)
    pyautogui.hotkey("ctrl","v")
    time.sleep(delay)
    pyautogui.hotkey("enter")
    time.sleep(delay)


def create_log_file(nb_logs):
    nb_shifts = (nb_logs-9)//3-1*((nb_logs)%3==0)
    final_remain = (nb_logs-9)%3
    poslogs = [500,200]
    pos_case = [[100,170],
        [100,215],
        [100,261],
        [100,306],
        [100,352],
        [100,397],
        [100,443],
        [100,488],
        [100,534],
        [100,579],
        [100,615],
        [100,670]
    ]
    delay = 0.4
    


    ## Initial 9
    for i in range(9):
        pyautogui.moveTo(pos_case[i][0], pos_case[i][1])
        process_name(delay)
        pyautogui.moveTo(poslogs[0], poslogs[1])
        process_log(delay)

    for shift_num in range(nb_shifts):
        for i in [-3,-2,-1]:
            pyautogui.moveTo(pos_case[i][0], pos_case[i][1])
            process_name(delay)
            pyautogui.moveTo(poslogs[0], poslogs[1])
            process_log(delay)
        pyautogui.moveTo(pos_case[0][0], pos_case[0][1])
        time.sleep(delay)
        pyautogui.scroll(-1)
        time.sleep(delay)

    
    for i in [-3,-2,-1][-1*final_remain:]:
        pyautogui.moveTo(pos_case[i][0], pos_case[i][1])
        process_name(delay)
        pyautogui.moveTo(poslogs[0], poslogs[1])
        process_log(delay)

poslogs = [500,200]
pos_case = [[100,170],
    [100,215],
    [100,261],
    [100,306],
    [100,352],
    [100,397],
    [100,443],
    [100,488],
    [100,534],
    [100,579],
    [100,615],
    [100,670]
]            

time.sleep(4)
create_log_file(677)
