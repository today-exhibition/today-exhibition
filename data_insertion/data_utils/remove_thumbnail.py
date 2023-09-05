import os

def remove_thumbnail(dirPath):
    dirPath = dirPath

    if os.path.exists(dirPath):
        for file in os.scandir(dirPath):
            os.remove(file)
        return print("thumbnail_imgs 폴더 내용 지우기 완료!")
    
    return print("thumbnail_imgs 폴더경로 없음")