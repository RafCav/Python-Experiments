import time

from dotenv import load_dotenv
import os
from elevenlabs import save
from elevenlabs.client import ElevenLabs
import pandas as pd
import sys

HOME_DIR = os.path.expanduser("~")
VIDEOS_INCOMPLETOS_DIR = os.path.join(HOME_DIR, "Videos", "TikTok", "Incompletos")
VIDEOS_DIR = os.path.join(HOME_DIR, "Videos", "TikTok")
AUDIO_PATH = os.path.join(HOME_DIR, "Videos", "TikTok", "Audios")

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

user = client.user.get()


def generate_audio(txt_to_speech, q, video_name):

    # Here we get the audio's name
    audio_name = video_name + f'-q{q}.mp3'

    # Verify if the audios already exist. If so, return
    audios = os.listdir(AUDIO_PATH)
    if audio_name in audios:
        print(f" | {audio_name} already exists into {AUDIO_PATH}")
        return

    audio = client.generate(
      text=txt_to_speech,
      voice="Will",
      model="eleven_multilingual_v2"
    )

    save(audio=audio, filename=os.path.join(AUDIO_PATH, audio_name))

    print(f" | Audio generated successfully!")


def main():
    # List all the videos not completed
    files = os.listdir(VIDEOS_INCOMPLETOS_DIR)

    # If there is no video, exit. Otherwise, keep going
    if not files:
        print(f"0 videos found in the path {VIDEOS_INCOMPLETOS_DIR}")
        sys.exit()
    else:
        print(f"{len(files)} video(s) found in the path {VIDEOS_INCOMPLETOS_DIR}")

    # Generate df
    sheet_id = '1ougkayhtVRRCc88jWGRMFdTBBM7AafbSEZsdqCRVwJE'
    gid = '988783826'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)

    # Read each file inside directory
    for file in files:
        print(f'\n### {file}')

        # Split file and extension
        file_name, file_ext = os.path.splitext(file)

        # Create a copy of df. Filtering just the questions of the video
        df_filtered = df.copy()
        df_filtered = df_filtered[df_filtered['video_name'] == file_name]

        # Verify the quota
        df_temp = df_filtered.copy()  # Had to generate another df
        quota_nedded = df_temp['question_len'].astype(int).sum()
        quota_total = user.subscription.character_limit
        print(f"Credit Quota Need: {quota_nedded} | You Have: {quota_total}", end='')
        if quota_total >= quota_nedded:
            print(" | You have enough :)")
        else:
            print(" | You don't have enough :(")
            sys.exit()

        # Generate the audios
        for i in range(len(df_filtered)):
            question = df_filtered['question'].iloc[i]
            print(f"Question {i + 1} of {len(df_filtered)}: {question}", end='')
            generate_audio(question, i + 1, file_name)


        # restantes = user.subscription.character_limit - user.subscription.character_count
        # print("Credit Quota Remaining:", restantes)




main()
