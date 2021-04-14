from google.cloud import translate_v2 as translate
def DetectLang(text):
    new_client = translate.Client()

    result = new_client.detect_language(text)
    return result


text = "Hello world, Weather forecast for today is"
resultList = DetectLang(text)
print(resultList["language"], resultList["confidence"])