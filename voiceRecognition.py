import speech_recognition as sr
from langdetect import detect

# צליל אזהרה לפי מערכת הפעלה
try:
    import winsound
    def play_warning_sound():
        winsound.Beep(1000, 500)
except ImportError:
    import beepy
    def play_warning_sound():
        beepy.beep(sound='error')

def detect_language():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 מאזינה... דברי בבירור")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language="ar-IL")
            language = detect(text)

            print(f"📝 טקסט: {text}")
            print(f"🌍 שפה: {language}")

            if language == "ar":
                print("🚨 זוהתה שפה עוינת (ערבית)")
                play_warning_sound()
                return "hostile"
            else:
                print("✅ שפה תקינה")
                return "neutral"

        except sr.UnknownValueError:
            print("❌ לא זוהה דיבור")
            return "unknown"
        except sr.RequestError:
            print("❌ שגיאה בגישה לשירות זיהוי")
            return "unknown"
        except sr.WaitTimeoutError:
            print("⏰ לא התקבלה אמירה")
            return "unknown"
