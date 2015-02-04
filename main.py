import tkinter
from tkinter import *
import tkinter.scrolledtext as scrolledText
from tkinter import Menu
from tkinter import messagebox, filedialog
from tkinter import BOTH, END, LEFT

class Editor:

	def new_command(self):
		textPad.delete('1.0', END)	#clear the text editor

	def open_command(self):
		file = filedialog.askopenfile(parent=root,mode='rb',title='Select a file')
		if file != None:
			self.filename = file.name
			contents = file.read()
			textPad.delete('1.0', END)	#clear the text editor
			textPad.insert('1.0',contents)
			file.close()
	 
	def save_command(self):
		if not self.filename:
			file = filedialog.asksaveasfile(mode='w')
		else:
			file = open(self.filename, mode='w')
		if file != None:
		# slice off the last character from get, as an extra return is added
			self.filename = file.name
			data = textPad.get('1.0', END+'-1c')
			file.write(data)
			file.close()
			
	def saveAs_command(self):
		#print(textPad.get('0.0',END))
		file = filedialog.asksaveasfilename()
		if file != None and file != "":
			self.filename = file
			with open(filename, mode='w') as file:
				data = textPad.get('1.0', END+'-1c')
				file.write(data)

	def exit_command(self):
		if messagebox.askokcancel("Quit", "Do you really want to quit?"):
			root.destroy()
	 
	def about_command(self):
		label = messagebox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")
		
	def get_position(self, event):
		"""get the line and column number of the text insertion point"""
		line, column = textPad.index('insert').split('.')
		end, gb = textPad.index('end').split('.')
		self.lines = int(end)-1
		s = "Lines: %d   line=%s column=%s" % (self.lines, line, column)
		statusText.set(s)
	
	def __init__(self, file=None):
		global root, textPad, statusText
		root = Tk(className="Python IDE")	
		textPad = scrolledText.ScrolledText(root, width=80, height=20) # creates text area	
		menu = Menu(root)
		root.config(menu=menu)
		filemenu = Menu(menu, tearoff=0)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", command=self.new_command)
		filemenu.add_command(label="Open...", command=self.open_command)
		filemenu.add_command(label="Save", command=self.save_command)
		filemenu.add_command(label="Save As...", command=self.saveAs_command)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.exit_command)
		helpmenu = Menu(menu, tearoff=0)
		menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About...", command=self.about_command)
		# end of menu creation
		
		# toolbar creation
		toolbar = Frame(root, bg = "grey")
		saveBtn = Button(toolbar, text="Save", command=self.save_command)
		saveBtn.pack(side=LEFT, padx=2, pady=2)
		toolbar.pack(side=TOP, fill=X)
		
		# status bar creation
		statusText = StringVar()
		status = Label(root, text="Info", textvariable=statusText, bd=1, relief=SUNKEN, anchor=W)
		status.pack(side=BOTTOM, fill=X)
		
		
		textPad.bind("<KeyRelease>", self.get_position)		
		
		text=''
		self.filename = file
		if file:
			with open(file, mode='rb') as f:
				text = f.read()
		textPad.delete('1.0', END)
		textPad.insert('1.0', text)
		textPad.mark_set(INSERT, '1.0')
		textPad.focus()
		
		textPad.pack()
		root.mainloop()

if __name__ == '__main__':
    try:
        Editor(file=sys.argv[1])
    except IndexError:
        Editor()

