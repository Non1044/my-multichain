import shutil
import errno

src = 'C:/Users/Bee/AppData/Roaming/MultiChain'
dest = 'C:/Users/Bee/Desktop/Backup'

try:
    shutil.copytree(src, dest)
except OSError as err:
    if err.errno == errno.ENOTDIR:
        shutil.copy(src, dest)
    else:
        print("Error: % s" % err)
