from genericpath import isdir
from django.test import TestCase
import os
from pathlib import Path
from pycom.settings import MEDIA_ROOT
from pycom.settings import MEDIA_URL

  
  
class FileTest(TestCase):
    valid=['jpeg','jpg','JPG','PNG','GIF','gif','png','JPEG']
    #print(MEDIA_ROOT2)
    print(MEDIA_ROOT)
    
    l=os.listdir(MEDIA_ROOT)
    files=[]
    folders=[]
    #print(l)
    for node in l :
         if(os.path.isdir(MEDIA_ROOT+node)):
             folders.append(MEDIA_ROOT+node)
         else:
             narr=os.path.splitext(node)
             ext=narr[1]
             if(ext in valid):
               files.append(MEDIA_ROOT+node)  
    print(folders)    
    print(files)    
    path1="C:\\Users\\shambhal\\pycom\\media/cache/"
    path2="c:/wamp/www/ht.py"
    bname=os.path.basename(path2)
    print("bname")
    print(bname)
    
    path2="cate/lupchup.jpg"
    filename=os.path.basename(path2)
    mpath=path2.replace(filename,'')
    Path(path1+mpath).mkdir(parents=True, exist_ok=True)
# Create your tests here.
