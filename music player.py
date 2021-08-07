#importing important libraries for my project
import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

#using oops
class Player(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.pack()

        mixer.init()
        if os.path.exists("songs.pkl"):
            with open("songs.pkl","rb") as f:
                self.playlist= pickle.load(f)
        else:
            self.playlist=[]

        self.current=0
        self.paused=True
        self.played=False

        self.create_frames()
        self.track_widget()
        self.control_widget()
        self.tracklist_widgets()

    def create_frames(self):
        #frame 1
        self.track=tk.LabelFrame(self,text="Song Track",
        font=("times new roman",15,"bold"),
        bg="grey",fg="white",bd=5,relief=tk.GROOVE)
        self.track.configure(width=410,height=300)
        self.track.grid(row=0,column=0,padx=10)

        # frame 2
        self.tracklist = tk.LabelFrame(self, text=f"playlist - {len(self.playlist)}",
                                   font=("times new roman", 15, "bold"),
                                   bg="grey", fg="white", bd=5, relief=tk.GROOVE)
        self.tracklist.configure(width=190, height=400)
        self.tracklist.grid(row=0, column=1,rowspan=3,pady=5)

        # frame 3
        self.controls = tk.LabelFrame(self,
                                   font=("times new roman", 15, "bold"),
                                   bg="white", fg="white", bd=2, relief=tk.GROOVE)
        self.controls.configure(width=410, height=80)
        self.controls.grid(row=2, column=0,pady=5,padx=10)

# picture window
    def track_widget(self):
        self.canvas = tk.Label(self.track,image=img)
        self.canvas.configure(width=400,height=240)
        self.canvas.grid(row=0,column=0)

        self.songtrack = tk.Label(self.track, font=("times new roman", 15, "bold"),bg="white",fg="dark blue")
        self.songtrack["text"]="load something to play!!"
        self.songtrack.configure(width=30, height=1)
        self.songtrack.grid(row=1, column=0)

# control window
    def control_widget(self):
        self.loadSongs=tk.Button(self.controls , bg="green",fg="white",font=10)
        self.loadSongs["text"]="load songs"
        self.loadSongs["command"]=self.retrieve_songs #only binding the function not calling
        self.loadSongs.grid(row=0,column=0,padx=10)

        self.prev = tk.Button(self.controls, image=prev)
        self.prev["text"] = "load songs"
        self.prev["command"] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = tk.Button(self.controls, image=pause)
        self.pause["text"] = "load songs"
        self.pause["command"] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next= tk.Button(self.controls, image=next_)
        self.next["text"] = "load songs"
        self.next["command"] = self.next_song
        self.next.grid(row=0, column=3)

        self.volume=tk.DoubleVar()
        self.slider=tk.Scale(self.controls, from_ =0,to=10,orient=tk.HORIZONTAL)
        self.slider["variable"]=self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider["command"] = self.change_volume
        self.slider.grid(row=0,column=4,padx=5)


    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist,orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1,rowspan=5,sticky="ns")  # ns means north south
        self.list =tk.Listbox(self.tracklist,selectmode=tk.SINGLE,
                              yscrollcommand=self.scrollbar.set,selectbackground="sky blue")
        self.enumerate_songs()
        self.scrollbar.config(command=self)
        self.list.config(height=22)
        self.list.bind('<Double-1>',self.play_song)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)






# creating some  more functions for buttons
    def enumerate_songs(self):
        for index,song in enumerate(self.playlist):
            self.list.insert(index,os.path.basename(song))
    def retrieve_songs(self):
        self.songlist=[]
        directory= filedialog.askdirectory()
        for root_,dirs,files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1]==".mp3":
                    path=(root_+"/"+file).replace("\\","/")
                    self.songlist.append(path)

        with open("songs.pkl", "wb") as f:
            pickle.dump(self.songlist, f)

        self.playlist=self.songlist
        self.tracklist["text"]=f"playlist - {len(self.playlist)}"
        self.list.delete(0,tk.END)
        self.enumerate_songs()

    def play_song(self,event=None):
        if event is not None:
            self.current=self.list.curselection()[0]
            for i in range (len(self.playlist)):
                self.list.itemconfigure(i,bg="white")

        mixer.music.load(self.playlist[self.current])

        self.pause['image']= play  # change picture to play
        self.paused=False
        self.played=True

        self.songtrack['anchor']='w'  # west
        self.songtrack["text"]=os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current,bg="sky blue")
        mixer.music.play()



    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play


    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='white')
        self.play_song()

    def change_volume(self,event=None):
        self.v=self.volume.get()
        mixer.music.set_volume(self.v / 10)


root=tk.Tk()
root.geometry('600x400')
root.wm_title("my music player")
# root.mainloop()

img = PhotoImage(file='pictures/pic.gif')
next_ = PhotoImage(file = 'pictures/next.gif')
prev = PhotoImage(file='pictures/previous.gif')
play = PhotoImage(file='pictures/play.gif')
pause = PhotoImage(file='pictures/pause.gif')

app=Player(master=root)
app.mainloop()