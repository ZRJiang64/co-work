# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:06:16 2023

@author: ZR_laptop
"""
#1.10大改了程式碼變成比較好閱讀
#1.11更變裁切範圍時，會超出圖片的bug
#圖片比螢幕大，且圖片可以調整大小
#把button從圖片換成文字
import tkinter as tk
from tkinter.filedialog import askopenfilename,askdirectory
from tkinter import filedialog,Frame,Entry,Button,Label,Checkbutton ,ttk,IntVar,StringVar
from tkinter import X,LEFT,SE, SUNKEN ,BOTTOM,RIGHT
from tkinter import messagebox
import cv2, os 
from PIL import Image, ImageTk

#選擇影片
def fileopen():
    file_sql = askopenfilename(title='選擇',
                                        filetypes=[
                                            ("video files","*.mp4"),
                                            ("video files","*.avi"),
                                            ("video files","*.wmv"),
                                            ("video files","*.flv"),
                                            ("video files","*.mkv"),
                                            ("video files","*.mov"),
                                            ('All Files','*')])
    vc = cv2.VideoCapture(file_sql)
    fps = vc.get(cv2.CAP_PROP_FPS)
    point = '[[0,0],[' + str(int(vc.get(3))) +',' + str(int(vc.get(4)))+']]' #picture's size
    vc.release() #release resource
    
    if file_sql:
        v1.set(file_sql)
        v3.set(int(fps))
        v4.set(point)
        v6.set(100)
        statustext.set('Frames per second:'+str(fps))


#選擇輸出資料夾
def folder_open():
    file_YuD =askdirectory()
    if file_YuD:
        v2.set(file_YuD)
        
# 把點限制在圖片內
def PointInPicture (point , size):
    for i in range(len(point)):
        if point[i][0] < 0 :
            point[i][0] = 0
        elif point[i][0] > size[1]:
            point[i][0] = size[1]
        if point[i][1] < 0 :
            point[i][1] = 0
        elif point[i][1] > size[0]:
            point[i][1] = size[0]
    if point[0][0] > point[1][0] :
        point[0][0] , point[1][0] = point[1][0] , point[0][0]
    if point[0][1] > point[1][1] :
        point[0][1] , point[1][1] = point[1][1] , point[0][1]
    return point

#剪裁範圍
def cut ():
    def mouse_handler(event, x, y, flags,prog):
        if event == cv2.EVENT_LBUTTONDOWN:
            dots[0][0],dots[0][1] = x,y
            
            
        if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            img = img2.copy()
            cv2.rectangle(img, (dots[0][0],dots[0][1]), (x, y), (0, 0, 255), 1)
            cv2.imshow('img',img)
            
        if event == cv2.EVENT_LBUTTONUP:
            dots[1][0],dots[1][1] = x,y

    # main code of cut
    vpath = v1.get() #video path
    if vpath == '' :
        messagebox.showwarning("warm!", "請填入影片位置")
    else:
        img = cv2.VideoCapture(vpath).read()[1]
        dots = [[0,0],[0,0]]
        cv2.namedWindow('img',0)
        #將圖片調整成比螢幕小
        if img.shape[1] > screen_w:
            r = (screen_w*0.8)/img.shape[1]
            cv2.resizeWindow('img', int(img.shape[1]*r) , int(img.shape[0]*r))
        if img.shape[0] > screen_h:
            r = (screen_h*0.8)/img.shape[0]
            cv2.resizeWindow('img', int(img.shape[1]*r) , int(img.shape[0]*r))
        cv2.imshow('img',img)
        img2 = img.copy()
        cv2.setMouseCallback("img", mouse_handler)
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        dots = PointInPicture(dots,img.shape)
        v4.set(str(dots))
        
        
##keep the same of digital of filename
def name(no:int,total:int): 
    no , total = str(no), str(total)
    nlen, tnlen = int(len(no)), int(len(total))
    for i in range(tnlen - nlen):
        no = '0' + no
    return no

## 轉換
def convert():
    vpath = v1.get() #video path
    fpath = v2.get() #save folder path 
    interval = v3.get() #capture interval
    img_rag = v4.get() # image range
    quality = v6.get() # image quality
    bw2wb = v5.get() #black_white to white_black
    
    if vpath == '' or interval==0 or img_rag=='' or quality == 0:
        messagebox.showwarning("warm!", "請填入影片位置")
    elif fpath == '':
        messagebox.showwarning("warm!", "請填入輸出位置")
    else:    
        img_rag = eval (img_rag)
        vc = cv2.VideoCapture(vpath) #video
        os.chdir(fpath) #adress change to save adress
        number = 1 #number of screen
        all_number = int(vc.get(7))//interval #number of saving picture
        temp = 1 #inital value of state bar 
        if vc.isOpened(): #chick video input
            rval, frame = vc.read() #rval  is Boolean ,pic is the first picture
        else:
            rval = False
        while rval:
            rval, frame = vc.read()
            
            #更新state bar 顯示 進度
            
            if number % (vc.get(7) // 20) == 0:
                bar['value']=5*temp
                temp += 1
                window.update()
            
            #依照週期挑選圖片，並選擇功能，然後儲存
            if number % interval == 0:
                frame = frame[img_rag[0][1]:img_rag[1][1],img_rag[0][0]:img_rag[1][0]] 
                if bw2wb == 1:
                    frame = 255 -frame
                cv2.imwrite( name(number//interval , all_number ) + '.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, quality])
                cv2.waitKey(0)
            number += 1
        vc.release()

def information():
    
    messagebox.showinfo("使用說明",'1.capture interval為整數，每章擷取的圖片間隔的禎數\n'+
                        '2.壓縮比的範圍從0到100，100為無損失，0為完全損失\n'+
                        '3.裁切功能為滑鼠左鍵拖曳，裁切完後點選任意按鍵\n'
                        '4.有問題可以找我')
    
if __name__ == '__main__':
    window = tk.Tk()
    window.title('viedo2photo.exe') 
    window.geometry('650x300') #width x height +start x+start y
    screen_w = window.winfo_screenwidth() #width of windows os screen 
    screen_h = window.winfo_screenheight() #height7 of windows os screen 
    # in-output area
    in_put = Frame(window)
    in_put.pack(pady= 5)
    v1 = StringVar(value = "") #影片地址
    ent = Entry(in_put, width=50, textvariable=v1).pack(side='left',padx=10)
    btn = Button(in_put, width=20, text='影片位置', font=(14), command=fileopen).pack()
    
    out_put = Frame(window)
    out_put.pack(pady= 5)
    v2 = StringVar(value = "") #輸出資料夾
    ent = Entry(out_put, width=50, textvariable=v2).pack(side='left',padx=10) 
    btn = Button(out_put, width=20, text='輸出位置', font=(14), command=folder_open)
    btn.pack()
    
    setting = tk.Frame(window)
    setting.pack(pady= 5)
    v3 = IntVar(value=None) #擷取圖片頻率
    v4 = StringVar(value ="") #裁切圖片範圍
    v5 = IntVar(value = None) #黑色白色反轉
    v6 = IntVar(value =None) #圖片壓縮比
    lbl = Label(setting, text='Capture Interval:', font=('Arial', 12))
    lbl.pack(side=LEFT)
    ent = Entry(setting, width=5, textvariable=v3).pack( side=LEFT,padx=10)
    ext = Button(setting, width=8, text='裁切範圍', font=('新細明體',12), command=cut)
    ext.pack(side=LEFT)
    lbl = Label(setting, text='：', font=('新細明體', 12)) 
    lbl.pack(side=LEFT)
    ent = Entry(setting, width= 15, textvariable=v4)
    ent.pack(side=LEFT)
    lbl = Label(setting, text='壓縮比：', font=('新細明體', 12)).pack(fill=X,side=LEFT)
    ent = Entry(setting, width=5, textvariable=v6).pack(fill=X, side=LEFT)
    C1 = Checkbutton(setting, text = "黑白反轉", variable = v5,onvalue = 1,font=('新細明體', 12), offvalue = 0,width = 10)
    C1.pack()
    
    
    trans = Frame(window)
    trans.pack(pady=10)
    

    ext = Button(trans, width=10, text='轉換', font=(14), command=convert)
    ext.pack(fill=X,padx=50, side=LEFT)
    
    author = Frame(window)
    author.pack(pady=10)
    """
    img = Image.open('i.jpg')
    img = img.resize((15,15),Image.BILINEAR )
    photo = ImageTk.PhotoImage(img)
    ext = Button(author,image=photo,command=information).pack(side=RIGHT)
    """
    ext = Button(author,text ='i',bg='lightblue',command=information)
    ext.config(width='2', height='1')
    ext.pack(side=RIGHT)
    lbl = Label(author, text='version:1.11    by:JZR', font=('Arial', 8)).pack(anchor=SE,padx=200) 
    
    bar = ttk.Progressbar(window,orient='horizontal',length=550,maximum=100 )
    bar.pack(pady=10)
    
    
    statustext = StringVar()
    statustext.set('status bar')
    statusbar = Label(window, textvariable=statustext, relief=SUNKEN, anchor='w')
    statusbar.pack(side=BOTTOM, fill=X)
    
    window.mainloop()