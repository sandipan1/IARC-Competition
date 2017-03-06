import cv2
from math import *
import numpy as np 
im=cv2.imread("/home/sandipan/computer_vision/bellatrix/1.jpg")

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray,(5,5),0)
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_TRUNC)
#thresh= cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
kernel=np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

gr=closing.astype(float)

height,width,channel=im.shape
y=height-75
x1= 15
x2= width -100
print y,x1,x2
line=[gr[y][i] for i in range (x1,x2)]
der= [line[i+1]-line[i] for i in range (len(line)-1)]
der = [abs(x) for x in der]
der_thres=[der[i]>40 for i in range(len(der))]
edge_pts=[]
for i in range(len(der_thres)):
	if der_thres[i]==True:
		edge_pts.append(i)
print edge_pts

for i in edge_pts:
	cv2.circle(closing,(i,y), 5, (0,255,0), -1)
cv2.imshow('frame',closing)
cv2.imshow("Thresholded",thresh)
cv2.imshow('closing',closing)
cv2.waitKey(0)