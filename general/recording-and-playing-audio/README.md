# [How to Play and Record Audio in Python](https://www.thepythoncode.com/article/play-and-record-audio-sound-in-python)
To run this:
- `pip3 install -r requirements.txt`
- To record audio:
    ```
    python audio_recorder.py --help
    ```
    **Output:**
    ```
    usage: audio_recorder.py [-h] [-o OUTPUT] [-d DURATION]

    an Audio Recorder using Python

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            Output file (with .wav)
    -d DURATION, --duration DURATION
                            Duration to record in seconds (can be float)
    ```
    For instance, you want to record 5 seconds and save it to `recorded.wav` file:
    ```
    python audio_recorder.py -d 5 -o recorded.wav
    ```
- To play audio, there are 3 options (`audio_player_playsound.py` using [playsound](https://pypi.org/project/playsound/), `audio_player_pydub.py` using [pydub](https://github.com/jiaaro/pydub), `audio_player_pyaudio.py` using [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/)), if you want to play `audio_file.mp3`::
    ```
    python audio_player_playsound.py audio_file.mp3
    ```
##
# [[] / []]()
Многие из приложений записывают ваш голос, а также воспроизводят звуки, если вы хотите сделать это, то вы попали в нужное место, в этом уроке мы будем использовать различные библиотеки Python для воспроизведения и записи аудио на Python.

Давайте установим необходимые библиотеки для этого учебника:

pip3 install playsound pyaudio pydub ffmpeg-python
Аудиоплеер
Во-первых, мы начнем с самого простого модуля здесь, playsound:

from playsound import playsound

playsound("audio_file.mp3")
Да, именно для этого модуля. Это в основном чистый Python, кроссплатформенный, однофункциональный модуль. В документации говорится, что расширения WAV и MP3, как известно, работают, и они могут работать и для других форматов.

Функция playsound() воспроизводит звук в аудиофайле и блокируется до завершения чтения файла, вы можете передать block=False, чтобы функция выполнялась асинхронно.

Другой альтернативой является использование библиотеки Pydub:

from pydub import AudioSegment
from pydub.playback import play

# read MP3 file
song = AudioSegment.from_mp3("audio_file.mp3")
# song = AudioSegment.from_wav("audio_file.wav")
# you can also read from other formats such as MP4
# song = AudioSegment.from_file("audio_file.mp4", "mp4")
play(song)
Примечание: Вам нужен FFmpeg, установленный на вашем компьютере, чтобы использовать функцию AudioSegment.from_file(), которая поддерживает все форматы, поддерживаемые FFmpeg.

Pydub является довольно популярной библиотекой, так как она предназначена не только для воспроизведения звука, вы можете использовать ее для различных целей, таких как преобразование аудиофайлов, нарезка звука, увеличение или уменьшение громкости и многое другое, проверьте их репозиторий для получения дополнительной информации.

Если вы хотите воспроизводить аудио с помощью PyAudio, проверьте эту ссылку.

Связанные с: Как извлечь аудио из видео в Python.

Аудио рекордер
Для записи голоса мы будем использовать библиотеку PyAudio, так как это наиболее удобный подход:

import pyaudio
import wave

# the file name output you want to record into
filename = "recorded.wav"
# set the chunk size of 1024 samples
chunk = 1024
# sample format
FORMAT = pyaudio.paInt16
# mono, change to 2 if you want stereo
channels = 1
# 44100 samples per second
sample_rate = 44100
record_seconds = 5
# initialize PyAudio object
p = pyaudio.PyAudio()
# open stream object as input & output
stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
frames = []
print("Recording...")
for i in range(int(sample_rate / chunk * record_seconds)):
    data = stream.read(chunk)
    # if you want to hear your voice while recording
    # stream.write(data)
    frames.append(data)
print("Finished recording.")
# stop and close stream
stream.stop_stream()
stream.close()
# terminate pyaudio object
p.terminate()
# save audio file
# open the file in 'write bytes' mode
wf = wave.open(filename, "wb")
# set the channels
wf.setnchannels(channels)
# set the sample format
wf.setsampwidth(p.get_sample_size(FORMAT))
# set the sample rate
wf.setframerate(sample_rate)
# write the frames as bytes
wf.writeframes(b"".join(frames))
# close the file
wf.close()
Приведенный выше код в основном инициализирует объект PyAudio, а затем мы открываем потоковый объект, который позволяет нам записывать с микрофона с помощью метода stream.read(). После того, как мы закончим запись, мы используем встроенный модуль wave для записи этого аудиофайла WAV на диск.

Когда вы установите input=True в методе p.open(), вы сможете использовать stream.read() для чтения с микрофона. Кроме того, когда вы установите значение output=True, вы сможете использовать stream.write() для записи в динамик.

Заключение
Хорошо, в этом уроке вы узнали, как вы можете воспроизводить аудиофайлы с помощью библиотек playsound, Pydub и PyAudio, а также записывать голос с помощью PyAudio.

Большая задача для вас - объединить это с экранным рекордером, и вы придумаете инструмент Python, который записывает ваш голос и экран одновременно. Вам нужно будет использовать поток, который записывает аудио и еще один для экранного рекордера, удачи в этом!

Узнайте больше с помощью курсов
Наконец, многие из концепций Python и обработки аудиосигналов не обсуждаются здесь подробно, если вы чувствуете, что хотите больше углубиться в Python и обработку сигналов, я настоятельно рекомендую вам пройти эти курсы:

Курс Python для всех
Курс по обработке аудиосигналов