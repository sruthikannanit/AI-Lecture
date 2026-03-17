import speech_recognition as sr

def listen_voice():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        audio = r.listen(src)

    try:
        return r.recognize_google(audio)
    except:
        return "Voice error"