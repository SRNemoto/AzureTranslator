import azure.cognitiveservices.speech.translation as translatesdk

filename = "api_key.txt"
api_file = open(filename, "r")
api_key = api_file.readlines()

# Creates an instance of a translation config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
trans_key, service_region = api_key[0].rstrip(), api_key[1].rstrip()
trans_config = translatesdk.SpeechTranslationConfig(subscription=trans_key, region=service_region, speech_recognition_language="en-US")

# Creates a speech synthesizer using the default speaker as audio output.
trans_rec = translatesdk.TranslationRecognizer(translation_config=trans_config)
trans_rec.add_target_language("es-MX")
trans_rec.add_target_language("zh-CN")
trans_rec.add_target_language("en-US")

print("Say something?")
result = trans_rec.recognize_once()

out_file = open("output.txt", "w", encoding="utf-8")
for tr in result.translations:
    out_file.write(result.translations[tr] + "\n")
# print(result)

# Checks result.
# if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#     print("Speech synthesized to speaker for text [{}]".format(text))
# elif result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = result.cancellation_details
#     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         if cancellation_details.error_details:
#             print("Error details: {}".format(cancellation_details.error_details))
#     print("Did you update the subscription info?")