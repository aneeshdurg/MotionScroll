import cv2
import pyautogui
import sys

if "-a" in sys.argv:
	sys.argv=["-v", "-p"]
	
cap = cv2.VideoCapture(0)
size = int(cap.get(4)/2)
Current = None
Previous = None
while True:
	_, frame = cap.read()

	Current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	Current = cv2.GaussianBlur(Current, (21, 21), 0)

	if Previous is None:
		Previous = Current
		continue

	frameDelta = cv2.absdiff(Previous, Current)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
 	yavg = 0
 	counter = 0
	for c in cnts:
		if cv2.contourArea(c)<100 or cv2.contourArea(c)>1000:
			continue
 		(x, y, w, h) = cv2.boundingRect(c)
		yavg+=(y+(h/2))
		counter += 1
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	if counter>0:	
		yavg/=counter

	if len(cnts) in range(2, 5):
		if yavg in range(0, size):
			pyautogui.scroll(100)
			if "-p" in sys.argv:
				print "Up"
		else:
			pyautogui.scroll(-100)
			if "-p" in sys.argv:			
				print "Down"	
	
	frame = cv2.flip(frame, 1)	
	if "-v" in sys.argv:
		cv2.imshow("Detected motion", frame)
	
	Previous = Current
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break	
