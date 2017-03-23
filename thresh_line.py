import cv2
import numpy as np

im=cv2.imread('/home/sandipan/computer_vision/bellatrix/map.jpg')
height, width ,channel= im.shape[:]
M = cv2.getRotationMatrix2D((width/2,height/2),-90,1)
im = cv2.warpAffine(im,M,(width,height))

#im=cv2.resize(im,(width/3,height/3))
height, width ,channel= im.shape[:]
print height,width,channel
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

#thresh1= cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
#ret,thresh1 = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
	
kernel=np.ones((7,7),np.uint8)

#blur = cv2.GaussianBlur(thresh1,(5,5),0)
#closing = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
erosion = cv2.erode(th2,kernel,iterations = 1)

#Harris corner detection


dst = cv2.cornerHarris(erosion,5,3,0.04)
im[dst>0.1*dst.max()]=[0,0,255]
# for i in range(len(dst)):
# 	for j in range(len(dst[i])):
# 		if dst[i][j]>0.2*dst.max():
# 			print (i,j,dst[i][j])

countours, hierarchy = cv2.findContours(th2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnts = sorted(countours,key=cv2.contourArea,reverse=True)
# epsilon = 0.1*cv2.arcLength(cnts[0],True)
# approx = cv2.approxPolyDP(cnts[0],epsilon,True)
# hull=cv2.convexHull(cnts[0])

# for i in cnts[0]:

# 	cv2.circle(gray, (i[0][0],i[0][1]), 5,(0,0,255),2)
new  = np.zeros( (height,width,channel-2), dtype=np.uint8)
cv2.drawContours(gray, [cnts[0]],0 , (0, 255, 0), 2)
cv2.drawContours(new,[cnts[0]],0,(255,0,0),2)
cv2.imshow("contour",new)
#for i in cnts[0]:
	#if i[0][0]<=height and i[0][1]<=width:
		#new[i[0][0]][i[0][1]]=255
	#else : pass
#cv2.imshow('new',new)

minLineLength = 100
maxLineGap =25
edges = cv2.Canny(np.array(erosion),50,150,apertureSize = 3)
if edges ==None :
		print "no edge"
	
else:
	#lines = cv2.HoughLines(edges,1,np.pi/180,5)
	lines = cv2.HoughLinesP(new,10,np.pi/180,75,minLineLength,maxLineGap)
	if lines !=None:
		for x1,y1,x2,y2 in lines[0]:
			m= (y2-y1)/(x2-x1)
			
			if m==10:
				cv2.line(im,(x1,y1),(10*x2,y2),(0,0,255),2)
			else:
				cv2.line(im,(x1,y1),(x2,y2),(0,255,0),2)
		# for rho,theta in lines[0]:
		# 	a = np.cos(theta)
		# 	b = np.sin(theta)
		# 	x0 = a*rho
		# 	y0 = b*rho
		# 	x1 = int(x0 + 1000*(-b))
		# 	y1 = int(y0 + 1000*(a))
		# 	x2 = int(x0 - 1000*(-b))
		# 	y2 = int(y0 - 1000*(a))
			
		# 	cv2.line(im,(x1,y1),(x2,y2),(0,255,0),2)
	else :
		print "no edge"




cv2.imshow("gray",gray)
cv2.imshow("th",th2)
cv2.imshow("ero",erosion)
cv2.imshow("im",im)


k=cv2.waitKey(0)
if k==ord('q'):

	cv2.destroyAllWindows()
