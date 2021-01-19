from tkinter import *
import random
import pygame as py
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

#initialize the window
root=Tk()
root.title("Music")
root.geometry("700x480+320+100")
root.resizable(0,0)
root.call('wm', 'iconphoto', root._w,PhotoImage(file='Images/music.png'))
#initilize the pygame mixer
py.mixer.init()


# add songs in the playlist
global count
count=0
def addsong():
    global count
    songs=filedialog.askopenfilenames(initialdir='D:\\',title="Choose The Songs",filetypes=(("mp3files","*.mp3"),))
    for song in songs:
        songaddress=song
        songname=song.rsplit('/')
        record=[songaddress,songname[len(songname)-1]]
        tree.insert(parent='', index='end', iid=count, text="Parent", values=(record[1], record[0]))
        count+=1

global pau
global stopped
global currentsong
global songcount
global shuffleb
global repeatb
songcount=0
pau=True
stopped=True
currentsong=''
shuffleb=False
repeatb=False
#play the song
def playsong():
    global currentsong
    if currentsong=='':
        global pau
        global stopped
        slider.config(value=0)
        Play.grid_forget()
        pause.grid(row=0,column=0)
        selected=tree.focus()
        values=tree.item(selected,'values')
        song=values[1]
        currentsong=song
        py.mixer.music.load(song)
        py.mixer.music.play(loops=0)
        Volume_slider.set(py.mixer.music.get_volume())
        pau=False
        stopped=False
        if songcount==0:
            songtime()
    else:
         py.mixer.music.unpause()
         pau=False
         Play.grid_forget()
         pause.grid(row=0,column=0)

#stop the song
def stopsong():
    global stopped
    global songcount
    global currentsong
    currentsong=''
    slider.config(value=0)
    pause.grid_forget()
    Play.grid(row=0,column=0)
    py.mixer.music.stop()
    for item in tree.selection():
        tree.selection_remove(item)
    footer.config(text='')
    songcount=0
    starttime.config(text="00:00:00")
    stopped=True


#pause and unpause the song
def pausesong():
    global pau
    global stopped
    if stopped==False:
        if pau==False:
            py.mixer.music.pause()
            pau=True
            pause.grid_forget()
            Play.grid(row=0,column=0)






#forward the songs
def forwardsong():
    if tree.focus()==str(len(tree.get_children())-1):
        pass
    else:
        global currentsong
        slider.config(value=0)
        selected = tree.focus()
        selected = str(int(selected) + 1)
        values = tree.item(selected, 'values')
        song = values[1]
        currentsong = song
        py.mixer.music.load(song)
        py.mixer.music.play(loops=0)
        tree.focus(item=selected)
        tree.selection_set(selected)

#backward the songs
def backwardsong():
    if tree.focus()=='0':
        pass
    else:
        global currentsong
        slider.config(value=0)
        selected = tree.focus()
        selected = str(int(selected) - 1)
        values = tree.item(selected, 'values')
        song = values[1]
        currentsong = song
        py.mixer.music.load(song)
        py.mixer.music.play(loops=0)
        tree.focus(item=selected)
        tree.selection_set(selected)


#delete songs
def deletesongs():
    for items in tree.get_children():
        tree.delete(items)
    stopsong()

def deleteselected():
    x=tree.selection()
    for treeitems in x:
        tree.delete(treeitems)

# define timing in footer
def songtime():
    if stopped:
        return
    global currentsong
    global songcount
    global shuffleb
    global repeatb
    songcount=1
    current_time=int(py.mixer.music.get_pos()/1000)

    converted=time.strftime('%H:%M:%S',time.gmtime(current_time))

    songmut=MP3(currentsong)
    slength=songmut.info.length

    convertedslength = time.strftime('%H:%M:%S', time.gmtime(slength))

    if int(slider.get()) == int(slength):
        converted = time.strftime('%H:%M:%S', time.gmtime(int(slider.get())))
        footer.config(text=f"Time Elaspsed:- {converted} of {convertedslength} in {int(Volume_slider.get()*100)} Volume")
        starttime.config(text=f"{converted}")
        endtime.config(text=f"{convertedslength}")
    if pau or stopped:
        pass
    elif int(slider.get()) == int(current_time):
        current_time+=1
        slider.config(to=int(slength), value=int(current_time))
        footer.config(text=f"Time Elaspsed:- {converted} of {convertedslength} in {int(Volume_slider.get()*100)} Volume")
        starttime.config(text=f"{converted}")
        endtime.config(text=f"{convertedslength}")
        # print("slider not moved")
    else:
        slider.config(to=int(slength), value=int(slider.get()))
        converted = time.strftime('%H:%M:%S', time.gmtime(int(slider.get())))
        footer.config(text=f"Time Elaspsed:- {converted} of {convertedslength} in {int(Volume_slider.get()*100)} Volume")
        starttime.config(text=f"{converted}")
        endtime.config(text=f"{convertedslength}")
        newone=int(slider.get())+1
        slider.config(value=newone)
        # print("slider moved")
    if  converted==convertedslength:
        if shuffleb==False and repeatb==False:
            forwardsong()
        elif repeatb==True:
            slider.config(value=0)
            song=currentsong
            py.mixer.music.load(song)
            py.mixer.music.play(loops=0)
        elif shuffleb==True:
             slider.config(value=0)
             num=random.randint(0, (len(tree.get_children())-1))
             values = tree.item(num, 'values')
             song = values[1]
             currentsong = song
             py.mixer.music.load(song)
             py.mixer.music.play(loops=0)
             tree.focus(item=num)
             tree.selection_set(num)
    footer.after(1000,songtime)


#define songslider
def songslider(x):
    selected = tree.focus()
    values = tree.item(selected, 'values')
    song = values[1]
    py.mixer.music.load(song)
    py.mixer.music.play(loops=0,start=int(slider.get()))

def volslider(x):
    py.mixer.music.set_volume(Volume_slider.get())

def repeatsong():
    global repeatb
    if repeatb==False:
        repeat.config(borderwidth=0)
        repeatb=True
    else:
        repeat.config(borderwidth=2)
        repeatb=False

def sufflesong():
    global shuffleb
    if shuffleb==False:
        shuffle.config(borderwidth=0)
        shuffleb=True
    else:
        shuffle.config(borderwidth=2)
        shuffleb=False


#define the mainscreen
Mainscreen=Frame(root)
Mainscreen.pack()


tree_scroll=Scrollbar(Mainscreen)
tree_scroll.pack(side=RIGHT,fill=Y)

#playlist on the main screen
tree=ttk.Treeview(Mainscreen,height=14,yscrollcommand=tree_scroll.set)

tree_scroll.config(command=tree.yview)


tree['columns']=('Name','Address')
tree.column("#0", width=0,stretch=NO)
tree.column("Name",anchor=W,width=400,minwidth=400)
tree.column("Address",anchor=E,width=280,minwidth=280)

tree.heading('#0',text="",anchor=W)
tree.heading("Name",text="Name",anchor=CENTER)
tree.heading("Address",anchor=CENTER,text="Address")
tree.pack()

#slider to slide the song
sliderouter=Frame(root)
sliderouter.pack(pady=15)
starttime=Label(sliderouter,text="00:00:00")
starttime.grid(row=0,column=0)
sliderframe = LabelFrame(sliderouter)
sliderframe.grid(row=0,column=1)
slider=ttk.Scale(sliderframe,from_=0,to=100,orient=HORIZONTAL,value=0,command=songslider,length=600)
slider.pack(ipady=6)
endtime=Label(sliderouter,text="00:00:00")
endtime.grid(row=0,column=2)

#buttons and volume frame
BVframe=Frame(root)
BVframe.pack()

#buttons needed
playimage=PhotoImage(file='Images/play-button.png')
Play=Button(BVframe,image=playimage,borderwidth=0,command=playsong)
Play.grid(row=0,column=0)
pauseimage=PhotoImage(file='Images/pause-button.png')
pause=Button(BVframe,image=pauseimage,command=pausesong,borderwidth=0)
# pause.grid(row=0,column=1)
stopimage=PhotoImage(file='Images/stop.png')
stop=Button(BVframe,image=stopimage,borderwidth=0,command=stopsong)
stop.grid(row=0,column=1)
backimage=PhotoImage(file='Images/back.png')
backward=Button(BVframe,image=backimage,borderwidth=0,command=backwardsong)
backward.grid(row=0,column=2)
forwardimage=PhotoImage(file='Images/forwards.png')
forward=Button(BVframe,image=forwardimage,borderwidth=0,command=forwardsong)
forward.grid(row=0,column=3)
suffleimage=PhotoImage(file='Images/shuffle.png')
shuffle=Button(BVframe,image=suffleimage,borderwidth=2,width=40,height=40,command=sufflesong)
shuffle.grid(row=0,column=4)
repeatimage=PhotoImage(file='Images/repeat.png')
repeat=Button(BVframe,image=repeatimage,borderwidth=2,width=40,height=40,command=repeatsong)
repeat.grid(row=0,column=5)
#divider
Label(BVframe).grid(row=0,column=6,padx=105)




#Volumne Controller

volumelbframe=LabelFrame(BVframe)
volumelbframe.grid(row=0,column=7)
Volume_slider=ttk.Scale(volumelbframe,from_=0,to=1,orient=HORIZONTAL,value=0.99,command=volslider,length=120)
Volume_slider.pack(pady=3)


#defining music menu
music_menu=Menu(root)
root.config(menu=music_menu)
addsongmenu=Menu(music_menu ,tearoff=0)
music_menu.add_cascade(label="Playlist",menu=addsongmenu)
addsongmenu.add_command(label="Add Songs",command=addsong)
addsongmenu.add_command(label="Remove All Songs",command=deletesongs)
#footer to Show Timer
footer= Label(root,text='',bd=1,relief=GROOVE,anchor=E)
footer.pack(fill=X,side=BOTTOM)



root.mainloop()
