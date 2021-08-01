from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image
import time

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

filelist = []


def GetlistOfAllFiles(parent):
    all_data = drive.ListFile(
        {'q': "'%s' in parents and trashed=false" % parent}).GetList()
    folder_list = [folder for folder in all_data if folder['mimeType']
                   == 'application/vnd.google-apps.folder']
    for file in all_data:
        if 'image/' in file['mimeType']:
            filelist.append(file)

    for f in folder_list:
        ftype = f.get('mimeType', None)
        if ftype and ftype == 'application/vnd.google-apps.folder':  # if folder
            folder_list.append(
                {"id": f['id'], "title": f['title'], "list": GetlistOfAllFiles(f['id'])})
    return folder_list


def loadAndDisplayFiles():
    for file in filelist:
        print("Viewing FIle:", file['title'], file['mimeType'], file['id'])

        imgData = drive.CreateFile({'id': file['id']})
        imgData.GetContentFile('temp')
        img = Image.open('temp')
        img.show()
        time.sleep(3)


GetlistOfAllFiles('root')
loadAndDisplayFiles()
