#Import the required libraries
from tkinter import *
from PIL import Image,ImageTk
from mutagen import File
from mutagen.mp3 import MP3
import time 
from tkinter import ttk
import io
import pymongo
from pygame import mixer  
import pygame
import gridfs
client=pymongo.MongoClient("mongodb://localhost:27017")

db=client["musicfiles"]
collection=db['fs.files']
#------------------------------image retreive
ukj=0

win= Tk()

#Set the geometry of frame
win.geometry("350x600")
win.configure(bg='cadetblue')


#Get the current screen width and height
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

win.resizable(False,False)
images=[]
images2=[]
a=1
paused =False
stopped =False
x=0


mixer.init()


imgpause= (Image.open("D:\\heroalom ka ghr\\play-button.png"))
resizepause= imgpause.resize((60,50), Image.ANTIALIAS)
newpause= ImageTk.PhotoImage(resizepause)
images2.append(newpause)



#-------------------------------play--pause image change function--------------
def playi():
    global paused
    
    if paused==True:
        btnplay.config(image=newpause)
        pygame.mixer.music.pause()
        paused = False
        
    elif paused==False:
        btnplay.config(image=new_imaged)
        pygame.mixer.music.unpause()
        paused = True
        







#---------------------------newpl-------------

def player(out):
    global stopped,x
    play_time()
    mixer.music.load(io.BytesIO(out))   
    mixer.music.play(loops=0)
    stopped=False
    x=1
    

    
    
    
#####-------------------------------------play_time-------------------


def play_time():
# Check for double timing
    if stopped:
        return


# Grab Current Song Elapsed Time
    current_time = pygame.mixer.music.get_pos() / 1000

# convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))



# Load Song with Mutagen
    song_mut = MP3(io.BytesIO(out))
# Get song Length
    global song_length
    song_length = song_mut.info.length
# Convert to Time Format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    status2.config(text=f'{converted_song_length}  ')


# Increase current time by 1 second
    current_time = current_time + 1 
	
    if int(my_slider.get()) == int(song_length):
        print("hero")
        next()
        status2.config(text=f'{converted_song_length}  ')

    elif paused ==False:
       print("kl")

    elif int(my_slider.get()) == int(current_time):
# Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
        print("alom")
    else:
#Update Slider To position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
		
#convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

#Output time to status bar
        status.config(text=f'{converted_current_time}')

#Move this thing along by one second
        next_time = int(my_slider.get())+1
        my_slider.config(value=next_time)
        print("kha")
    status.after(1000, play_time)

#--------------------------------------previous track-----------------
def previous():
    global ukj,a,paused,out,stopped,x
    if x==0:
        stopped=False
    else:
        stopped=True
    status.config(text="")
    my_slider.config(value=0)
    ukj=ukj-1
    if(ukj>-1):  
     fs=gridfs.GridFS(db)
     out=fs.get(ukj).read()
     file = File(io.BytesIO(out))
     artwork = file.tags['APIC:FRONT_COVER'].data
     songlabelname= file.tags["TIT2"]
     songlabel.config(text=songlabelname)
     midimage(artwork)
     player(out) 
    
    else:
        lk=collection.find({"_id":{"$gt":2}},{'file':0, 'name':0})
        for j in lk:
          k=j
        lk2=k['_id']
        ukj=lk2
        fs=gridfs.GridFS(db)
        out=fs.get(ukj).read()
        file = File(io.BytesIO(out))
        artwork = file.tags['APIC:FRONT_COVER'].data
        songlabelname= file.tags["TIT2"]
        songlabel.config(text=songlabelname)
        midimage(artwork)
        player(out)
    btnplay.config(image=new_imaged)
    a=2
    paused=True

def sl(x):
    #s.config(text=int(my_slider.get()))
    mixer.music.load(io.BytesIO(out))   
    mixer.music.play(loops=0,start=int(my_slider.get()))
     
    
    
    
 
#--------------------------------------next button---------------
def next():
    global ukj,a,paused,out,stopped,x
    if x==0:
        stopped=False
    else:
        stopped=True
    status.config(text="")
    my_slider.config(value=0)
    ukj=ukj+1
    lk=collection.find({"_id":{"$gt":2}},{'file':0, 'name':0})
    for j in lk:
       k=j
    lk2=k['_id']
    if ( ukj<lk2+1):
       fs=gridfs.GridFS(db)
       out=fs.get(ukj).read()
       file = File(io.BytesIO(out))
       artwork = file.tags['APIC:FRONT_COVER'].data
       songlabelname= file.tags["TIT2"]
       songlabel.config(text=songlabelname)

       
       midimage(artwork)
       player(out)

    else:
       ukj=0
       fs=gridfs.GridFS(db)
       out=fs.get(ukj).read()
       file = File(io.BytesIO(out))
       artwork = file.tags['APIC:FRONT_COVER'].data
       songlabelname = file.tags['TALB']
       songlabel.config(text=songlabelname)
       midimage(artwork)
       player(out)
    

    btnplay.config(image=new_imaged)
    a=2
    paused=True
    



#-----------------------middle image------------------
def midimage(by):
    image1 = io.BytesIO(by)
    frame = Frame(win, width=300, height=300)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    jkl=Image.open(image1)
    resizemid=jkl.resize((300,300), Image.ANTIALIAS)
    newmid= ImageTk.PhotoImage(resizemid)
    label = Label(frame,border=0, image = newmid)
    label.pack()
    images.append(newmid)


    
    


def pr():
    global a
    if a==1:
       
       fs=gridfs.GridFS(db)
       out=fs.get(0).read()
       player(out)
       

       pr.__code__  = (lambda:None).__code__
    else:
              pr.__code__  = (lambda:None).__code__






fs=gridfs.GridFS(db)
out=fs.get(0).read()
file = File(io.BytesIO(out))
songlabelname = file.tags['TALB']
songlabel.config(text=songlabelname)
by = file.tags['APIC:FRONT_COVER'].data
imgd= (Image.open("D:\\heroalom ka ghr\\pause.png"))
resized_imaged= imgd.resize((60,50), Image.ANTIALIAS)
new_imaged= ImageTk.PhotoImage(resized_imaged)
midimage(by)

#--------------------------------song ----------------------function-----------------------------
def song():
   global listboc
   listboc= Listbox(win)
   he=db.fs.files.find({})
   for c in he:
      k=c['filename']
      listboc.insert(END,f"{k}")
   listboc.place(x=20,y=20)

#-------------chkma-----------------



     

#-------------------------------------button play  -------------------------------------------------
img= (Image.open("D:\\heroalom ka ghr\\play-button.png"))
resized_image= img.resize((60,50), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)
btnplay=Button(width=60,pady=5,image=new_image,bg='cadetblue',activebackground='cadetblue', border=0,command=lambda:[pr(),playi()])
btnplay.place(x=135,y=500)

#-------------------------------------button next  -------------------------------------------------
img2= (Image.open("D:\\heroalom ka ghr\\next-button.png"))
resized_image2= img2.resize((60,50), Image.ANTIALIAS)
new_image2= ImageTk.PhotoImage(resized_image2)
btnnext=Button(width=60,pady=5,  image=new_image2,bg='cadetblue',activebackground='cadetblue', border=0,command=lambda:[next()])
btnnext.place(x=230,y=500)

#-------------------------------------button previous  -----------------------------------------------
img3= (Image.open("D:\\heroalom ka ghr\\previous.png"))
resized_image3= img3.resize((60,50), Image.ANTIALIAS)
new_image3= ImageTk.PhotoImage(resized_image3)
btnprevious=Button(width=60,pady=5,  image=new_image3,bg='cadetblue',activebackground='cadetblue', border=0,command=lambda:[previous()]).place(x=43,y=500)

#-------------------song button----------------------------------------------------------------------
btnsong=Button(width=60,pady=5,activebackground='cadetblue', border=0,command=song).place(x=43,y=100)









#-------------------- ctime-------------
status = Label(win, text='00:00',bg='cadetblue')
status.place(x=20,y=450)

#----------length-----------------------
status2 = Label(win, text='00:00',bg='cadetblue')
status2.place(x=300,y=450)






#---------------------slider---------------------

style = ttk.Style()
style.configure("TScale", background="cadetblue")
my_slider=ttk.Scale(win, from_=0,to=100,orient=HORIZONTAL,length=310,value=0,command=sl)
my_slider.place(x=20,y=470)


win.mainloop()