import azure.cognitiveservices.speech as SpeechSDK
import azure.cognitiveservices.speech.translation as TransSDK
import os, requests, uuid, json, asyncio
import time

# filename = "api_key.txt"
# api_file = open(filename, "r")
# api_file_lines = api_file.readlines()

# api_key, service_region = api_file_lines[0].rstrip(), api_file_lines[1].rstrip()

class SpchTxtHandler:
    """ Module for handling transformations between speech and text as well as translations """

    def __init__(self, api_key, service_region):
        """ Initializes this module with an api key and region"""
        self._key = api_key
        self._region = service_region
    
    async def Speech2TxtTrans(self, input_lang="en-US", target_langs=["en-US"]):
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

        done = False
        out_str = ""

        def stop_cb(evt):
            """callback that stops continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            trans_recog.stop_continuous_recognition()
            nonlocal done
            done = True
            
        def update_str(evt):
            # print('RECOGNIZING[yeet]: {}'.format(evt))
            nonlocal out_str
            out_str = evt
            # print('parsed_str {}'.format(evt))
            # out_str = evt.translations['en']
            

        # Connect callbacks to the events fired by the speech recognizer
        trans_recog.recognizing.connect(update_str)
        # trans_recog.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        trans_recog.recognized.connect(update_str)

        # trans_recog.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        # trans_recog.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        # trans_recog.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # # stop continuous recognition on either session stopped or canceled events
        trans_recog.session_stopped.connect(stop_cb)
        trans_recog.canceled.connect(stop_cb)

        trans_recog.start_continuous_recognition()
        time.sleep(3)
        trans_recog.stop_continuous_recognition()

        # print(dir(out_str.result.translations))

        return out_str.result.translations

        # result = trans_recog.recognize_once_async()
        # result = dir(result.get().translations)
        # result = result.get().translations
        # print([method_name for method_name in dir(result) if callable(getattr(result, method_name))])

        # return result.get().translations
        # return result
        

    def Txt2Spch(self, input_txt, input_lang):
        """ Converts inputted text to speech for given language """
        speech_config = SpeechSDK.SpeechConfig(
            subscription=self._key,
            region=self._region,
            speech_recognition_language=input_lang
        )

        speech_synthesizer = SpeechSDK.SpeechSynthesizer(speech_config=speech_config)

        speech_synthesizer.speak_text_async(input_txt).get()

    def TransTxt(self, input_txt, target_lang):
        base_url = 'https://api.cognitive.microsofttranslator.com'
        path = '/translate?api-version=3.0'
        params = '&to=' + target_lang
        constructed_url = base_url + path + params

        headers = {
            'Ocp-Apim-Subscription-Key': self._key,
            'Ocp-Apim-Subscription-Region': self._region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text' : input_txt
        }]
        response = requests.post(constructed_url, headers=headers, json=body)
        return response.json()[0]['translations'][0]['text']


async def main():
    filename = "api_key.txt"
    api_file = open(filename, "r")
    api_key = api_file.readlines()

    hand = SpchTxtHandler(api_key[0].rstrip(), api_key[1].rstrip())
    # print(hand.TransTxt("再试一次，包括他的ETF援助给我的东西，不是胡言乱语。", "en-US"))
    translation = await hand.Speech2TxtTrans()

    # translation = translation.get()
    # print([method_name for method_name in dir(translation) if callable(getattr(translation, method_name))])
    # print(translation['en'])
    print(translation['en'])

if __name__ == "__main__":
    asyncio.run(main())