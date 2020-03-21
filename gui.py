import tkinter as tk
import time
import tkinter.filedialog as fd

import cipherlib,rsalib


def btn(frame,text,callback):
    btn=tk.Button(frame)
    btn["text"]=text
    def wrap():
        frame.pack_forget()
        frame.update()
        callback()
        frame.pack()
    btn["command"]=wrap
    return btn

def callback_encode():
    f=tk.Frame(win)
    
    var1=tk.StringVar(value="公钥名：未选择")
    keyfile=None
    def callback0():
        nonlocal var1,keyfile
        keyfile=fd.askopenfilename()
        var1.set("公钥名："+keyfile)
        chosen_key=True
    b=tk.Button(f,text="选择路径",command=callback0)
    b.grid(row=1,column=1)
    l=tk.Label(f,textvariable=var1)
    l.grid(row=0,columnspan=3)

    var2=tk.StringVar(value="文件名：未选择")
    codefile=None
    def callback1():
        nonlocal var2,codefile
        codefile=fd.askopenfilename()
        var2.set("文件名："+codefile)
    b=tk.Button(f,text="选择路径",command=callback1)
    b.grid(row=3,column=1)
    l=tk.Label(f,textvariable=var2)
    l.grid(row=2,columnspan=3)

    def callback3():
        if keyfile==None or codefile==None:
            return
        with open(keyfile,'rb') as f:
            key=rsalib.Key.loads(f)
        with open(codefile,'rb') as f:
            code=f.read()
        print(cipherlib.decode(code,f))
    def callback2():
        f.destroy()
        win.quit()
    tk.Button(f,text="取消",command=callback2).grid(row=4,column=2)
    f.pack()
    
    win.mainloop()

callbacks=[callback_encode]*4
class MainWindow:
    def __init__(self):
        global win
        win=tk.Tk()
        f=tk.Frame(win)
        self.fronts=[]
        for (i,text) in enumerate(("加密","解密","导入证书","生成证书")):
            b=btn(f,text,callbacks[i])
            b.grid(row=i//2,column=i%2)
        f.pack()


if __name__=="__main__":
    m=MainWindow()
        
