
import os
src='/home/shambhal/pycom/media/'
target='/home/shambhal/appoint.shambhalnetworks.in/media/'
os.symlink(src, target)
print("sym created")