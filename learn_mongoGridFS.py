from gridfs import *
from pymongo import MongoClient

pic_src = 'c:\\Users\\yqin78\\Proj.Python\\PyBMS_BrIM\\_data\\MARCpic\\Photos_1.jpg'
pic_sv = 'c:\\Users\\yqin78\\Proj.Python\\PyBMS_BrIM\\_data\\MARCpic\\new_Photos_1.jpg'


def insertFile(pic_path, file_name):
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    with open(pic_path, 'rb') as image:
        data = image.read()
        id = fs.put(data, filename=file_name)
        print(id)


def getFile(file_name, save_path):
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    file = fs.get_version(file_name, 0)
    data = file.read()
    out = open(save_path, 'wb')
    out.write(data)
    out.close()


def delFile(Obj_Id):
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    fs.delete(Obj_Id)


def listName():
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    print(fs.list())


insertFile(pic_src, 'test_pic')
getFile('test_pic', pic_sv)
listName()
