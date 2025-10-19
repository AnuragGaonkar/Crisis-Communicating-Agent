from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

def detect_language(text):
    try:
        language_code = detect(text)
        return language_code
    except:
        return "unknown"
