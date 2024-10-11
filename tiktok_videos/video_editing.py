from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os

# Video
VIDEO_NAME = '0001-tecnologia-facil'
VIDEO_PATH = os.path.join(r'C:\Users\Rafae\Videos\TikTok\Incompletos', VIDEO_NAME + '.mp4')
FINAL_VIDEO_PATH = os.path.join(r'C:\Users\Rafae\Videos\TikTok', VIDEO_NAME + '.mp4')

# Audio
AUDIO_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios'
AUDIO_INTRO_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios\Zero\Teste o seu conhecimento.mp3'
AUDIO_THEME_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios\Zero\Tecnologia.mp3'
AUDIO_LEVEL_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios\Zero\Nível Médio.mp3'
AUDIO_ANSWER_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios\Zero\Correct Answer.mp3'
AUDIO_ENDING_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios\Zero\Curte o video.mp3'


def main():

    try:
        video = VideoFileClip(VIDEO_PATH)
    except Exception as err:
        print(f"Couldn't load the video: {err}")
        return '400'

    # Seconds when occurs the questions
    questions_at = [5, 14, 28, 41, 55]
    asnwers_at = [10, 23.5, 37, 50.5, 64]

    audio_clips_q = []
    audio_clips_a = []
    audio_clips_o = []

    # Load Questions Audios
    for i, sec in enumerate(questions_at, start=1):
        audio_name = f"{VIDEO_NAME}-q{i}.mp3"  # Nome do arquivo de áudio
        audio = AudioFileClip(os.path.join(AUDIO_PATH, audio_name)).set_start(sec)
        audio_clips_q.append(audio)

    # Load Answer Audios
    for sec in asnwers_at:
        audio = AudioFileClip(AUDIO_ANSWER_PATH).set_start(sec)
        audio_clips_a.append(audio)

    # Load Other Audios
    audio_intro = AudioFileClip(AUDIO_INTRO_PATH).set_start(0)
    audio_clips_o.append(audio_intro)
    audio_theme = AudioFileClip(AUDIO_THEME_PATH).set_start(2)
    audio_clips_o.append(audio_theme)
    audio_level = AudioFileClip(AUDIO_LEVEL_PATH).set_start(3)
    audio_clips_o.append(audio_level)
    audio_ending = AudioFileClip(AUDIO_ENDING_PATH).set_start(65)
    audio_clips_o.append(audio_ending)

    final_audio = CompositeAudioClip(audio_clips_q + audio_clips_a + audio_clips_o)

    final_video = video.set_audio(final_audio)

    final_video.write_videofile(FINAL_VIDEO_PATH, codec="libx264", audio_codec="aac")


main()
