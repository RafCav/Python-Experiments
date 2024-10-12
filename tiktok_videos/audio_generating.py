from dotenv import load_dotenv
import os
from elevenlabs import save
from elevenlabs.client import ElevenLabs
import pandas as pd

VIDEO_NAME = '0001-curiosidades-facil'
VIDEO_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios'

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

user = client.user.get()


def generate_audio(txt_to_speech, q):

    audio = client.generate(
      text=txt_to_speech,
      voice="Will",
      model="eleven_multilingual_v2"
    )

    save(audio=audio, filename=os.path.join(VIDEO_PATH, VIDEO_NAME + f'-q{q}.mp3'))


def main():
    print("Credit Quota Total:", user.subscription.character_limit)

    sheet_id = '1ougkayhtVRRCc88jWGRMFdTBBM7AafbSEZsdqCRVwJE'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

    for i in range(len(df)):
        question = df['question'].iloc[i]
        print(f"Pergunta {i+1} de {len(df)}: {question}", end='')
        generate_audio(question, i+1)
        print(f" | Áudio gerado com sucesso!")

    restantes = user.subscription.character_limit - user.subscription.character_count
    print("Credit Quota Remaining:", restantes)


main()
