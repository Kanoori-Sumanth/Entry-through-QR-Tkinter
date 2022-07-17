import cv2
import time
# import pandas as pd

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

t1 = time.time()
found = False
while True:
	_, img = cap.read()
	cv2.imshow("Input",img)

	t2 = time.time()

	if(cv2.waitKey(1) & 0xFF==ord('q') or (t2-t1 > 10)):
		break
	
	data,bbox,strai = detector.detectAndDecode(img)
	if(data):
		print(data)
		found = True
		break
	# t2 = time.time()
	# if(t2-t1 > 10): # looks for QRCode for 10 secs and if not found, stops capturing
	# 	break

if(found):
	cv2.imshow("QRCodeScanner",img)
else:
	print("QRCode not detected.. Try again(try to adjust lighting)")
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()

if(data):
	fp = open("data.csv","a+")
	fp.write(data + "\n")
	fp.close()

# print(pd.read_csv("data.csv")) # if needed, data in csv file can be printed onto console using pandas module's read_csv function
