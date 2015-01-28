import tkinter
import tkinter.scrolledtext  as ScrolledText 
from tkinter import Menu  as Menu 
from tkinter import messagebox, filedialog
from tkinter import BOTH, END, LEFT

root = tkinter.Tk(className="Just another Text Editor")
textPad = ScrolledText.ScrolledText(root, width=40, height=40) # creates text area
filename = None

# create a menu
def new_command():
	textPad.delete('1.0', END)	#clear the text editor

def open_command():
	global filename
	file = filedialog.askopenfile(parent=root,mode='rb',title='Select a file')
	if file != None:
		filename = file.name
		print(filename)
		contents = file.read()
		textPad.delete('1.0', END)	#clear the text editor
		textPad.insert('1.0',contents)
		file.close()
 
def save_command():
	if filename==None:
		file = filedialog.asksaveasfile(mode='w', initialfile=filename)
	else:
		file = open(filename, mode='w')
	if file != None:
	# slice off the last character from get, as an extra return is added
		data = textPad.get('1.0', END+'-1c')
		file.write(data)
		file.close()
		
def saveAs_command():
	global filename
	file = filedialog.asksaveasfilename()
	if file != None:
		filename = file
		with open(filename, mode='w') as file:
			data = textPad.get('1.0', END+'-1c')
			file.write(data)

def exit_command():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
 
def about_command():
    label = messagebox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")
	
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=new_command)
filemenu.add_command(label="Open...", command=open_command)
filemenu.add_command(label="Save", command=save_command)
filemenu.add_command(label="Save As...", command=saveAs_command)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)
# end of menu creation
 
textPad.pack()
root.mainloop()