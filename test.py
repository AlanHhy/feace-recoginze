from aip import AipFace
import base64
import urllib
import cv2

""" 你的 APPID AK SK """
APP_ID = 'yourAPP_ID'
API_KEY = 'yourAPI_KEY'
SECRET_KEY = 'yourSECRET_KEY'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def fileopen(filepath):  # 打开图片
    with open(filepath, 'rb') as f:
        data = base64.b64encode(f.read())
    image = str(data, 'utf-8')
    return image


def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)
    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)
    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break
        c = cv2.waitKey(10)  # 按q退出
        cv2.imshow(window_name, frame)
        if c == ord('p'):
            cv2.imwrite('p3.jpg', frame)  # 保存图片
            print('图片保存成功')
            break
        if c == ord('o'):
            cv2.imwrite('p3.jpg', frame)  # 保存图片
            break
        if c == ord('q'):
            break
            # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()


def face_detect(filepath1, filepath2):  # 人脸对比
    image1 = fileopen(filepath1)
    image2 = fileopen(filepath2)
    result = client.match([
        {
            'image': image1,
            'image_type': 'BASE64',
        },
        {
            'image': image2,
            'image_type': 'BASE64',
        }])
    print(result)  # 打印出所有的信息


def face_add(filepath, groupid, userid):  # 人脸库增加 地址 组 用户
    image = fileopen(filepath)
    imageType = "BASE64"
    result = client.addUser(image, imageType, groupid, userid)
    if result['error_code'] == 0:
        print("增加人脸成功")
    else:
        print("增加人脸失败")


def face_search(filepath,groupIdList):  #人脸库搜索  groupIdList="你的用户组名称"
    image = fileopen(filepath)
    imageType="BASE64"
    data=client.search(image,imageType,groupIdList)
    result = data.get('result')
    print(result, end='\n')            #打印出所有信息
    if result == None:
        return None
    else:#分数大于70
        if result['user_list'][0]['score'] >70 :
            print(result['user_list'][0]['user_id'])
            return result['user_list'][0]['user_id']
        else :
            return None



if __name__ == '__main__':

    # face_detect('p1.jpg', 'p2.jpg')
    # face_add('p1.jpg', '1', '1')


    # result = face_search('timg.jpg', '1')
    # if result == "1":
    #     print("匹配成功")
    # else:
    #     print("匹配不成功")

    CatchUsbVideo('window_name', 0)
