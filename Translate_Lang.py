from tkinter import DISABLED , INSERT , Toplevel , ttk , scrolledtext
from tkinter import filedialog as fd
import speech_recognition as sp
from gtts import gTTS
import tkinter as tk
import googletrans
import os

lang = []
recog = sp.Recognizer()
mic = sp.Microphone()

for language in list(googletrans.LANGUAGES.values()):
    lang.append(language.capitalize())

def get_val(from_ , to):
    global f_key , t_key
    lower_f = from_.lower()
    lower_t = to.lower()
    for key , val in googletrans.LANGUAGES.items():
        if val == lower_f:
            f_key = key
        elif val == lower_t:
            t_key = key
        else:
            continue

def translate():
    global root

    global f_key , t_key , translated_text
    from_lang = combo.get()
    to_lang = combo_from.get()
    get_val(from_lang , to_lang)

    try:
        trans = googletrans.Translator()
        textbox_text = textbox.get("1.0" , tk.END)
        text_translate = trans.translate(textbox_text , src = f_key , dest = t_key)
        translated_text = text_translate.text
        show_text()
    except NameError:
        label_err = ttk.Label(root , text = "Error ! Try Again")
        label_err.grid(row = 3 , column = 0 , pady = 15 , padx = 15 , sticky = 'E')
        root.after(2000 , label_err.destroy)
    except IndexError:
        label_err = ttk.Label(root , text = "Error ! Try Again")
        label_err.grid(row = 3 , column = 0 , pady = 15 , padx = 15 , sticky = 'E')
        root.after(2000 , label_err.destroy)

def show_text():
    global win
    win = Toplevel(root)
    frame = tk.Frame(win)
    win.title("Translated Text")

    label_trans = ttk.Label(win , text = "Translated Text : ")
    label_trans.grid(row = 0 , column = 0 , pady = 15 , padx = 20 , sticky = "E")
    label_win = scrolledtext.ScrolledText(win , width = 30 , height = 6 , wrap = "word" , font = ("Segoe UI" , 10))
    label_win.insert(INSERT , translated_text)
    label_win.update()
    label_win.config(state = DISABLED)
    label_win.grid(row = 0 , column = 1 , pady = 15 , padx = 20)

    button = ttk.Button(win , text = "Text-To-Speech" , command = lambda: play())
    button.grid(row = 1 , column = 1 , pady = 15 , padx = 20 , sticky = 'W')
    win.protocol("WM_DELETE_WINDOW" , stop)

    save = ttk.Button(win , text = "Save Audio" , command = save_audio)
    save.grid(row = 1 , column = 1 , pady = 15 , padx = 34 , sticky = 'E')

def play():
    global speak
    speak = gTTS(text = translated_text , lang = t_key , slow = False)
    speak.save("Translated.mp3")
    os.system("start Translated.mp3")

def stop():
    win.destroy()
    if os.path.exists("Translated.mp3"):
        os.remove("Translated.mp3")

def speech_to_text():
    try:
        with mic as source:
            recog.adjust_for_ambient_noise(source , duration = 1)
            sound = recog.listen(source)
            text_speech = recog.recognize_vosk(sound)
            textbox.insert(INSERT , text_speech[14:-3])
            textbox.update()
    except sp.RequestError:
        label_er = ttk.Label(root , text = "Error !")
        label_er.grid(row = 3 , column = 0 , pady = 15 , padx = 20)
        root.after(2000 , label_er.destroy)
    except sp.UnknownValueError:
        label_er = ttk.Label(root , text = "Error !")
        label_er.grid(row = 3 , column = 0 , pady = 15 , padx = 20)
        root.after(2000 , label_er.destroy)

def save_audio():
    try:
        filetype = (('Audio Files (.mp3)' , '*.mp3') , )
        audio = gTTS(text = translated_text , lang = t_key , slow = False)
        files_save = fd.asksaveasfilename(title = "Save File As" , filetypes = filetype)
        if files_save:
            files_save += ".mp3"
            audio.save(files_save)
            label_save = ttk.Label(win , text = "File Saved")
            label_save.grid(row = 1 , column = 0 , pady = 15 , padx = 20 , sticky = 'E')
            win.after(4000 , label_save.destroy)
        else:
            label_error1 = ttk.Label(win , text = "File Not Saved")
            label_error1.grid(row = 1 , column = 0 , pady = 15 , padx = 20 , sticky = 'E')
            win.after(4000 , label_error1.destroy)
    except NameError:
        label_error = ttk.Label(win , text = "File Not Saved")
        label_error.grid(row = 1 , column = 0 , pady = 15 , padx = 20 , sticky = 'E')
        win.after(4000 , label_error.destroy)

    
root = tk.Tk()
fr = tk.Frame(root)
global combo , combo_from , textbox
root.title("Text-To-Speech Translator")
photo = tk.PhotoImage(file = "")    # Path of the icon file
root.iconphoto(True , photo)

lab = ttk.Label(root , text = "Translate From : ")
lab.grid(row = 0 , column = 0 , pady = 15 , padx = 20 , sticky = 'E')

combo = ttk.Combobox(root , width = 32 , state = "readonly")
combo["values"] = lang
combo.current(0)
combo.bind("<<ComboboxSelected>>" , lambda p : root.focus())
combo.grid(row = 0 , column = 1 , pady = 15 , padx = 20 , sticky = 'W')

label = ttk.Label(root , text = "Translate To : ")
label.grid(row = 1 , column = 0 , pady = 15 , padx = 20 , sticky = 'E')

combo_from = ttk.Combobox(root , width = 32 , state = "readonly")
combo_from["values"] = lang
combo_from.current(0)
combo_from.bind("<<ComboboxSelected>>" , lambda p : root.focus())
combo_from.grid(row = 1 , column = 1 , pady = 15 , padx = 20 , sticky = 'W')

label_text = ttk.Label(root , text = "Enter Text : ")
label_text.grid(row = 2 , column = 0 , pady = 15 , padx = 20 , sticky = "E")
textbox = scrolledtext.ScrolledText(root , width = 30 , height = 6 , font = ("Segoe UI" , 10) , wrap = "word")
textbox.grid(row = 2 , column = 1 , pady = 15 , padx = 20)

but = ttk.Button(text = "Translate Text" , command = translate)
but.grid(row = 3 , column = 1 , pady = 15 , padx = 20 , sticky = 'W')

button_conv = ttk.Button(text = "Speech-To-Text" , command = speech_to_text)
button_conv.grid(row = 3 , column = 1 , pady = 15 , padx = 35 , sticky = 'E')


root.mainloop()