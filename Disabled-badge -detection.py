import cv2
import numpy as np


import serial,time
#arduino = serial.Serial('COM6', 9600)
arduino=serial.Serial('/dev/ttyACM0',9600)
time.sleep(1)

opened=False
cap=cv2.VideoCapture(1)

while True:
	triangle=False
	circle=False
	ret, img = cap.read()
	# Convert to grayscale. 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
	# Blur using 3 * 3 kernel. 
	gray_blurred = cv2.blur(gray, (3, 3)) 
	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# Green color
	low_green = np.array([25, 52, 72])
	high_green = np.array([102, 255, 255])
	green_mask = cv2.inRange(hsv_frame, low_green, high_green)
	green = cv2.bitwise_and(img, img, mask=green_mask)
	# Apply Hough transform on the blurred image. 
	detected_circles = cv2.HoughCircles(gray_blurred,  cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,param2 = 30, minRadius = 1, maxRadius = 40)
	
	_, contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		area = cv2.contourArea(cnt)
		approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
		x = approx.ravel()[0]
		y = approx.ravel()[1]

		if area >5  and len(approx) == 3:
			
			#print "Area:",area
			cv2.drawContours(img, cnt, 0, (255, 0, 255), 1)  # (-1) draw all countours
			#cv2.drawContours(img, [approx], 0, (255, 255, 0), 1)
			cv2.drawContours(img, [approx], 0, (220, 0, 0), 2)

			#cv2.putText(pic, "Triangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255))
			#print('triangle')
			x,y,w,h=cv2.boundingRect(cnt)
			triangle=True
			# Draw circles that are detected. 
			if detected_circles is not None: 
				
				# Convert the circle parameters a, b and r to integers. 
				detected_circles = np.uint16(np.around(detected_circles)) 
  
				for pt in detected_circles[0, :]: 
					a, b, r = pt[0], pt[1], pt[2]
					#print (x,y,a,b)
					if x<a-r and x+w>a+r and y<b-r and y+h>b+r:
						# cv2.rectangle(img, (a-r,b), (a+r, b), (255, 255, 0), 1)
						# cv2.rectangle(img, (a,b-r), (a, b+r), (255, 255, 0), 1)
						cv2.rectangle(img, (a-r,b), (a+r, b), (220, 0, 0), 2)
						cv2.rectangle(img, (a,b-r), (a, b+r), (220, 0, 0), 2)
						# Draw the circumference of the circle. 
						cv2.circle(img, (a, b), r, (220, 0, 0), 2) 
						#print (b-r,(y+h)/2)
						# Draw a small circle (of radius 1) to show the center. 
						cv2.circle(img, (a, b), 1, (0, 0, 255), 2)
						circle=True
		#print "triangle",triangle
		#print "circle",triangle


	if not opened:
		if circle and triangle:
			arduino.write(b'o')
			
		
			
	data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
	
	if data:
		if data=="Gate open":opened=True
		if data=="Gate close":opened=False
	cv2.imshow("Frame", img)
	cv2.imshow("Green", green)
	
	key = cv2.waitKey(1)
	if key == 27:
		break




