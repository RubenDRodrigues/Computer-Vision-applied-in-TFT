import pyaudio
import wave
import speech_recognition as sr
from os import path
import numpy as np
import sounddevice as sd
import wave
import io
p = pyaudio.PyAudio()


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44000
CHUNK = 2048
RECORD_SECONDS = 4

print ( "Available devices:\n")
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print ( str(info["index"]) +  ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))
    pass

device_id = 5
device_info = p.get_device_info_by_index(device_id)
channels = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
# https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.__init__
stream = p.open(format=FORMAT,
                channels=channels,
                rate=int(device_info["defaultSampleRate"]),
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=device_info["index"],
                as_loopback=True
                )

print("Sample: " +str(p.get_sample_size(pyaudio.paInt16)))

r = sr.Recognizer()
frames = []

for _ in range(int((RATE / CHUNK) * RECORD_SECONDS)):
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    frames.append(data)


volumeFactor = 1.4
multiplier = pow(2, (np.sqrt(np.sqrt(np.sqrt(volumeFactor))) * 192 - 192)/6)

# Doing Something To Data Here To Incrase Volume Of It
numpy_data = np.array(frames, dtype=np.int16)
# double the volume using the factor computed above
np.multiply(numpy_data, multiplier, 
    out=numpy_data, casting="unsafe")


audiodatas = sr.AudioData(numpy_data,RATE,2)

convert_rate = None
convert_width= None

raw_data = audiodatas.get_raw_data(convert_rate, convert_width)
sample_rate = audiodatas.sample_rate if convert_rate is None else convert_rate
sample_width = audiodatas.sample_width if convert_width is None else convert_width

# generate the WAV file contents
with io.BytesIO() as wav_file:
    wav_writer = wave.open(wav_file, "wb")
    try:  # note that we can't use context manager, since that was only added in Python 3.4
        wav_writer.setframerate(sample_rate)
        wav_writer.setsampwidth(sample_width)
        wav_writer.setnchannels(2)
        wav_writer.writeframes(raw_data)
        wav_data = wav_file.getvalue()
    finally:  # make sure resources are cleaned up
        wav_writer.close()

    print(type(wav_file))
    wav_file.seek(0)

    with sr.AudioFile(wav_file) as source:
        audio = r.record(source) 
        print(audio)

#wf = wave.open("output.wav", 'wb')
#wf.setnchannels(channels)
#wf.setsampwidth(2)
#wf.setframerate(RATE)
#wf.writeframes(b''.join(numpy_data))
#wf.close()


#
#from os import path
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "output.wav")



try:
    print(r.recognize_google(audio,language="en-GB"))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
