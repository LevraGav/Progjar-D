import os
import json
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,param=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            # print(e)
            return dict(status='ERROR',data=str(e))

    def get(self,filename=''):
        if(filename==''):
            return None
        try:
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def upload(self, param):
        try:
            filename = param[0] 
            data = param[1]
            simpan = open(filename, 'xb')
            simpan.write(base64.b64decode(data))
            simpan.close()
        except IndexError:
            return dict(status='ERROR',data='some parameters are missing')
        except FileExistsError:
            return dict(status='ERROR', data = 'file name exsist')
        return dict(status="OK", data='data uploaded successfully');

    def delete(self,param):
        try:
            filename = param[0]
            os.remove(filename)
        except IndexError:
            return dict(status='ERROR',data='some parameters are missing')
        except FileNotFoundError:
            return dict(status='ERROR',data='file not found')
        return dict(status='OK',data="file deleted successfully")

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get('pokijan.jpg'))