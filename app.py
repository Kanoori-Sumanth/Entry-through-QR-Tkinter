import os
import sys
import qrcode
import cv2
import time
import numpy as np
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from datetime import datetime
# from qrscan import QrScanner
# from qrgen import QrGenerator

folName = "qrc"

if not os.path.isdir(folName):
	os.makedirs(folName)

def createQR(idEntry,nameEntry,mobEntry,parMobEntry,genWin,qrLabel,qrCapVal,warnVal):
	global folName
	idEntryVal = idEntry.get().strip()
	nameEntryVal = nameEntry.get().strip()
	mobEntryVal = mobEntry.get().strip()
	parMobEntryVal = parMobEntry.get().strip()
	text = "%s,%s,%s,%s"%(idEntryVal, nameEntryVal, mobEntryVal, parMobEntryVal)	# would be saved in json model and not included in QR in the future
	if((len(idEntryVal)!=0 and len(nameEntryVal)!=0 and len(mobEntryVal)!=0 and len(parMobEntryVal)!=0)):
		file_name = idEntry.get()
		file_name += ".png"
		file_path = folName + "/" + idEntry.get() + ".png"

		warnVal.set("")

		existing = os.listdir(folName)

		if(file_name not in existing):
			img = qrcode.make(text)	# would be converted to encrypted form in future
			img.save(file_path)

		else:
			# messagebox.showwarning("Warning","QR for %s already exists"%(file_name))
			warnVal.set("QR for %s already exists"%(file_name))


		imgtk = ImageTk.PhotoImage(Image.open(file_path))
		qrLabel.imgtk = imgtk
		qrLabel.configure(image = imgtk)

		qrCapVal.set("QR code for %s"%(file_name))

	else:
		# messagebox.showwarning("Warning","Some field missing",master=genWin)
		warnVal.set("Some field missing")

		



def openGenerator(win):
	genWin = Toplevel(win)
	genWin.title("Generate QR Code")
	genWin.geometry("1000x500")

	frameFont = ("Times 20")

	formFrame = Frame(genWin)
	formFrame.grid(row=0,column=0,padx=50,pady=0)


	headLabel = Label(formFrame,text="Enter student details",font=("Times 30"),highlightbackground="black", highlightthickness=2)
	headLabel.grid(row=0,column=0,columnspan=2,padx=10,pady=30)

	Label(formFrame,text="ID:",font=frameFont).grid(row=1,column=0,padx=10,pady=10)
	idVal = StringVar()
	idEntry = Entry(formFrame,font=frameFont,textvariable=idVal)
	idEntry.grid(row=1,column=1)
	idEntry.focus_force()

	Label(formFrame,text="Name:",font=frameFont).grid(row=2,column=0,padx=10,pady=10)
	nameVal = StringVar()
	nameEntry = Entry(formFrame,font=frameFont,textvariable=nameVal)
	nameEntry.grid(row=2,column=1)

	Label(formFrame,text="Mobile no:",font=frameFont).grid(row=3,column=0,padx=10,pady=10)
	mobVal = StringVar()
	mobEntry = Entry(formFrame,font=frameFont,textvariable=mobVal)
	mobEntry.grid(row=3,column=1)

	Label(formFrame,text="Parent mobile:",font=frameFont).grid(row=4,column=0,padx=10,pady=10)
	parMobVal = StringVar()
	parMobEntry = Entry(formFrame,font=frameFont,textvariable=parMobVal)
	parMobEntry.grid(row=4,column=1)

	# frame to display QR code generated

	qrFrame = Frame(genWin)
	qrFrame.grid(row=0,column=1,padx=50,pady=50)

	qrLabel = Label(qrFrame)
	qrLabel.grid(row=0,column=0)

	qrCapVal = StringVar()
	qrCapLabel = Label(qrFrame,textvariable=qrCapVal,font=frameFont)
	qrCapLabel.grid(row=1,column=0)

	dumImg = np.zeros((370,370))	# dummy black pic to show initially
	showFrame(qrLabel,dumImg)

	warnVal = StringVar()
	warnLabel = Label(formFrame,textvariable=warnVal,font=("Times 30"))		# used to display any warnings like field missing, already exists, or data length issues to the user
	warnLabel.grid(row=6,column=0,columnspan=2)

	submitBtn = Button(formFrame,text="Submit",font=frameFont,command=lambda:createQR(idEntry,nameEntry,mobEntry,parMobEntry,genWin,qrLabel,qrCapVal,warnVal))
	submitBtn.grid(row=5,column=0,columnspan=2,pady=30)




def showFrame(label,img):
	imgFAr = Image.fromarray(img)
	imgtk = ImageTk.PhotoImage(image=imgFAr)
	label.imgtk = imgtk
	label.configure(image = imgtk)


found = False
def readAndDecode(cap,camLabel,detector,t1,idVal,nameVal,mobVal,parMobVal,timeVal):
	global found
	camImg = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
	showFrame(camLabel,camImg)


	data,bbox,strai = detector.detectAndDecode(camImg)
	if(data):
		print(data)
		dataList = data.split(",")
		idVal.set(dataList[0])
		nameVal.set(dataList[1])
		mobVal.set(dataList[2])
		parMobVal.set(dataList[3])
		date = str(datetime.fromtimestamp(1887639468))		# print date and time from POSIX timestamp
		print(date)
		timeVal.set(date)

		# add script to write data to excel sheet

		return data,True

	t2 = time.time()
	if(cv2.waitKey(1) & 0xFF==ord('q') or (t2-t1>5)):
		print("Not detected")
		return "",False




	camLabel.after(10,readAndDecode,cap,camLabel,detector,t1,idVal,nameVal,mobVal,parMobVal,timeVal)


def openScanner(win):
	scanWin = Toplevel(win)
	scanWin.title("Scan QR Code")
	scanWin.geometry("1250x800")

	frameFont = ("Times 20")

	leftFrame = Frame(scanWin,highlightbackground="black",highlightthickness=2)
	leftFrame.grid(row=0,column=0,padx=20,pady=50)

	camLabel = Label(leftFrame,highlightbackground="black",highlightthickness=2)
	camLabel.grid(row=0,column=0,padx=10,pady=10)

	camImg = np.zeros((480,640))	# display black initially

	showFrame(camLabel,camImg)

	# Add button to initialize cam and assign it a command to method with below code
	# cap = cv2.VideoCapture(0)
	# detector = cv2.QRCodeDetector()
	# t1 = time.time()
	# detected = readAndDecode(cap,camLabel,detector,t1)


	rightFrame = Frame(scanWin,highlightbackground="black",highlightthickness=2)
	rightFrame.grid(row=0,column=1,padx=20,pady=50)

	
	headLabel = Label(rightFrame,text="Student details",font=("Times 30"),highlightbackground="black", highlightthickness=2)
	headLabel.grid(row=0,column=0,columnspan=2,padx=10,pady=30)

	Label(rightFrame,text="ID:",font=frameFont).grid(row=1,column=0,padx=10,pady=10)
	idVal = StringVar()
	idEntry = Entry(rightFrame,font=frameFont,textvariable=idVal)
	idEntry.grid(row=1,column=1,padx=10,pady=10)

	Label(rightFrame,text="Name:",font=frameFont).grid(row=2,column=0,padx=10,pady=10)
	nameVal = StringVar()
	nameEntry = Entry(rightFrame,font=frameFont,textvariable=nameVal)
	nameEntry.grid(row=2,column=1,padx=10,pady=10)

	Label(rightFrame,text="Mobile no:",font=frameFont).grid(row=3,column=0,padx=10,pady=10)
	mobVal = StringVar()
	mobEntry = Entry(rightFrame,font=frameFont,textvariable=mobVal)
	mobEntry.grid(row=3,column=1,padx=10,pady=10)

	Label(rightFrame,text="Parent mobile:",font=frameFont).grid(row=4,column=0,padx=10,pady=10)
	parMobVal = StringVar()
	parMobEntry = Entry(rightFrame,font=frameFont,textvariable=parMobVal)
	parMobEntry.grid(row=4,column=1,padx=10,pady=10)

	Label(rightFrame,text="Time:",font=frameFont).grid(row=5,column=0,padx=10,pady=10)
	timeVal = StringVar()
	timeEntry = Entry(rightFrame,font=frameFont,textvariable=timeVal)
	timeEntry.grid(row=5,column=1,padx=10,pady=10)


	cap = cv2.VideoCapture(0)
	detector = cv2.QRCodeDetector()
	camBtn = Button(leftFrame,text="Scan",command=lambda:readAndDecode(cap,camLabel,detector,time.time(),idVal,nameVal,mobVal,parMobVal,timeVal),font=("Times 20"))
	camBtn.grid(row=1,column=0)




	# if(detected):
	# 	fp = open("data.csv","a+")
	# 	fp.write(data)
	# 	fp.close()

	# display id, name, etc details from decoded QR






if __name__ == "__main__":
	win = Tk()
	win.title("Student entry through QR")
	win.geometry("800x500")

	# scan_win = ScannerWindow(win)
	
	gen_btn = Button(win,text="Generate",command=lambda:openGenerator(win),font=("Times 20"))
	gen_btn.pack(padx=100,pady=100)

	scan_btn = Button(win,text="Scan",command=lambda:openScanner(win),font=("Times 20"))
	scan_btn.pack(padx=100,pady=100)

	win.mainloop()
