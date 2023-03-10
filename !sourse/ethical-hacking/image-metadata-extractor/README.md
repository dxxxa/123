# [How to Extract Image Metadata in Python](https://www.thepythoncode.com/article/extracting-image-metadata-in-python)
To run this:
- `pip3 install -r requirements.txt`
- Extract metadata of the image `image.jpg`:
    ```
    python image_metadata_extractor.py image.jpg
    ```
##
# [[] / []]()
В этом уроке вы узнаете, как извлечь некоторые полезные метаданные из изображений с помощью библиотеки Pillow на Python.

Такие устройства, как цифровые камеры, смартфоны и сканеры, используют стандарт EXIF для сохранения изображений или аудиофайлов. Этот стандарт содержит много полезных тегов для извлечения, которые могут быть полезны для криминалистического исследования, таких как марка, модель устройства, точная дата и время создания изображения и даже информация GPS на некоторых устройствах.

Обратите внимание, что существуют бесплатные инструменты для извлечения метаданных, такие как ImageMagick или ExifTool в Linux, целью этого учебника является извлечение метаданных с помощью языка программирования Python.

Получите -35 OFF сейчас: этический взлом с помощью электронной книги Python

Для начала работы необходимо установить библиотеку Pillow:

pip3 install Pillow
Откройте новый файл Python и следуйте инструкциям:

from PIL import Image
from PIL.ExifTags import TAGS
Теперь это будет работать только с файлами изображений JPEG, возьмите любое изображение, которое вы взяли, и протестируйте его для этого урока (если вы хотите протестировать на моем изображении, вы найдете его в репозитории учебника):

# path to the image or video
imagename = "image.jpg"

# read the image data using PIL
image = Image.open(imagename)
Мы загрузили изображение с помощью метода Image.open(). Перед вызовом функции getexif() библиотека Pillow имеет некоторые атрибуты объекта image, давайте распечатаем их:

# extract other basic metadata
info_dict = {
    "Filename": image.filename,
    "Image Size": image.size,
    "Image Height": image.height,
    "Image Width": image.width,
    "Image Format": image.format,
    "Image Mode": image.mode,
    "Image is Animated": getattr(image, "is_animated", False),
    "Frames in Image": getattr(image, "n_frames", 1)
}

for label,value in info_dict.items():
    print(f"{label:25}: {value}")
Получить сейчас: Этический взлом с помощью электронной книги Python

Теперь вызовем метод getexif() для изображения, который возвращает метаданные изображения:

# extract EXIF data
exifdata = image.getexif()
Проблема с переменной exifdata теперь заключается в том, что имена полей являются просто идентификаторами, а не читаемыми человеком именами полей, поэтому нам понадобится словарь TAGS от PIL. Модуль ExifTags, который сопоставляет каждый идентификатор тега с удобочитаемым текстом:

# iterating over all EXIF data fields
for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    # decode bytes 
    if isinstance(data, bytes):
        data = data.decode()
    print(f"{tag:25}: {data}")
Вот мой вывод:

Filename                 : .\image.jpg
Image Size               : (5312, 2988)       
Image Height             : 2988
Image Width              : 5312
Image Format             : JPEG
Image Mode               : RGB
Image is Animated        : False
Frames in Image          : 1
ExifVersion              : 0220
ShutterSpeedValue        : 4.32
ApertureValue            : 1.85
DateTimeOriginal         : 2016:11:10 19:33:22
DateTimeDigitized        : 2016:11:10 19:33:22
BrightnessValue          : -1.57
ExposureBiasValue        : 0.0
MaxApertureValue         : 1.85
MeteringMode             : 3
Flash                    : 0
FocalLength              : 4.3
ColorSpace               : 1
ExifImageWidth           : 5312
FocalLengthIn35mmFilm    : 28
SceneCaptureType         : 0
ImageWidth               : 5312
ExifImageHeight          : 2988
ImageLength              : 2988
Make                     : samsung
Model                    : SM-G920F
Orientation              : 1
YCbCrPositioning         : 1
XResolution              : 72.0
YResolution              : 72.0
ImageUniqueID            : A16LLIC08SM A16LLIL02GM

ExposureProgram          : 2
ISOSpeedRatings          : 640
ResolutionUnit           : 2
ExposureMode             : 0
FlashPixVersion          : 0100
WhiteBalance             : 0
Software                 : G920FXXS4DPI4
DateTime                 : 2016:11:10 19:33:22
ExifOffset               : 226
MakerNote                : 0100 
                                Z@P
UserComment              :
ExposureTime             : 0.05
FNumber                  : 1.9
Куча полезных вещей; Быстро погуглив модель, я пришел к выводу, что это изображение было сделано Samsung Galaxy S6. Запустите это на изображениях, которые были захвачены другими устройствами, и вы увидите другие (возможно, больше) поля.