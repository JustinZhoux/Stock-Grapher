from tkinter import *
from Stocks2 import *
def click():
	entered_text = e1.get()
	output.delete(0.0,END)
	try:
		draw(entered_text)
		output.insert(END,"Generating graph")
	except ValueError:
		output.insert(END,"Please check your input ticker")


root = Tk()
root.title("Stock Graphs")
Label(root, text = "Enter the stock ticker").grid(row = 0)
e1 = Entry(root)
e1.grid (row=0, column=1)
Button(root,text = "Graph",command = click).grid(row=2,column=0,sticky = W)
Label(root,text = "\nFeedback :") .grid(row = 4,column=0,sticky = W)
output = Text(root, width = 30, height = 5, wrap = WORD)
output.grid(row = 5, column = 0, columnspan = 2, sticky = W)
root.mainloop()