import os

path = 'F:\\123\\222'


def rm_dir(path):
    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, path)):
        return False
    os.chdir(os.path.join(cwd, path))

    for file in os.listdir():
        print("file = " + file)
        os.remove(file)
    print(cwd)
    os.chdir(cwd)
    os.rmdir(os.path.join(cwd, path))

rm_dir(path)