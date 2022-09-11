import os.path
import qrcode
import cv2
import time
import json
import re
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from datetime import datetime
from datetime import date



class MainWin(Tk):
	def __init__(self,title,geometry):
		Tk.__init__(self)
		self.title(title)
		self.geometry(geometry)
		self.font = ("Times 20")

	def open(self):
		genBtn = Button(self, text = "Generate", font = self.font, command = lambda:self.openGenerator(self))
		genBtn.pack(padx = 100,pady = 100)

		scanBtn = Button(self, text = "Scan",font = self.font, command = lambda:self.openScanner(self))
		scanBtn.pack(padx = 100, pady = 100)

		self.mainloop()

	def openGenerator(self,mainWin):
		genWin = QRGenerator(mainWin,"QR Generator","1000x500")
		genWin["background"] = "#9fafca"

	def openScanner(self,mainWin):
		try:
			jsonFile = open("student-data.json","r")
		except FileNotFoundError:
			with open("student-data.json","w") as fp:
				fp.write("{\n}")
		scanWin = QRScanner(mainWin,"QR Scanner","1250x800")
		scanWin["background"] = "#9fafca"


class Window(Toplevel):
	def __init__(self,mainWin,title,geometry):
		Toplevel.__init__(self)
		self.title(title)
		self.geometry(geometry)
		self.fields = ["name","mobile","parent mobile","year"]

	def showFrame(self,label,img):
		imgFAr = Image.fromarray(img)
		imgtk = ImageTk.PhotoImage(image=imgFAr)
		label.imgtk = imgtk
		label.configure(image = imgtk)


class ValidatorClass:	# form validator class

	def check_id(self,strg):
		if(len(strg)!=7):
			return False
		if(not(strg[0]=='N' or strg[0]=='n' or strg[0]=='S' or strg[0]=='s')):
			return False
		if(not(strg[1:].isdigit())):
			return False
		return True

	def check_num(self,strg):
		if(len(strg)!=10):
			return False
		if(not(int(strg[0])>=6 and int(strg[0])<=9)):
			return False
		if(not(strg.isdigit())):
			return False
		return True


	def check_name(self,strg, search=re.compile(r'[^a-zA-Z. ]').search):
		return not bool(search(strg))


class QRGenerator(Window):

	def __init__(self,mainWin,title,geometry):
		Window.__init__(self,mainWin,title,geometry)

		self.frameFont = ("Times 20")
		self.folName = "qrc"

		if not(os.path.exists("student-data.json")):
			with open("student-data.json","w") as stjson:
				stjson.write("")
				
		jsonFile = open("student-data.json","r")

		self.validator = ValidatorClass()

		try:
			self.records = json.load(jsonFile)
		except json.decoder.JSONDecodeError:
			messagebox.showwarning("Warning","Somethings wrong with json file or empty file",parent=self)
			self.records = {}

		jsonFile.close()
		

		# ---------------- frame to take details from user ----------------
		formFrame = Frame(self)
		formFrame.grid(row=0,column=0,padx=50,pady=0)

		headLabel = Label(formFrame,text="Enter student details",font=("Times 30"),highlightbackground="black", highlightthickness=2)
		headLabel.grid(row=0,column=0,columnspan=2,padx=10,pady=30)

		Label(formFrame,text="ID:",font=self.frameFont).grid(row=1,column=0,padx=10,pady=10)
		self.idVal = StringVar()
		idEntry = Entry(formFrame,font=self.frameFont,textvariable=self.idVal)
		idEntry.grid(row=1,column=1)
		idEntry.focus_force()

		Label(formFrame,text="Name:",font=self.frameFont).grid(row=2,column=0,padx=10,pady=10)
		self.nameVal = StringVar()
		nameEntry = Entry(formFrame,font=self.frameFont,textvariable=self.nameVal)
		nameEntry.grid(row=2,column=1)

		Label(formFrame,text="Mobile no:",font=self.frameFont).grid(row=3,column=0,padx=10,pady=10)
		self.mobVal = StringVar()
		mobEntry = Entry(formFrame,font=self.frameFont,textvariable=self.mobVal)
		mobEntry.grid(row=3,column=1)

		Label(formFrame,text="Parent mobile:",font=self.frameFont).grid(row=4,column=0,padx=10,pady=10)
		self.parMobVal = StringVar()
		parMobEntry = Entry(formFrame,font=self.frameFont,textvariable=self.parMobVal)
		parMobEntry.grid(row=4,column=1,padx=10,pady=10)

		Label(formFrame,text="Year:",font=self.frameFont).grid(row=5,column=0,padx=10,pady=10)
		self.yearVal = StringVar()
		yearDropDown = OptionMenu(formFrame,self.yearVal,*["P1","P2","E1","E2","E3","E4"])
		yearDropDown.grid(row=5,column=1)


		# ---------------- frame to display QR code generated ----------------

		qrFrame = Frame(self)
		qrFrame.grid(row=0,column=1,padx=50,pady=50)

		self.qrLabel = Label(qrFrame)
		self.qrLabel.grid(row=0,column=0)

		dumImg = np.zeros((370,370))	# dummy black pic to show initially
		Window.showFrame(self,self.qrLabel,dumImg)

		self.qrCapVal = StringVar()
		qrCapLabel = Label(qrFrame,textvariable=self.qrCapVal,font=self.frameFont)
		qrCapLabel.grid(row=1,column=0)


		submitBtn = Button(formFrame,text="Submit",font=self.frameFont,command=lambda:self.createQR())
		submitBtn.grid(row=6,column=0,columnspan=2,pady=30)

	def createQR(self):
		idEntryVal = self.idVal.get().strip().capitalize()
		nameEntryVal = self.nameVal.get().strip()
		mobEntryVal = self.mobVal.get().strip()
		parMobEntryVal = self.parMobVal.get().strip()
		yearVal = self.yearVal.get()

		text = "%s,%s,%s,%s"%(nameEntryVal, mobEntryVal, parMobEntryVal,yearVal)	# fields be saved in json model and not included in QR

		if(self.validator.check_id(idEntryVal)):
			if(self.validator.check_name(nameEntryVal) and len(nameEntryVal)>0):
				if(self.validator.check_num(mobEntryVal)):
					if(self.validator.check_num(parMobEntryVal)):
						if(len(yearVal)>0):
							file_name = idEntryVal
							file_name += ".png"
							file_path = self.folName + "/" + file_name



							if not os.path.isdir(self.folName):
								os.makedirs(self.folName)

							existing = os.listdir(self.folName)

							if(file_name not in existing):
								currentRecord = {}
								data = list(text.split(","))
								index = idEntryVal

								for i in range(len(self.fields)):
									currentRecord[self.fields[i]] = data[i]

								self.records[index] = currentRecord

								jsonFile = open("student-data.json","w")

								json.dump(self.records,jsonFile,indent = 4)

								jsonFile.close()




								qr = qrcode.make(idEntryVal)		# would be converted to encrypted form in future
								
								qr.save(file_path)

							else:
								messagebox.showwarning("Warning","QR for %s already exists"%(file_name),parent=self)


							imgtk = ImageTk.PhotoImage(Image.open(file_path))
							self.qrLabel.imgtk = imgtk
							self.qrLabel.configure(image = imgtk)

							self.qrCapVal.set("QR code for %s"%(file_name))
						else:
							messagebox.showwarning("Error","Select Year!",parent=self)
					else:
						messagebox.showwarning("Error","Parent mobile number invalid!\n(start with 6-9 & has 10 digits)",parent=self)
				else:
					messagebox.showwarning("Error","Mobile number invalid!\n(start with 6-9 & has 10 digits)",parent=self)
			else:
				messagebox.showwarning("Error","Name invalid! \n(Only A-z, ',' and '.' are allowed)",parent=self)
		else:
			messagebox.showwarning("Error","ID number invalid!",parent=self)


class QRScanner(Window):
	def __init__(self,mainWin,title,geometry):
		try:
			jsonFile = open("student-data.json","r")
			self.records = json.load(jsonFile)

			Window.__init__(self,mainWin,title,geometry)
			self.frameFont = ("Times 20")

			leftFrame = Frame(self,highlightbackground="black",highlightthickness=2)
			leftFrame.grid(row=0,column=0,padx=20,pady=50)

			self.camLabel = Label(leftFrame,highlightbackground="black",highlightthickness=2)
			self.camLabel.grid(row=0,column=0,padx=10,pady=10)

			camImg = np.zeros((480,640))	# display black initially

			Window.showFrame(self,self.camLabel,camImg)


			rightFrame = Frame(self,highlightbackground="black",highlightthickness=2)
			rightFrame.grid(row=0,column=1,padx=20,pady=50)

			
			headLabel = Label(rightFrame,text="Student details",font=("Times 30"),highlightbackground="black", highlightthickness=2)
			headLabel.grid(row=0,column=0,columnspan=2,padx=10,pady=30)

			Label(rightFrame,text="ID:",font=self.frameFont).grid(row=1,column=0,padx=10,pady=10)
			self.idVal = StringVar()
			idEntry = Entry(rightFrame,font=self.frameFont,textvariable=self.idVal)
			idEntry.grid(row=1,column=1,padx=10,pady=10)

			Label(rightFrame,text="Name:",font=self.frameFont).grid(row=2,column=0,padx=10,pady=10)
			self.nameVal = StringVar()
			nameEntry = Entry(rightFrame,font=self.frameFont,textvariable=self.nameVal)
			nameEntry.grid(row=2,column=1,padx=10,pady=10)

			Label(rightFrame,text="Mobile no:",font=self.frameFont).grid(row=3,column=0,padx=10,pady=10)
			self.mobVal = StringVar()
			mobEntry = Entry(rightFrame,font=self.frameFont,textvariable=self.mobVal)
			mobEntry.grid(row=3,column=1,padx=10,pady=10)

			Label(rightFrame,text="Parent mobile:",font=self.frameFont).grid(row=4,column=0,padx=10,pady=10)
			self.parMobVal = StringVar()
			parMobEntry = Entry(rightFrame,font=self.frameFont,textvariable=self.parMobVal)
			parMobEntry.grid(row=4,column=1,padx=10,pady=10)

			Label(rightFrame,text="Year:",font=self.frameFont).grid(row=5,column=0,padx=10,pady=10)
			self.yearVal = StringVar()
			yearDropDown = OptionMenu(rightFrame,self.yearVal,*["P1","P2","E1","E2","E3","E4"])
			yearDropDown.grid(row=5,column=1,padx=10,pady=10)

			Label(rightFrame,text="Time:",font=self.frameFont).grid(row=6,column=0,padx=10,pady=10)
			self.timeVal = StringVar()
			timeEntry = Entry(rightFrame,font=self.frameFont,textvariable=self.timeVal)
			timeEntry.grid(row=6,column=1,padx=10,pady=10)

			addBtn = Button(rightFrame,text="Submit",font=self.frameFont,command=lambda:self.addStudent())
			addBtn.grid(row=7,column=0,columnspan=2,padx=10,pady=10)



			self.cap = cv2.VideoCapture(0)
			self.detector = cv2.QRCodeDetector()
			camBtn = Button(leftFrame,text="Scan",command=lambda:self.readAndDecode(time.time()),font=("Times 20"))
			camBtn.grid(row=1,column=0)


		except FileNotFoundError:
			print("student-data.json not found")
			messagebox.showwarning("Error","student-data.json file missing",parent=self)

		except json.decoder.JSONDecodeError:
			messagebox.showwarning("Error","student-data.json file is empty",parent=self)




	def addStudent(self):
		validator = ValidatorClass()
		if(validator.check_id(self.idVal.get())):
			try:
				scanned=f"{self.idVal.get()} - {self.nameVal.get()} - {self.mobVal.get()} - {self.parMobVal.get()} - {self.yearVal.get()} - {self.timeVal.get()}"
				curRecord = scanned.split(" - ")
				dat = str(date.today())
				branches = {"N":"Nzd","S":"Sklm"}
				excel_file_name = dat+"_"+curRecord[4]+"_"+branches[self.idVal.get()[0]]+"_"+".xlsx"	# date_branch_year.xlsx
				yearVal = curRecord[4]

				if not(os.path.exists(excel_file_name)):
					df = pd.DataFrame({"ID":[],
										"Name":[],
										"Mobile":[],
										"Parent":[],
										"Year":[],
										"Out time":[],
										"In time":[]})
					new_xl_writer = pd.ExcelWriter(excel_file_name,engine="xlsxwriter")
					df.to_excel(new_xl_writer,sheet_name="Sheet1",index=False)
					new_xl_writer.save()

					messagebox.showwarning("Warning","Created new xl file",parent=self)
				else:
					messagebox.showwarning("Warning","File already present",parent=self)



				prevData = pd.read_excel(excel_file_name,sheet_name="Sheet1")
				
				print("have read excel file sheet")

				ids = list(prevData["ID"])

				xl_writer = pd.ExcelWriter(excel_file_name,engine="xlsxwriter")
				print("defined xl_writer")



				if curRecord[0] in ids:
					curTime = datetime.now().strftime("%H:%M:%S")
					curRecord.append(curTime)
					ind = ids.index(curRecord[0])
					messagebox.showwarning("Warning","Student record found. Adding intime",parent=self)

				else:
					curRecord.append("-")
					ind = len(prevData.index)
					messagebox.showwarning("Warning","Student record not found. Adding record",parent=self)
					print("not in prevData")

				prevData.loc[ind] = curRecord

				prevData.to_excel(xl_writer,sheet_name="Sheet1",index=False)
				print("to_excel done")
				xl_writer.save()
				print("xl_writer saved")
				prevData = None

			except FileNotFoundError:
				messagebox.showwarning("Warning","Excel file not found!",parent=self)

			except ValueError:
				messagebox.showwarning("Warning",f"Provided sheet_name {yearVal} not found in excel file.",parent=self)
		else:
			messagebox.showwarning("Error","Invalid ID number",parent=self)
		

	def readAndDecode(self,t1):
		camImg = cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
		Window.showFrame(self,self.camLabel,camImg)


		qrdata,bbox,strai = self.detector.detectAndDecode(camImg)
		validator = ValidatorClass()
		if(qrdata):
			if validator.check_id(qrdata):
				self.idVal.set(qrdata)

				currentRecord = self.records[qrdata]

				self.nameVal.set(currentRecord["name"])
				self.mobVal.set(currentRecord["mobile"])
				self.parMobVal.set(currentRecord["parent mobile"])
				self.yearVal.set(currentRecord["year"])
				date = datetime.now().strftime("%H:%M:%S")
				self.timeVal.set(date)


				return qrdata,True
			else:
				messagebox.showwarning("Error","Invalid QR",parent=self)

		t2 = time.time()
		if(cv2.waitKey(1) & 0xFF==ord('q') or (t2-t1>5)):
			messagebox.showwarning("Warning","QR code not detected",parent=self)
			return "",False


		self.camLabel.after(10,self.readAndDecode,t1)
