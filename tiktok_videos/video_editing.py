import time

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os
import sys


HOME_DIR = os.path.expanduser("~")
VIDEOS_INCOMPLETOS_DIR = os.path.join(HOME_DIR, "Videos", "TikTok", "Incompletos")
VIDEOS_DIR = os.path.join(HOME_DIR, "Videos", "TikTok")
AUDIO_PATH = os.path.join(HOME_DIR, "Videos", "TikTok", "Audios")
AUDIO_ANSWER_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios\Zero\Correct Answer.mp3'
AUDIO_ENDING_PATH = r'C:\Users\Rafae\Videos\TikTok\Audios\Zero\Curte o video.mp3'


def main():

    # List all incompleted videos
    files = os.listdir(VIDEOS_INCOMPLETOS_DIR)

    # If there is no video, exit. Otherwise, keep going
    if not files:
        print(f"0 videos found in the path {VIDEOS_INCOMPLETOS_DIR}")
        sys.exit()
    else:
        print(f"{len(files)} video(s) found in the path {VIDEOS_INCOMPLETOS_DIR}")

    for file in files:
        print(file)

        file_path = os.path.join(VIDEOS_INCOMPLETOS_DIR, file)

        # Split file and extension
        file_name, file_ext = os.path.splitext(file)

        try:
            video = VideoFileClip(file_path)
        except Exception as err:
            print(f"Couldn't load the video: {err}")
            return '400'

        # Seconds when occurs the questions
        questions_at = [0.5, 10.5, 20.5, 30.5, 40.5, 50.5]
        asnwers_at = [7, 17, 27, 37, 47, 57]

        audio_clips_q = []
        audio_clips_a = []
        audio_clips_o = []

        # Load Questions Audios
        for i, sec in enumerate(questions_at, start=1):
            audio_name = f"{file_name}-q{i}.mp3"  # Nome do arquivo de áudio
            audio = AudioFileClip(os.path.join(AUDIO_PATH, audio_name)).set_start(sec).volumex(2.0)
            audio_clips_q.append(audio)

        # Load Answer Audios
        for sec in asnwers_at:
            audio = AudioFileClip(AUDIO_ANSWER_PATH).set_start(sec).volumex(0.5)
            audio_clips_a.append(audio)

        # Load Other Audios
        # audio_intro = AudioFileClip(AUDIO_INTRO_PATH).set_start(0)
        # audio_clips_o.append(audio_intro)
        # audio_theme = AudioFileClip(AUDIO_THEME_PATH).set_start(2)
        # audio_clips_o.append(audio_theme)
        # audio_level = AudioFileClip(AUDIO_LEVEL_PATH).set_start(4)
        # audio_clips_o.append(audio_level)
        audio_ending = AudioFileClip(AUDIO_ENDING_PATH).set_start(58)
        audio_clips_o.append(audio_ending)
        # audio_bg = AudioFileClip(AUDIO_BG_PATH).subclip(0, 67).volumex(0.5)
        # audio_clips_o.append(audio_bg)

        # Concatenate audios
        final_audio = CompositeAudioClip(audio_clips_q + audio_clips_a + audio_clips_o)

        # Insert final audio into the video
        final_video = video.set_audio(final_audio)

        final_video_path = os.path.join(VIDEOS_DIR, file)

        # Generate video
        final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac")

        # TODO: Se o video já estiver editado, exluir... ou
        # TODO: Editar apenas videos que não estejam em videos finalizados


main()
