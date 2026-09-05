import os
import time
import zipfile



def list_zip_file(filename):
    with zipfile.ZipFile(filename) as myzip:
        for zipinfo in myzip.infolist():
            yield zipinfo.filename




if __name__ == "__main__":

    for path, dirname, filename in os.walk('./'):
        for dir in dirname:
            if os.path.isdir(dir):
                print(f"{dirname} is a directory")
        for file in filename:
            if os.path.isfile(file):
                print(f"{file} is a file")

    # check if file or directory exist
    print(os.path.exists('check_filename.py'))
    print(os.path.exists('../os_module'))

    if not os.path.exists('./my_directory'):
        try:
            os.makedirs('./my_directory')
        except OSError as error:
            print(error)

    file = "check_filename.py"
    st = os.stat(file)
    print("file stats: ", file)
    mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime = st
    print("- created:", time.ctime(ctime))
    print("- last accessed:", time.ctime(atime))
    print("- last modified:", time.ctime(mtime))
    print("- Size:", size, "bytes")
    print("- owner:", uid, gid)
    print("- mode:", oct(mode))


    extensions = ['.jpeg','.jpg','.txt','.py']

    for ext in extensions:
        print("File with extension => ", ext)
        for path, dirs, files in os.walk('../../.'):
            for file in files:
                if file.endswith(ext):
                    print(os.path.join(path, file))

    for filename in list_zip_file('txtZip.zip'):
        print(filename)