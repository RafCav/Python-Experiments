import pandas as pd
import pyautogui
import time
import pyperclip

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def create_video(df):
    def switch_page():
        time.sleep(1)
        pyautogui.moveTo(800, 450)
        pyautogui.keyDown('alt')  # Press and hold 'Alt'
        pyautogui.press('tab')  # Press and release 'tab'
        pyautogui.keyUp('alt')  # Release 'Alt'
        time.sleep(0.1)

    def effect_control(x_coord, y_coord, op, ans):
        def effect():
            pyautogui.moveTo(420, 800, duration=0.5)
            time.sleep(0.3)
            pyautogui.mouseDown()
            time.sleep(0.5)
            pyautogui.mouseUp()

            time.sleep(0.3)
            pyautogui.moveTo(350, 815, duration=0.5)
            pyautogui.click()  # Remove Effect Button
            time.sleep(0.3)
            pyautogui.moveTo(350, 630, duration=0.5)
            pyautogui.click()  # Effect Button

        print(f"op: {op} | ans: {ans}")
        if op == ans:
            print('Ativa o efeito')
            pyautogui.moveTo(1100, 205, duration=0.5)  # Botão "Animar"
            pyautogui.click()
            time.sleep(0.3)
            effect()
            time.sleep(0.3)
            pyautogui.moveTo(x_coord, y_coord + 15, duration=0.5)
            pyautogui.click()  # Text
            time.sleep(0.3)
            effect()
            time.sleep(0.3)
            pyautogui.moveTo(610, 205, duration=0.5)
            pyautogui.click()  # Colors
            time.sleep(0.3)
            pyautogui.moveTo(110, 415, duration=0.5)
            pyautogui.click()  # Effect Color
        else:
            print('Desativa o efeito')
            pyautogui.moveTo(1100, 205, duration=0.5)  # Botão "Animar"
            pyautogui.click()
            time.sleep(0.3)
            effect()
            time.sleep(0.3)
            pyautogui.moveTo(350, 815, duration=0.5)
            pyautogui.click()  # Remove Effect Button
            time.sleep(0.3)
            pyautogui.moveTo(x_coord, y_coord + 15, duration=0.5)
            pyautogui.click()  # Text Card
            time.sleep(0.3)
            effect()
            time.sleep(0.3)
            pyautogui.moveTo(350, 815, duration=0.5)
            pyautogui.click()  # Remove Effect Button
            time.sleep(0.3)
            pyautogui.moveTo(610, 205, duration=0.5)
            pyautogui.click()  # Colors
            time.sleep(0.3)
            pyautogui.moveTo(165, 415, duration=0.5)
            pyautogui.click()  # No Effect Color

        time.sleep(0.3)

    def edit_page(data, page):  # Beware the Zoom
        # ------------------- TITLE
        pyautogui.moveTo(860, 285, duration=0.5)
        pyperclip.copy(data['title'])  # Copy the text I nedd
        pyautogui.doubleClick()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')  # select all
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')  # paste
        time.sleep(0.1)
        pyautogui.click(500, 500)  # Exit Text
        time.sleep(0.1)

        # ------------------- SUBTITLE
        pyautogui.moveTo(820, 315, duration=0.5)
        pyperclip.copy(data['subtitle'])
        pyautogui.doubleClick()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.click(500, 500)
        time.sleep(0.1)

        # ------------------- QUESTION
        pyautogui.moveTo(840, 420, duration=0.5)
        pyperclip.copy(data['question'])
        pyautogui.doubleClick()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.click(500, 500)
        time.sleep(0.1)

        # ------------------- OP1
        pyautogui.moveTo(790, 530, duration=0.5)
        pyperclip.copy('A) ' + data['op1'])
        pyautogui.doubleClick()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)

        if not page % 2 == 0:  # If the page is odd
            effect_control(790, 530, 'A', data['answer'])
            time.sleep(0.5)

        pyautogui.click(500, 500)
        time.sleep(0.1)

        # ------------------- OP2
        pyautogui.moveTo(790, 575, duration=0.5)
        pyperclip.copy('B) ' + data['op2'])
        pyautogui.doubleClick()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)

        if not page % 2 == 0:  # If the page is odd
            effect_control(790, 575, 'B', data['answer'])
            time.sleep(0.5)

        pyautogui.click(500, 500)
        time.sleep(0.1)

        # ------------------- OP3
        pyautogui.moveTo(790, 615, duration=0.5)
        pyperclip.copy('C) ' + data['op3'])
        pyautogui.doubleClick()
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)

        if not page % 2 == 0:  # If the page is odd
            effect_control(790, 615, 'C', data['answer'])
            time.sleep(0.5)

        pyautogui.click(500, 500)
        time.sleep(0.1)

    screen_width, screen_height = pyautogui.size()  # Screen Size
    print(f"Largura: {screen_width}, Altura: {screen_height}")

    # ------------------- BROWSER

    switch_page()

    # ------------------- OTHER PAGES

    for i in range(10):
        if i == 0:  # Only first loop
            pyautogui.moveTo(250, 750, duration=0.5)  # Página 1
            time.sleep(3)
            pyautogui.click()
        else:
            pyautogui.moveTo(360, 500, duration=0.5)  # Blank space
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.scroll(-100)

        payload = {
            'title': df['title'].iloc[i],
            'subtitle': df['subtitle'].iloc[i],
            'question': df['question'].iloc[i],
            'op1': df['op1'].iloc[i],
            'op2': df['op2'].iloc[i],
            'op3': df['op3'].iloc[i],
            'answer': df['answer'].iloc[i]
        }

        time.sleep(0.5)
        edit_page(payload, i)


def main():

    # Get Dataframe
    sheet_id = '1ougkayhtVRRCc88jWGRMFdTBBM7AafbSEZsdqCRVwJE'
    df_original = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    duplicated_df = df_original.copy()
    df = pd.concat([df_original, duplicated_df], ignore_index=True).sort_values(by='page')

    print(df)
    time.sleep(3)
    create_video(df)


main()
