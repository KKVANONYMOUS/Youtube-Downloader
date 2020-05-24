from pytube import YouTube
from tkinter.filedialog import *
from tkinter import *
from tkinter.messagebox import *
from threading import *

#total file size container
file_size=0

#function for updating percentage while downloading
def progress(stream,chunk,file_handle,remaining=None):
    #fetching percentage of file that has been downloaded
    file_downloaded=(file_size-file_handle)
    percent=(file_downloaded/file_size) * 100
    btn.config(text="{:00.0f} % downloaded".format(percent))

def startDownload():
    global file_size
    try:
        #storing url given by user
        url=urlField.get()

        #changing button text
        btn.config(text="Please wait...")

        #disabling button
        btn.config(state=DISABLED)

        #opens dialog box to ask for saving location
        path=askdirectory()

        if path is None:
            return

        ob=YouTube(url,on_progress_callback=progress)
        strm=ob.streams.get_highest_resolution()

        #setting video size
        file_size=strm.filesize

        #setting video title and description
        vTitle.config(text=strm.title)
        vTitle.pack(side=TOP,pady=10)
        vDesc.config(text=ob.description)
        vDesc.pack(side=TOP,pady=10)
        #command to start download
        strm.download(path)
        #setting button back to normal
        btn.config(text="Start Download")
        btn.config(state=NORMAL)

        showinfo("Download Finished","Downloaded successfully")
        urlField.delete(0,END)
        
        #hiding video title
        vTitle.pack_forget()
    except Exception as e:
        print(e)
        showinfo("Error","Some error occurred...")
        btn.config(text="Start Download")
        btn.config(state=NORMAL)
        urlField.delete(0,END)
         

#function to start download thread
def startDownloadThread():
    #create thread
    thread=Thread(target=startDownload)
    thread.start()

#Building gui using tkinter
main=Tk()

#setting title
main.title("Youtube Downloader")

#setting icon
main.iconbitmap("youtube.ico")

main.geometry("500x600")

#heading icon
file=PhotoImage(file='youtube.png')
headingIcon=Label(main,image=file)
headingIcon.pack(side=TOP)

#url textfield
urlField=Entry(main,font=("verdana",18),justify=CENTER)
urlField.pack(side=TOP,fill=X,padx=10)

#download button
btn=Button(main,text="start download",font=("verdana",18),relief='ridge',command=startDownloadThread)
btn.pack(side=TOP,pady=10)

#video title
vTitle=Label(main,text="Video title",font=("verdana",13))

#video description
vDesc=Label(main,text="Video Description")
main.mainloop()