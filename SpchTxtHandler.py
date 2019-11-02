import azure.cognitiveservices.speech as SpeechSDK
import azure.cognitiveservices.speech.translation as TransSDK

# filename = "api_key.txt"
# api_file = open(filename, "r")
# api_file_lines = api_file.readlines()

# api_key, service_region = api_file_lines[0].rstrip(), api_file_lines[1].rstrip()

class SpchTxtHandler():
    """ Module for handling transformations between speech and text as well as translations """

    def __init__(self, api_key, service_region):
        """ Initializes this module with an api key and region"""
        self._key = api_key
        self._region = service_region
    
    def Speech2TxtTrans(self, input_lang="en-US", target_langs=["en-US"]):
        """ Creates a Translation Recognizer to translate input speech to desired languages """
        trans_config = TransSDK.SpeechTranslationConfig(
            subscription=self._key,
            region=self._region,
            speech_recognition_language=input_lang
        )

        trans_recog = TransSDK.TranslationRecognizer(
            translation_config=trans_config
        )
        
        for lang in target_langs:
            trans_recog.add_target_language(lang)

        result = trans_recog.recognize_once()

        return result.translations

    def Txt2Spch(self, input_txt, input_lang):
        """ Converts inputted text to speech for given language """
        speech_config = SpeechSDK.SpeechConfig(
            subscription=self._key,
            region=self._region,
            speech_recognition_language=input_lang
        )

        speech_synthesizer = SpeechSDK.SpeechSynthesizer(speech_config=speech_config)

        speech_synthesizer.speak_text_async(input_txt).get()
