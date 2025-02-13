import os
from typing import List, Tuple
import proto  # type: ignore
from google.cloud import texttospeech_v1beta1 as texttospeech
from google.cloud.texttospeech_v1beta1.types.cloud_tts import SynthesizeSpeechRequest

# ✅ GPT 응답을 가져오기 위해 gpt_test.py 모듈 import
from gpt_test import generate_gpt_response

from credentials import GOOGLE_JSON_PATH
from generate_audio import play_audio
from generate_subtitle import generate_subtitle_file
from utils import words_length

import ctypes

# ✅ VLC 라이브러리 경로 설정
VLC_PATH = "C:\\Program Files\\VideoLAN\\VLC"
os.add_dll_directory(VLC_PATH)
ctypes.CDLL(os.path.join(VLC_PATH, "libvlc.dll"))

import vlc

# ✅ Google Cloud API 인증 정보 설정
os.environ["BASE_DIR_PATH"] = r"C:\Users\82109\Desktop\BJ_sena\sena\ai_virtuber_backend\src"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_JSON_PATH


def _config_texttospeech_request(text_to_transform_to_audio: str) -> Tuple[SynthesizeSpeechRequest, List[str]]:
    ssml_text = "<speak>"
    response_counter = 0
    mark_array: List[str] = []

    for s in text_to_transform_to_audio.split(" "):
        ssml_text += f'<mark name="{response_counter}"/>{s}<break time="0.15s"/>'
        mark_array.append(s)
        response_counter += 1
    ssml_text += "</speak>"

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    # ✅ **한국어 음성 모델 적용**
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",  # ✅ 한국어 적용
        name="ko-KR-Neural2-A",  # ✅ 한국어 음성 모델 (다른 옵션: "ko-KR-Wavenet-A")
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=0,  # ✅ 기본 음높이 (더 낮추려면 -2, 높이면 +2)
        speaking_rate=1.0,  # ✅ 기본 속도 (더 빠르게: 1.2, 더 느리게: 0.85)
    )

    # ✅ enable_time_pointing을 리스트 형식으로 수정
    speech_request = SynthesizeSpeechRequest(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
        enable_time_pointing=[SynthesizeSpeechRequest.TimepointType.SSML_MARK]
    )
    return speech_request, mark_array


def generate_audio_and_subtitle(user_input: str, audio_filename="audio.mp3"):
    """🎤 사용자 입력을 받아 GPT 응답 후 음성 변환"""
    # ✅ GPT 응답 생성
    gpt_response = generate_gpt_response(user_input)

    print(f"📜 GPT Response: {gpt_response}")
    print(f"Character length = {len(gpt_response)}")
    print(f"Words length = {words_length(gpt_response)}")

    client = texttospeech.TextToSpeechClient()
    request, mark_array = _config_texttospeech_request(gpt_response)
    response = client.synthesize_speech(request=request)

    play_audio(audio_filename, response.audio_content)
    subtitle_file = generate_subtitle_file(response.timepoints, mark_array)

    #print(f"📜 생성된 자막 파일: {subtitle_file}")


### 🚀 **터미널에서 사용자 입력을 받아 GPT 응답 후 음성 출력**
def main():
    print(" 🎤 음성 변환 프로그램 실행 중... (종료하려면 'exit' 입력)")

    while True:
        user_input = input("\n 👤 사용자 입력: ")
        if user_input.lower() == "exit":
            print("👋 프로그램 종료!")
            break

        generate_audio_and_subtitle(user_input)


if __name__ == "__main__":
    main()
