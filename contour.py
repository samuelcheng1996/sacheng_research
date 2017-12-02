#Samuel Cheng

#Program that draws contours of an image of floorplans and prints pixel coordinates

import cv2
import numpy as np

img = cv2.imread('baskin.jpg')
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# gray = np.float32(gray)

#image filtering to remove noise
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)

#binary image for better edge detection
retval, img = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

#perform erosion and dilation
kernel = np.ones((5,5), np.uint8)
img_erosion = cv2.erode(img, kernel, iterations=2)
img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
img_erosion = cv2.erode(img_dilation, kernel, iterations=1)
img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)
img = cv2.erode(img_dilation, kernel, iterations=3)
# cv2.imwrite('erosion.jpg',img)

#canny edge detector
img = cv2.Canny(img,10,52)
# img = cv2.dilate(img, kernel, iterations=3)
#cv2.imwrite('contour.jpg',img)
#img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

#contour drawing
img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# print(contours)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
cv2.drawContours(img, contours, -1, (0,255,0), 3)
img = cv2.resize(img, (0,0), fx=0.1, fy=0.1)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()



#draw circle on double left click. Print coordinate if a is pressed
def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),25,(255,0,0),-1)
        mouseX,mouseY = x,y
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image',draw_circle)
while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print (mouseX,mouseY)
