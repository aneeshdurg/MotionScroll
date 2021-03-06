import cv2
import pyautogui
import sys
from time import time
class motionDetector:
    Previous = None
    bogSub = False
    def __init__(Self, sub):
        Self.bogSub = sub
    def getMotion(Self, Current):
        Current = cv2.cvtColor(Current, cv2.COLOR_BGR2GRAY)
	Current = cv2.GaussianBlur(Current, (21, 21), 0)
	if Self.Previous is None:
	    Self.Previous = Current
	    return False, 0, 0, 0, None
	frameDelta = cv2.absdiff(Self.Previous, Current)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
        if not Self.bogSub:
            Self.Previous = Current
 	yavg = 0
 	counter = 0
        maxArea = -1
	for c in cnts:
            cArea = cv2.contourArea(c)
            if cArea>maxArea:
                maxArea = cArea     
	    if cArea<100 or cArea>1000:
	    	continue
 	    (x, y, w, h) = cv2.boundingRect(c)
	    yavg+=(y+(h/2))
	    counter += 1
	    cv2.rectangle(Current, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	if counter>0:	
		yavg/=counter
        return True, len(cnts), yavg, maxArea,Current 



if "-a" in sys.argv:
	sys.argv=["-v", "-p"]
	
cap = cv2.VideoCapture(0)
size = int(cap.get(4)/2)
upDetector = motionDetector(False)
dnDetector = motionDetector(False)
ltDetector = motionDetector(True)
rtDetector = motionDetector(True)

orgArea, stTime, rtimer, ltimer = 0, 0, False, False


Previous = None
while True:
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)	
        upFrame = frame[0:size-50, 0+int(cap.get(3)/4):int(3*cap.get(3)/4)]
        dnFrame = frame[size+50:,  0+int(cap.get(3)/4):int(3*cap.get(3)/4)]
        ltFrame = frame[:, 0:int(cap.get(3)/4)-50]
        rtFrame = frame[:, int(3*cap.get(3)/4)+50:]
        
        _, uCount, _, _, upFrame = upDetector.getMotion(upFrame)
        _, dCount, _, _, dnFrame = dnDetector.getMotion(dnFrame)
        _, lCount, _, lArea, ltFrame = ltDetector.getMotion(ltFrame)
        s, rCount, _, rArea, rtFrame = rtDetector.getMotion(rtFrame)
        if not s:
            continue
        if "-v" in sys.argv:
            cv2.imshow("up", upFrame)
            cv2.imshow("dn", dnFrame)
            cv2.imshow("lt", ltFrame)
            cv2.imshow("rt", rtFrame)
        if uCount in range(2, 5):
            pyautogui.scroll(100)
            if "-p" in sys.argv:
	        print "Up"
        elif dCount in range(2, 5):
            pyautogui.scroll(-100)
	    if "-p" in sys.argv:			
	        print "Down"	
        elif rArea>7000 and not rtimer:
            rtimer = True
            ltimer = False
            orgArea = rArea
            stTime = time()
        elif lArea>7000 and not ltimer:
            ltimer = True
            rtimer = False
            orgArea = lArea
            stTime = time()
        
        if ltimer:
            if time()-stTime>=2:
                if "-p" in sys.argv:
                    print 'l'
                pyautogui.press('left')
                ltimer = False
            elif abs(lArea - orgArea)>10000:
                ltimer = False
	if rtimer:
            if time()-stTime>=2:
                if "-p" in sys.argv:
                    print 'r'
                pyautogui.press('right')
                rtimer = False
            elif abs(rArea - orgArea)>10000:
                rtimer = False
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break	
