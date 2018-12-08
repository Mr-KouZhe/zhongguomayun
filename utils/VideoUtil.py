import cv2,os

fps = 24   #视频帧率
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
videoWriter = cv2.VideoWriter('flower2.avi', fourcc, fps, (200,480))   #(1360,480)为视频大小
root='E:/upload/v/2/'
imgs=os.listdir(root)
for image_name in imgs:
    print(root+image_name)
    videoWriter.write(cv2.imread(root+image_name))
#for i in range(1,300):
   # p1=0
   # p2=i
   # img12 = cv2.imread('D:/testResults/img_'+str(p1)+'_'+str(p2)+'.jpg')
#    cv2.imshow('img', img12)
#    cv2.waitKey(1000/int(fps))
    #videoWriter.write(img12)
videoWriter.release()