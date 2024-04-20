import requests
from keys import HUGGING_FACE_KEY
import time
from detect_language import detect_language


API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


def text_to_text(input: str, language: str, language_out = "fr_XX"):
    output = query({
        "inputs": input,
        "parameters": {"src_lang": language, "tgt_lang": language_out}
    })
    print(output)
    translated_text = output[0]['translation_text']
    return translated_text


input1 = "Ciao, mi chiamo Matthias e oggi facciamo un hackaton"
input2 = "Меня зовут Вольфганг и я живу в Берлине"
print(text_to_text(input2, detect_language(input2)))

