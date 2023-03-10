# [How to Extract Audio from Video in Python](https://www.thepythoncode.com/article/extract-audio-from-video-in-python)
##
# [[] / []]()
Если вы хотите конвертировать свое видео в аудиоформат с помощью Python, то вы находитесь в правильном месте. В этом уроке я покажу вам два простых метода извлечения аудио из видеофайла с помощью библиотеки FFmpeg и MoviePy на Python.

Прежде чем мы начнем, вам необходимо установить FFmpeg на вашем компьютере. Если вы используете Windows, проверьте этот учебник, где вы просто устанавливаете его и добавляете в переменную PATH. Если вы используете Linux, то его легко установить с помощью следующих команд:

$ sudo apt update
$ sudo apt install ffmpeg
Обратите внимание, что MoviePy зависит от программного обеспечения FFmpeg для чтения и записи видео, и он автоматически установит его при первом использовании. Поэтому вам не следует сильно беспокоиться, если вы провалите вышеуказанный шаг и захотите использовать второй метод (т. Е. Используя MoviePy).

Давайте установим MoviePy сейчас:

$ pip install moviepy
Связанные с: Как добавить аудио в видео в Python.

Метод 1: Использование FFmpeg напрямую
Этот метод включает в себя использование встроенного модуля подпроцесса Python для соответствующей команды FFmpeg:

import subprocess
import os
import sys

def convert_video_to_audio_ffmpeg(video_file, output_ext="mp3"):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

if __name__ == "__main__":
    vf = sys.argv[1]
    convert_video_to_audio_ffmpeg(vf)
В функции convert_video_to_audio_ffmpeg() мы сначала разделяем имя входного видеофайла на исходное имя файла без расширения и само расширение, чтобы мы могли получить имя выходного файла, просто добавив расширение аудио к исходному имени. В данном случае это mp3.

Мы используем метод subprocess.call() для выполнения команды FFmpeg, флаг -y предназначен для игнорирования приглашения перезаписи, а -i для указания входного видеофайла. Последним аргументом является имя выходного файла с расширением mp3 audio, вы можете изменить его на wav, если хотите, но это привело к большому аудиофайлу в моем случае по какой-то причине.

Наконец, мы передаем подпроцесс. DEVNULL в аргумент stdout и подпроцесс. STDOUT to stderr, чтобы мы могли отбросить выходные данные FFmpeg. Вы можете запустить скрипт через:

$ python video2audio_ffmpeg.py zoo.webm
Где zoo.webm находится ваш видеофайл любого формата.

Связанные с: Как перевернуть видео в Python

Метод 2: Использование MoviePy
В этом методе мы используем довольно простую библиотеку MoviePy, которая использует FFmpeg под капотом:

import os
import sys
from moviepy.editor import VideoFileClip


def convert_video_to_audio_moviepy(video_file, output_ext="mp3"):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(f"{filename}.{output_ext}")


if __name__ == "__main__":
    vf = sys.argv[1]
    convert_video_to_audio_moviepy(vf)
Здесь мы создаем экземпляр класса VideoFileClip(), а затем используем метод write_audiofile() из объекта audio клипа, чтобы сохранить его в виде аудиофайла. С помощью скрипта:

$ python video2audio_moviepy.py zoo.webm
Заключение
Хорошо, вот и все для этого быстрого учебника, я надеюсь, что он помог вам выполнить ваши проекты быстро и надежно.