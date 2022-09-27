# Importing necessary modules required

from fnmatch import translate
from flask import Flask, redirect, render_template, request, flash
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import os


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


i = 0

languages = {"afrikaans": "af", "albanian": "sq", "amharic": "am", "arabic": "ar", "armenian": "hy", "azerbaijani": "az",
             "basque": "eu", "belarusian": "be", "bengali": "bn", "bosnian": "bs", "bulgarian": "bg",
             "catalan": "ca", "cebuano": "ceb", "chichewa": "ny", "chinese (simplified)": "zh-cn", "chinese (traditional)": "zh-tw",
             "corsican": "co", "croatian": "hr", "czech": "cs", "danish": "da", "dutch": "nl",
             "english": "en", "esperanto": "eo", "estonian": "et", "filipino": "tl", "finnish": "fi",
             "french": "fr", "frisian": "fy", "galician": "gl", "georgian": "ka", "german": "de",
             "greek": "el", "gujarati": "gu", "haitian creole": "ht", "hausa": "ha", "hawaiian": "haw",
             "hebrew": "he", "hindi": "hi", "hmong": "hmn", "hungarian": "hu", "icelandic": "is",
             "igbo": "ig", "indonesian": "id", "irish": "ga", "italian": "it", "japanese": "ja",
             "javanese": "jw", "kannada": "kn", "kazakh": "kk", "khmer": "km", "korean": "ko",
             "kurdish (kurmanji)": "ku", "kyrgyz": "ky", "lao": "lo", "latin": "la", "latvian": "lv",
             "lithuanian": "lt", "luxembourgish": "lb", "macedonian": "mk", "malagasy": "mg", "malay": "ms",
             "malayalam": "ml", "maltese": "mt", "maori": "mi", "marathi": "mr", "mongolian": "mn",
             "myanmar (burmese)": "my", "nepali": "ne", "norwegian": "no", "odia": "or", "pashto": "ps",
             "persian": "fa", "polish": "pl", "portuguese": "pt", "punjabi": "pa", "romanian": "ro",
             "russian": "ru", "samoan": "sm", "scots gaelic": "gd", "serbian": "sr", "sesotho": "st",
             "shona": "sn", "sindhi": "sd", "sinhala": "si", "slovak": "sk", "slovenian": "sl",
             "somali": "so", "spanish": "es", "sundanese": "su", "swahili": "sw", "swedish": "sv",
             "tajik": "tg", "tamil": "ta", "telugu": "te", "thai": "th", "turkish": "tr",
             "ukrainian": "uk", "urdu": "ur", "uyghur": "ug", "uzbek": "uz", "vietnamese": "vi",
             "welsh": "cy", "xhosa": "xh", "yiddish": "yi", "yoruba": "yo", "zulu": "zu"}

i = 0


@app.route('/translation', methods=['POST'])
def translate_text():
    '''
        Translate text from one language to another
        return: translated text to translator.html
    '''
    text = request.form.get('user_text')
    target = request.form.get('target_language')
    print(text, target)
    translated_text = translator(text, target)
    return render_template('translator.html', translated_text=translated_text)


@app.route('/translation2', methods=['POST', 'GET'])
def translate_speech():
    '''
        Translate speech from one language to another
        Process: Record audio -> Convert to text -> Translate text -> Convert to speech -> Play
        return: translated speech to translator2.html
    '''
    print("inside translation2")
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        extensions_available = ["wav"]
        if file.filename.split(".")[-1] not in extensions_available:
            print(file.filename.split(".")[-1])
            return render_template("error.html", message = "Please upload a file with .wav extension only\nTo do so, Just save the audio file with .wav extension")
        
    target = request.form.get('target_language')
    if target not in languages.keys():
        return render_template("error.html", message = "Choose a valid language. Look in the Supported Languages list for more information.")
    try:   
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            print(transcript)
    except:
        return render_template("error.html", message = "Sorry, I didn't understand that. Please try again.")

    translated_text = translator(transcript, target)
    
    

    target = languages[target].lower()
    try:
        speak = gTTS(text=translated_text, lang=target, slow=False)
    except:
        return render_template("error.html", message = "Sorry, I didn't understand that. Please try again.")
    #? Using save() method to save the translated
    global i
    i += 1
    
    #? speech in capture_voice.mp3
    speak.save(fr"static\translated_speech\captured_voice{i}.mp3")

    return render_template('translator2.html', translated_text=translated_text, path = fr"static\translated_speech\captured_voice{i}.mp3")


def translator(text, target):
    """Trasnlate text from one language to another

    Args:
        text (str): text to be translated
        target (str): target language

    Returns:
        str: translated text
    """
    if target not in languages.keys():
        return "Choose a valid language. Look in the Supported Languages list for more information"
    target = languages[target].lower()
    print(target)
    translator = Translator()
    translation = translator.translate(text, dest=target)
    print(translation.text)
    return translation.text


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
