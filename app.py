import os
import sys
import qrcode
import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from datetime import datetime
# from qrscan import QrScanner
# from qrgen import QrGenerator

folName = "qrc"

if not os.path.isdir(folName):
	os.makedirs(folName)

def createQR(idEntry,nameEntry,mobEntry,genWin):
	global folName
	text = "%s,%s,%s,"%(idEntry.get(), nameEntry.get(), mobEntry.get())	# would be converted to encrypted form in future
	if(not(len(idEntry.get())==0 or len(nameEntry.get())==0 or len(mobEntry.get())==0)):
		text += str(datetime.today().date())
		file_name = idEntry.get()
		file_name += ".png"
		file_path = folName + "/" + idEntry.get() + ".png"

		existing = os.listdir(folName)

		if(file_name not in existing):
			img = qrcode.make(text)	# would be converted to encrypted form in future
			img.save(file_path)

			# while(1):
			# 	cv2.imshow("Take pic",img)
			# 	if(cv2.waitKey(0) & 0xFF==ord('q')):
			# 		break
		

		else:
			messagebox.showwarning("Warning","QR for %s already exists"%(file_name))

		img = cv2.imread(file_path)
		cv2.imshow("QR code for %s"%(file_name),img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		# genWin.destroy()
	else:
		messagebox.showwarning("Warning","Some field missing",master=genWin)

	# sys.exit(0)


def openGenerator(win):
	genWin = Tk()
	genWin.title("Generate QR Code")
	genWin.geometry("600x500")

	frameFont = ("Times 20")

	frame = Frame(genWin)
	frame.grid(row=0,column=0,padx=90,pady=100)

	Label(frame,text="Enter student details",font=("Times 30"),highlightbackground="black", highlightthickness=2).grid(row=0,column=0,columnspan=2,padx=10,pady=10)

	Label(frame,text="ID:",font=frameFont).grid(row=1,column=0,padx=10,pady=10)
	idVal = StringVar()
	idEntry = Entry(frame,font=frameFont,textvariable=idVal)
	idEntry.grid(row=1,column=1)
	# idEntry.focus_force()

	Label(frame,text="Name:",font=frameFont).grid(row=2,column=0,padx=10,pady=10)
	nameVal = StringVar()
	nameEntry = Entry(frame,font=frameFont,textvariable=nameVal)
	nameEntry.grid(row=2,column=1)

	Label(frame,text="Mobile no:",font=frameFont).grid(row=3,column=0,padx=10,pady=10)
	mobVal = StringVar()
	mobEntry = Entry(frame,font=frameFont,textvariable=mobVal)
	mobEntry.grid(row=3,column=1)

	# msgVal = StringVar()
	msgLabel = Label(frame,font=frameFont,text="Press 'q' to close QR",highlightbackground="black", highlightthickness=2)
	msgLabel.grid(row=5,column=0,columnspan=2,)

	submitBtn = Button(frame,text="Submit",font=frameFont,command=lambda:createQR(idEntry,nameEntry,mobEntry,genWin))
	submitBtn.grid(row=4,column=0,columnspan=2)



	# Label(genWin,text="Sometext",font=("Times 20")).pack(padx=10,pady=10)



def openScanner(win):
	scanWin = Tk()
	scanWin.title("Scan QR Code")
	scanWin.geometry("1000x800")

	Label(scanWin,text="Sometext",font=("Times 20")).pack(padx=10,pady=10)


if __name__ == "__main__":
	win = Tk()
	win.title("Student entry through QR")
	win.geometry("800x500")

	# scan_win = ScannerWindow(win)
	
	gen_btn = Button(win,text="Generate",command=lambda:openGenerator(win))
	# gen_btn.font = ("Times 30")
	gen_btn.pack(padx=100,pady=100)

	scan_btn = Button(win,text="Scan",command=lambda:openScanner(win))
	# scan_btn.font = ("Times 30")
	scan_btn.pack(padx=100,pady=100)

	win.mainloop()
