import subprocess
import Tkinter as tk

root = tk.Tk()

canvasMain = tk.Canvas(root, width = 350, height = 250)
canvasMain.pack()

def deployCompile():
    from compileall import compile_dir
    compile_dir('E:\Python\IVM\IVM\source\ivm')

def deployMain():
    subprocess.call([r'E:\Python\IVM\IVM\source\deply - Main.bat'])

buttonCompile = tk.Button (root,text='Compile',command=deployCompile,bg='red',fg='white')
buttonMain = tk.Button (root,text='Deploy wotmod',command=deployMain,bg='green',fg='white')
canvasMain.create_window(170,130, window=(buttonCompile, buttonMain))

root.mainloop()
