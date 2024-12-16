from tkinter import *
from PIL import Image,ImageTk
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import pyttsx3
import speech_recognition
import threading

bot=ChatBot('Bot')
trainer=ListTrainer(bot)
for files in os.listdir('Data/english/'):

    data=open('Data/english/'+files,'r',encoding='utf-8').readlines()
    trainer.train(data)

def botrep():
    ques=quesfie.get()
    ques=ques.capitalize()
    ans=bot.get_response(ques)
    textar.insert(END,'You: '+ques+'\n\n')
    textar.insert(END,'BOT: '+str(ans)+'\n\n')
    pyttsx3.speak(ans)
    quesfie.delete(0,END)

def audiotext():
    while True:
        sr=speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone()as m:
                sr.adjust_for_ambient_noise(m,duration=0.2)
                audio=sr.listen(m)
                query=sr.recognize_google(audio)
                quesfie.delete(0,END)
                quesfie.insert(0,query)
                botrep()
        except Exception as e:
            print(e)

root=Tk()
root.geometry('500x570+100+30')
root.title('Chatbot in english')
root.config(bg='lightcoral')
logopic=Image.open('Talingbot.png')
logopic=logopic.resize((120,120),Image.Resampling.LANCZOS)
logopic2=ImageTk.PhotoImage(logopic)
logopicleb=Label(root,image=logopic2,bg='lightcoral')
logopicleb.pack()
center=Frame(root)
center.pack()
scr=Scrollbar(center)
scr.pack(side=RIGHT)
textar=Text(center,font=('TimesNew Roman',20,'bold'),height=10,yscrollcommand=scr.set,wrap='word')
textar.pack(side=LEFT)
scr.config(command=textar.yview)

quesfie=Entry(root,font=('verdana',20,'bold'))
quesfie.pack(pady=15,fill=X)
asp=Image.open('ask.png')
asp=asp.resize((45,45),Image.Resampling.LANCZOS)
asp2=ImageTk.PhotoImage(asp)
askb=Button(root,image=asp2,command=botrep)
askb.pack()


def click(event):
    askb.invoke()

root.bind('<Return>',click)
thread=threading.Thread(target=audiotext)
thread.setDaemon((True))
thread.start()

root.mainloop()
