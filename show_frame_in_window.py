#实时显示摄像头内容并单击任意键停止调用

import cv2

clicked=False
def onMouse(event,x,y,flags,param):
    global clicked
    if event ==cv2.EVENT_LBUTTONUP:
        clicked=True

cameraCapture=cv2.VideoCapture(0)
cv2.namedWindow('MyWindow')
cv2.setMouseCallback('MyWindow',onMouse)

print( 'showing camer feed.click window or press any key to stop.')
success,frame=cameraCapture.read()
print
while success and cv2.waitKey(1)==-1 and not clicked:
    cv2.imshow('MyWindow',frame)
    success,frame=cameraCapture.read()

cv2.destroyWindow('MyWindow')
cameraCapture.release()
