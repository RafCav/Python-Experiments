import pandas as pd
import pyautogui
import time
import pyperclip

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# LOCATIONS (22% zoom)
PAGE1 = (400, 900)
TITLE = (1010, 350)
SUBTITLE = (970, 380)
QUESTION = (1000, 480)
ANS1 = (940, 635)
ANS1_BLOCK = (940, 650)
ANS2 = (940, 685)
ANS2_BLOCK = (940, 700)
ANS3 = (940, 730)
ANS3_BLOCK = (940, 745)
ANIMATE_BTM = (1350, 255)
BLANK_SPACE = (1600, 560)
BLOCKS = {ANS1: ANS1_BLOCK, ANS2: ANS2_BLOCK, ANS3: ANS3_BLOCK}

A_MENU_SCROLL_BAR = (530, 990)
A_PULSE_BTM = (430, 740)
A_REMOVE_BTM = (430, 970)
ANS_BLOCK_COLOR = (770, 255)
ANS_BLOCK_COLOR_YELLOW = (200, 520)
ANS_BLOCK_COLOR_ORANGE = (130, 520)

# EXECUTIONS QUEUE
TESTING_ORDER = [PAGE1, TITLE, SUBTITLE, QUESTION, ANS1, ANS1_BLOCK, ANS2, ANS2_BLOCK, ANS3, ANS3_BLOCK]
TEXT_ALTERATION_ORDER = [TITLE, SUBTITLE, QUESTION, ANS1, ANS2, ANS3]


def switch_page():
    time.sleep(1)
    pyautogui.moveTo(BLANK_SPACE)
    pyautogui.keyDown('alt')  # Press and hold 'Alt'
    pyautogui.press('tab')  # Press and release 'tab'
    pyautogui.keyUp('alt')  # Release 'Alt'
    time.sleep(0.1)


def location_testing():
    for location in TESTING_ORDER:
        pyautogui.moveTo(location, duration=0.5)
        if location == ANS3:  # When reach text of third answer option, try effects
            pyautogui.click()
            for loc2 in [ANIMATE_BTM, A_MENU_SCROLL_BAR, A_REMOVE_BTM, A_PULSE_BTM]:
                pyautogui.moveTo(loc2, duration=0.5)
                if loc2 == ANIMATE_BTM:
                    pyautogui.click()
                if loc2 == A_MENU_SCROLL_BAR:
                    pyautogui.mouseDown()
                    time.sleep(0.5)
                    pyautogui.mouseUp()
        if location == ANS3_BLOCK:
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(ANS_BLOCK_COLOR, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(ANS_BLOCK_COLOR_YELLOW, duration=0.5)
            time.sleep(0.5)
            pyautogui.moveTo(ANS_BLOCK_COLOR_ORANGE, duration=0.5)

        time.sleep(0.5)
    pyautogui.click(BLANK_SPACE)


def edit_page(data, page):
    # Change all text first
    for index, loc in enumerate(TEXT_ALTERATION_ORDER):
        column_value = list(data.values())[index]
        pyperclip.copy(column_value)
        pyautogui.doubleClick(loc)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.click(BLANK_SPACE)

    # Turn on or off the affects
    if page % 2 != 0:
        # Define a helper function for repeated actions

        def pulse_effect(activate):
            pyautogui.moveTo(A_MENU_SCROLL_BAR, duration=0.2)
            pyautogui.mouseDown()
            time.sleep(0.5)
            pyautogui.mouseUp()
            time.sleep(0.5)
            pyautogui.moveTo(A_REMOVE_BTM, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(A_PULSE_BTM, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)
            if not activate:
                pyautogui.moveTo(A_REMOVE_BTM, duration=0.2)
                pyautogui.click()

        # Loop through the answers
        for loc, op in [(ANS1, 'A'), (ANS2, 'B'), (ANS3, 'C')]:
            is_correct = (op == data['ANS'])

            pyautogui.moveTo(loc, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(ANIMATE_BTM, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)
            pulse_effect(is_correct)
            time.sleep(0.5)

            pyautogui.moveTo(BLOCKS[loc], duration=0.2)
            pyautogui.click()
            time.sleep(0.5)
            pulse_effect(is_correct)
            time.sleep(0.5)
            pyautogui.moveTo(ANS_BLOCK_COLOR, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(ANS_BLOCK_COLOR_ORANGE if is_correct else ANS_BLOCK_COLOR_YELLOW, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)


def main():
    screen_width, screen_height = pyautogui.size()  # Screen Size
    print(f"Largura: {screen_width}, Altura: {screen_height}")

    # Get Dataframe https://docs.google.com/spreadsheets/d/1ougkayhtVRRCc88jWGRMFdTBBM7AafbSEZsdqCRVwJE
    sheet_id = '1ougkayhtVRRCc88jWGRMFdTBBM7AafbSEZsdqCRVwJE'
    df_original = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    duplicated_df = df_original.copy()
    df = pd.concat([df_original, duplicated_df], ignore_index=True).sort_values(by='page')

    print(df)

    time.sleep(10)

    switch_page()

    # location_testing()

    time.sleep(10)

    for i in range(len(df)):
        if i == 0:  # Only first loop
            pyautogui.click(PAGE1)
        else:
            pyautogui.scroll(-100)

        payload = {
            'TITLE': df['title'].iloc[i],
            'SUBTITLE': df['subtitle'].iloc[i],
            'QUSTIONS': df['question'].iloc[i],
            'ANS1': 'A) ' + str(df['op1'].iloc[i]),
            'ANS2': 'B) ' + str(df['op2'].iloc[i]),
            'ANS3': 'C) ' + str(df['op3'].iloc[i]),
            'ANS': df['answer'].iloc[i]
        }

        time.sleep(0.5)
        edit_page(payload, i)
        time.sleep(0.5)

        pyautogui.click(BLANK_SPACE)
        time.sleep(0.5)


main()
