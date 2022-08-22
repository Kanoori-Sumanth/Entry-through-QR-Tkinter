from classes import MainWin
from tkinter import *

if __name__ == "__main__":
	mainWindow = MainWin("Student Entry/Exit through QR","800x500")
	mainWindow["background"] = "#9fafca"
	mainWindow.open()

# TODO:

	# what if an id is scanned and it is not present in json file.
	# handle exception while trying to take data of certain id from json file
