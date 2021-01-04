from google.cloud import speech

client = speech.SpeechClient()

storage_uri = 'C:\\Users\\Asiek\\Documents\\Audacity\\test.wav'
audio = speech.RecognitionAudio(uri=storage_uri)
speech_context = speech.SpeechContext(phrases={"$DAY": "Monday"})

GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/my-key.json"


config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    speech_contexts=[speech_context],
)

response = client.recognize(config=config, audio=audio)

print(response)

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print("-" * 20)
    print("First alternative of result {}".format(i))
    print("Transcript: {}".format(alternative.transcript))