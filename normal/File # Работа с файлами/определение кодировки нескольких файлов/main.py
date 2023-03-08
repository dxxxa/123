# Пример определения кодировки нескольких файлов.
# Для определения кодировки текстовых файлов, их необходимо открывать в режиме чтения байтов: more='rb'
# https://docs-python.ru/packages/modul-chardet-python-opredelenie-kodirovki/

import glob
from chardet.universaldetector import UniversalDetector

# создаем детектор
detector = UniversalDetector()
for filename in glob.glob('*.xml'):
    print(filename.ljust(60), end='')
    # сбрасываем детектор 
    # в исходное состояние
    detector.reset()
    # проходимся по строкам очередного
    # файла в режиме 'rb'
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    print(detector.result)