from dotenv import load_dotenv
from google import genai
import os
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
from kokoro import KPipeline
import soundfile as sf
from RealtimeSTT import AudioToTextRecorder

load_dotenv()
API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")
client = genai.Client(api_key=API_KEY_GEMINI)

def speech_to_text_fast():
    recorder = AudioToTextRecorder()
    recorder.start()
    input("Press Enter to stop recording...")
    recorder.stop()
    print("Transcription: ", recorder.text())
    return recorder.text()


def speech_to_text():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(device)
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-large-v3-turbo"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    
    processor = AutoProcessor.from_pretrained(model_id)
    
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )
    result = pipe("audio.wav")
    return result["text"]

def text_to_speech(text):
    pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice
    print("talking")
    generator = pipeline(
    text, voice='af_heart', # <= change voice here
    speed=1, split_pattern=r'\n+'
    )
    for i, (gs, ps, audio) in enumerate(generator):
        print(i)  # i => index
        print(gs) # gs => graphemes/text
        print(ps) # ps => phonemes
        sf.write(f'{i}.wav', audio, 24000) # save each audio file
    

def ask_llm(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
    )
    return response.text



def main():
    #text_to_speech(ask_llm(speech_to_text_fast()))
    text= '''
    I switched from Arch to NixOS 6 months ago as arch was letting me down right when i needed my laptop the most, I have had to fix it using the archiso and reinstall it many times.
Arch can be stable if you want it, but for my tinkering use case, it broke a lot. 
I broke Hyprland and was KDE plasma in the meantime, but I was too busy to fix it and I thought reinstalling it would be easier than fixing it.
I gave up on rolling release distro's and was seriously considering to move to debain stable at this point, but i though development would be an issue there due to outdated packages.
I had heard about nixos from youtube and thought i was sold on it, I knew that it would be a challenge, but since i had my holidays coming up i had the time for it.
    '''
    text_to_speech(text)




if __name__ == "__main__":
    main()
    exit()
