from tkinter import *
from PIL import Image, ImageTk
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from googletrans import Translator
import os
from gtts import gTTS
import pygame
import speech_recognition
import threading



translator = Translator()

bot = ChatBot('Bot')
trainer = ListTrainer(bot)

for files in os.listdir('Data/bengali/'):
    data = open('Data/bengali/' + files, 'r', encoding='utf-8').readlines()
    trainer.train(data)

def translate_to_bengali(text):
    translation = translator.translate(text, src='en', dest='bn')
    return translation.text

def speak_bengali(text):
    tts = gTTS(text=text, lang='bn')
    tts.save('temp.mp3')
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

def botrep():
    ques = quesfie.get()
    ques = ques.capitalize()

    translated_ques = translate_to_bengali(ques)

    ans = bot.get_response(translated_ques)
    translated_ans = translate_to_bengali(str(ans))

    textar.insert(END, 'You: ' + ques + '\n\n')
    textar.insert(END, 'BOT: ' + translated_ans + '\n\n')
    speak_bengali(translated_ans)
    quesfie.delete(0, END)

def audiotext():
    while True:
        sr = speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone() as m:
                sr.adjust_for_ambient_noise(m, duration=0.2)
                audio = sr.listen(m)
                query = sr.recognize_google(audio)

                translated_query = translate_to_bengali(query)

                quesfie.delete(0, END)
                quesfie.insert(0, translated_query)
                botrep()
        except Exception as e:
            print(e)

root = Tk()
root.geometry('500x570+100+30')
root.title('Chatbot in English')
root.config(bg='lightcoral')

logopic = Image.open('Talingbot.png')
logopic = logopic.resize((120, 120), Image.Resampling.LANCZOS)
logopic2 = ImageTk.PhotoImage(logopic)
logopicleb = Label(root, image=logopic2, bg='lightcoral')
logopicleb.pack()

center = Frame(root)
center.pack()

scr = Scrollbar(center)
scr.pack(side=RIGHT)

textar = Text(center, font=('TimesNew Roman', 20, 'bold'), height=10, yscrollcommand=scr.set, wrap='word')
textar.pack(side=LEFT)

scr.config(command=textar.yview)

quesfie = Entry(root, font=('verdana', 20, 'bold'))
quesfie.pack(pady=15, fill=X)

asp = Image.open('ask.png')
asp = asp.resize((45, 45), Image.Resampling.LANCZOS)
asp2 = ImageTk.PhotoImage(asp)
askb = Button(root, image=asp2, command=botrep)
askb.pack()


def click(event):
    askb.invoke()

root.bind('<Return>', click)

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

thread = threading.Thread(target=audiotext)
thread.setDaemon(True)
thread.start()

root.mainloop()

