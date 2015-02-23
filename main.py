import tkinter
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledText
from tkinter import Menu
from tkinter import messagebox, filedialog
from tkinter import BOTH, END, LEFT


def loadSyntaxHL():
	dic = {'red':[], 'green':[], 'blue':[], 'purple':[], 'comment':[]}
	with open('java.dat', mode='r') as f:
		for line in f:
			line = line.split('=')
			s = line[0].strip()
			l = [x.strip() for x in line[1].split(',')]
			dic[s] = l
	return dic

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)



class Editor:

	def highlight_pattern(self, pattern, tag, start="1.0", end="end",regexp=False):
		global root, textPad, statusText
		start = textPad.index(start)
		end = textPad.index(end)
		textPad.mark_set("matchStart", start)
		textPad.mark_set("matchEnd", start)
		textPad.mark_set("searchLimit", end)

		count = tk.IntVar()
		while True:
			index = textPad.search(pattern, "matchEnd","searchLimit",
								count=count, regexp=regexp)
			if index == "": break
			textPad.mark_set("matchStart", index)
			textPad.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
			textPad.tag_add(tag, "matchStart", "matchEnd")

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
		
	def key_press(self, event):
		global root, textPad, statusText
		self.linenumbers.redraw(event)
		self.get_position(event)
		textPad.tag_remove("red", "1.0", END)
		textPad.tag_remove("blue", "1.0", END)
		textPad.tag_remove("green", "1.0", END)
		textPad.tag_remove("purple", "1.0", END)
		for color in self.dic.keys():
			if color == 'comment':
				for word in self.dic[color]:
					self.highlight_pattern(r"%s[^\n]*" % word, color, regexp=True)
			else:
				for word in self.dic[color]:
					self.highlight_pattern(r"\y%s\y" % word, color, regexp=True)
	
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
		
		self.linenumbers = TextLineNumbers(root, width=30)
		self.linenumbers.attach(textPad)
		self.linenumbers.pack(side="left", fill="y")
		
		textPad.bind("<KeyPress>", self.key_press)
		textPad.bind("<KeyRelease>", self.key_press)	
		#root.bind("<Button>", self.key_press)		
		textPad.vbar.bind("<Motion>", self.key_press)		
		
		textPad.tag_configure("red", foreground="#ff0000")
		textPad.tag_configure("blue", foreground="#0000ff")
		textPad.tag_configure("green", foreground="#00ff00")
		textPad.tag_configure("black", foreground="#000000")
		textPad.tag_configure("purple", foreground="#800080")
		textPad.tag_configure("comment", foreground="#AAAAAA")

		
		text=''
		self.filename = file
		if file:
			with open(file, mode='rb') as f:
				text = f.read()
		textPad.delete('1.0', END)
		textPad.insert('1.0', text)
		textPad.mark_set(INSERT, '1.0')
		textPad.focus()
		
		self.dic = loadSyntaxHL()
		
		textPad.pack()
		root.mainloop()

if __name__ == '__main__':
    try:
        Editor(file=sys.argv[1])
    except IndexError:
        Editor()