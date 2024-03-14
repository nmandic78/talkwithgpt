# **GPT-Sarcastic-Whisper**

This POC showcases a simple Python script for interacting with GPT models using OpenAI's Whisper ASR API and ElevenAI's TTS API. Record your questions and get sarcastic responses from the chatbot using voice input and output.


#### Installation

Clone the repository:

    git clone https://github.com/nmandic78/talkwithgpt.git

Install the required dependencies:

    pip install -r requirements.txt

Get API keys for OpenAI and ElevenAI.

Replace the placeholder API keys in the script with your own:

    openai.api_key = "sk-XXXXXXXXXXXXXXX"
    api_key="XXXXXXXXXXXXXXX" # register for free and put your own (even though you have some small number of requests without your API key)

#### Usage

Run the main script:

    python talk_with_GPT.py

Follow the instructions in the terminal to record your audio and receive sarcastic responses from the chatbot.

Press the return key to stop recording and let the script transcribe your question, generate a response, and play it back using text-to-speech.

#### Acknowledgements

    OpenAI Whisper ASR API for speech recognition.
    OpenAI GPT-3.5-turbo for generating sarcastic chatbot responses.
    ElevenAI TTS API for text-to-speech conversion.

Enjoy interacting with your sarcastic AI assistant!
