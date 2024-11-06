import sys
import os
import shutil
import pandas as pd
import pyautogui
import time
import pyperclip

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

screen_width, screen_height = pyautogui.size()  # Screen Size
screen_size = f'{screen_width}x{screen_height}'

# LOCATIONS (18% zoom)
PAGE1 = (255, 750) if screen_size == '1600x900' else (325, 900)
QUESTION = (830, 415) if screen_size == '1600x900' else (1000, 490)
ANS1 = (790, 515) if screen_size == '1600x900' else (950, 628)
ANS1_BLOCK = (790, 525) if screen_size == '1600x900' else (950, 638)
ANS2 = (790, 548) if screen_size == '1600x900' else (950, 665)
ANS2_BLOCK = (790, 558) if screen_size == '1600x900' else (950, 675)
ANS3 = (790, 580) if screen_size == '1600x900' else (950, 707)
ANS3_BLOCK = (790, 590) if screen_size == '1600x900' else (950, 717)
ANIMATE_BTM = (1140, 205) if screen_size == '1600x900' else (1380, 255)
BLANK_SPACE = (1200, 500) if screen_size == '1600x900' else (1600, 560)
BLOCKS = {ANS1: ANS1_BLOCK, ANS2: ANS2_BLOCK, ANS3: ANS3_BLOCK}

A_MENU_SCROLL_BAR = (425, 830) if screen_size == '1600x900' else (530, 990)
A_PULSE_BTM = (350, 630) if screen_size == '1600x900' else (430, 740)
A_REMOVE_BTM = (350, 820) if screen_size == '1600x900' else (430, 970)
ANS_BLOCK_COLOR = (600, 210) if screen_size == '1600x900' else (770, 255)
ANS_BLOCK_COLOR_YELLOW = (160, 420) if screen_size == '1600x900' else (200, 520)
ANS_BLOCK_COLOR_ORANGE = (110, 420) if screen_size == '1600x900' else (130, 520)

SHARE_BTM = (1520, 150) if screen_size == '1600x900' else (1520, 150)
DOWNLOAD_BTM = (1240, 560) if screen_size == '1600x900' else (1520, 150)
DOWNLOAD_BTM_2 = (1240, 625) if screen_size == '1600x900' else (1520, 150)

# EXECUTIONS QUEUE
TESTING_ORDER = [PAGE1, QUESTION, ANS1, ANS1_BLOCK, ANS2, ANS2_BLOCK, ANS3, ANS3_BLOCK]
TEXT_ALTERATION_ORDER = [QUESTION, ANS1, ANS2, ANS3]


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

    sys.exit()


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


def generate_dataframe():
    sheet_id = '1ougkayhtVRRCc88jWGRMFdTBBM7AafbSEZsdqCRVwJE'
    gid = '988783826'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    df_original = pd.read_csv(url)  # Generate df a partir do sheets

    df_video_name = df_original[df_original['video_name'].notna()]

    last_vid = df_video_name['video_name'].str[-8:].astype(int).max()  # Last 8 num of prev vid
    video_name = f"1mq_tsc-{str(last_vid + 1).zfill(8)}"  # Create the current video's name
    print(f'Last Video: {last_vid}\nCurrent Video Name: {video_name}')

    if len(df_original) < 6:
        print('Google Sheets must have at least 6 questions')
        sys.exit()

    df_original = df_original[~df_original['video_name'].notna()].head(6)  # Filtering 6 questions not made before

    duplicated_df = df_original.copy()

    duplicated_df['page'] = range(1, len(duplicated_df) + 1)
    df = pd.concat([duplicated_df, duplicated_df], ignore_index=True).sort_values(by='page')

    return df, video_name


def download(video_name):
    # Share Button
    pyautogui.moveTo(SHARE_BTM, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    # Download Button
    pyautogui.moveTo(DOWNLOAD_BTM, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    # Download... Again...
    pyautogui.moveTo(DOWNLOAD_BTM_2, duration=0.5)
    pyautogui.click()
    time.sleep(20)

    switch_page()

    # Above I'm going to rename the video and put in the correct folder
    home_dir = os.path.expanduser("~")
    downloads_dir = os.path.join(home_dir, "Downloads")

    current_name = "Quiz - Tiktok.mp4"  # That's the name when I download from Canva
    current_path = os.path.join(downloads_dir, current_name)

    # I search the path of current video
    retry = 0
    if not os.path.exists(current_path):  # Sometimes, the video is not downloaded yet. So we wait
        if retry == 5:
            print(f"{current_path} not found")
            sys.exit()
        time.sleep(20)
        retry += 1

    new_name = f"{video_name}.mp4"  # Defina o novo nome desejado
    new_path = os.path.join(home_dir, "Videos", "TikTok", "Incompletos")

    # Verify if the new path exists
    if not os.path.exists(new_path):
        print(f"{new_path} not found")
        sys.exit()

    # Cut and Paste in the new path
    new_path = os.path.join(new_path, new_name)

    try:
        shutil.move(current_path, new_path)  # Rename and move the video
        print(f"File renamed and moved successfully to {new_path}")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An Error Occurred: {e}")


def main():
    print(f"Largura: {screen_width}, Altura: {screen_height} | ({screen_size})")

    df, video_name = generate_dataframe()

    time.sleep(5)

    switch_page()

    # location_testing()  # Don't worry, this function will interrupt the code :)

    time.sleep(5)

    for i in range(len(df)):
        if i == 0:  # Only first loop
            pyautogui.click(PAGE1)
        else:
            pyautogui.scroll(-100)

        payload = {
            'QUESTIONS': df['question'].iloc[i],
            'ANS1': 'A) ' + str(df['op1'].iloc[i]),
            'ANS2': 'B) ' + str(df['op2'].iloc[i]),
            'ANS3': 'C) ' + str(df['op3'].iloc[i]),
            'ANS': df['answer'].iloc[i]
        }

        time.sleep(2)
        edit_page(payload, i)

        pyautogui.click(BLANK_SPACE)
        time.sleep(2)

    download(video_name)

    # TODO: Set video_name column with the name of the video


main()
