import olefile
ole = olefile.OleFileIO('/home/dpaspa/MEGA/Business/Synertec/Spimaco/time/test.mpp')
print(ole.listdir())
ole.close()
