import os

myfolder = './'
newpath = os.path.join(myfolder, 'work')

try:
    os.mkdir(path=newpath)

    for idx in range(1, 11):
        newfile = os.path.join(newpath, 'somefolder' + str(idx).zfill(3))
        os.mkdir(path=newfile)
except FileExistsError:
    print('Directory exists already...')
finally:
    print('finished')