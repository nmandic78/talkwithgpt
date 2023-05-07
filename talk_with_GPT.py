import openai
from elevenlabs import generate, play
from playsound import playsound

import pyaudio
import wave
import threading
import queue
import os
import sys


# Set your OpenAI API key
openai.api_key = "sk-XXXXXXXXXXXXXXX"

# Record audio
def record_audio(filename, stop_event, audio_queue):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Press enter to finish recording.")

    while not stop_event.is_set():
        data = stream.read(CHUNK)
        audio_queue.put(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(list(audio_queue.queue)))

# Transcribe audio
def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language='en')
        return transcript["text"]

# send question to our sarcastic AI
def chatgpt(question):
    # Generate a response. You can set a tone, role, style with few-shot in messages list.
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant chatbot that reluctantly answers questions with sarcastic responses."},
        {"role": "user", "content": "How many pounds are in a kilogram?"},
        {"role": "assistant", "content": "This again? There are 2.2 pounds in a kilogram. Please make a note of this."},
        {"role": "user", "content": "What does HTML stand for?"},
        {"role": "assistant", "content": "Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future."},
        {"role": "user", "content": question}
    ],
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.8,)

    response = completion.choices[0].message.content
    return response

# Transcribe audio
def say_answer(text):
    audio = generate(
    text,
    voice="Antoni",
    model="eleven_monolingual_v1",
    api_key="XXXXXXXXXXXXXXX" # register for free and put your own (even though you have some small number of requests without your API key)
    )

    filename = 'temp_answer.mp3'
    with open(filename, 'wb') as file:
        file.write(audio)

    playsound("temp_answer.mp3")


# Main function
def main():
    audio_filename = "recorded_audio.wav"
    stop_event = threading.Event()
    audio_queue = queue.Queue()

    record_thread = threading.Thread(target=record_audio, args=(audio_filename, stop_event, audio_queue))
    record_thread.start()

    input("Press the return key to stop recording...\n")
    stop_event.set()
    record_thread.join()

    transcription = transcribe_audio(audio_filename)
    print("Transcription:", transcription)

    answer = chatgpt(transcription)
    print("Answer:", answer)

    say_answer(answer)

if __name__ == "__main__":
    main()
