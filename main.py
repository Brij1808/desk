
import numpy as np
from object_detector import *


size_22 = []
size_18 = []
size_20 = []
ade=[]
a_22 = [i for i in range(225, 245)]
b_22 = [j for j in range(520, 555)]
a_18 = [i for i in range(425, 460)]
b_18 = [i for i in range(220, 235)]
a_20 = [i for i in range(480, 515)]
b_20 = [i for i in range(216, 235)]


parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


detector=HomogeneousBgDetector()

cy1=230
offset=6
counter=0

upper_left = (40, 20)
bottom_right = (500, 650)

#camera = cv2.VideoCapture('rtsp://admin:brijesh123@192.168.1.101:554/Streaming/Channels/101')
camera = cv2.VideoCapture('http://192.168.168.244:8080/video')
#camera = cv2.VideoCapture(0)

while True:
    check, frame = camera.read()
    frame = cv2.resize(frame, (1000, 700))
    r = cv2.rectangle(frame, upper_left, bottom_right, (100, 50, 200), 5)
    rect_img = frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
    cv2.line(frame,(cy1,50),(cy1,599),(0,0,0),5)
    #frame1 = cv2.cvtColor(rect_img, cv2.COLOR_RGB2BGR)


    corners, _, _ = cv2.aruco.detectMarkers(rect_img, aruco_dict, parameters=parameters)

    int_corners = np.int0(corners)
    cv2.polylines(rect_img, int_corners, True, (0, 255, 0), 5)


    contours=detector.detect_objects(rect_img)


    for cnt in contours:

        rect=cv2.minAreaRect(cnt)

        (x,y),(w,h),angle=rect

        box=cv2.boxPoints(rect)

        box=np.int0(box)

        cv2.circle(rect_img,(int(x),int(y)),5,(0,0,255),-1)

        cv2.polylines(rect_img,[box],True,(255,0,0),1)
        #cv2.putText(rect_img, "W{}".format(round(w, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN,2, (100, 200, 0), 2)
        #cv2.putText(rect_img, "H{}".format(round(h, 1)), (int(x - 100), int(y + 15)),cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        if int(y)<(cy1+offset) and int(y)>(cy1-offset):
            cv2.imwrite(filename='saved_img.jpg',img=rect_img)
            parameters = cv2.aruco.DetectorParameters_create()
            aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

            detector = HomogeneousBgDetector()

            img = cv2.imread("saved_img.jpg")

            corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

            int_corners = np.int0(corners)
            cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

            contours = detector.detect_objects(img)

            lst_w = []
            lst_h = []
            for cnt in contours:
                rect = cv2.minAreaRect(cnt)

                (x, y), (w, h), angle = rect
                # print(type(w))
                lst_h.append(h)
                lst_w.append(w)

                # width=list(np.array(w))
                # width=max(width)

                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # print(box)

                cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.polylines(img, [box], True, (255, 0, 0), 2)
                cv2.putText(img, "Width {}".format(round(w, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2,
                            (100, 200, 0), 2)
                cv2.putText(img, "Height {}".format(round(h, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN,
                            2,
                            (100, 200, 0), 2)

            image = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

            #cv2.imshow("image", image)
            my_h = max(list(map(int, lst_h)))
            my_w = max(list(map(int, lst_w)))
            if ((round(my_w) in a_22) or (round(my_w) in b_22)) and ((round(my_h) in a_22) or (round(my_h) in b_22)):
                size_22.append("16")
            elif ((round(my_w) in a_18) or (round(my_w) in b_18)) and ((round(my_h) in a_18) or (round(my_h) in b_18)):
                size_18.append("18")
            elif ((round(my_w) in a_20) or (round(my_w) in b_20)) and ((round(my_h) in a_20) or (round(my_h) in b_20)):
                size_20.append("20")
            else:
                print("not match")
            axc = (f"size_16 {len(size_22)} -- size_18 {len(size_18)}")
            ade.append(axc)


            continue

            counter+=1
            print(counter)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.waitKey(1650)
        cv2.destroyAllWindows()
