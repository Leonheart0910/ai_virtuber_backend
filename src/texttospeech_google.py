import os
from typing import List, Tuple

import proto  # type: ignore
from google.cloud import texttospeech_v1beta1 as texttospeech
from google.cloud.texttospeech_v1beta1.types.cloud_tts import (
    SynthesizeSpeechRequest,
)

from credentials import GOOGLE_JSON_PATH
from generate_audio import play_audio
from generate_subtitle import generate_subtitle_file
from utils import words_length

import ctypes

VLC_PATH = "C:\\Program Files\\VideoLAN\\VLC"  # VLC가 설치된 경로 확인 후 수정
os.add_dll_directory(VLC_PATH)  # DLL 경로 추가
ctypes.CDLL(os.path.join(VLC_PATH, "libvlc.dll"))  # VLC 라이브러리 로드

import vlc

os.environ["BASE_DIR_PATH"] = r"C:\Users\halo0\Desktop\leonproject\ai-bj\test_api\Kuebiko-main\vtube_test\src"
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

    voice = texttospeech.VoiceSelectionParams(
        language_code="es-US",
        name="es-US-Neural2-A",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=4,
        speaking_rate=0.9,
    )

    SSML_MARK = proto.RepeatedField(
        proto_type=proto.ENUM,
        enum=SynthesizeSpeechRequest.TimepointType,
        number=SynthesizeSpeechRequest.TimepointType.SSML_MARK,
        message="SSML_MARK",
    )
    # enable_time_pointing을 리스트 형식으로 수정
    speech_request = SynthesizeSpeechRequest(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
        enable_time_pointing=[SynthesizeSpeechRequest.TimepointType.SSML_MARK]  # 리스트로 수정
    )
    return (speech_request, mark_array)


def generate_audio_and_subtitle(user_question: str, audio_filename="audio.mp3"):
    text_to_transform_to_audio = user_question
    print(f"Character length = {len(text_to_transform_to_audio)}")
    print(f"Words length = {words_length(text_to_transform_to_audio)}")

    client = texttospeech.TextToSpeechClient()
    request, mark_array = _config_texttospeech_request(text_to_transform_to_audio)
    response = client.synthesize_speech(request=request)

    play_audio(audio_filename, response.audio_content)
    subtitle_file = generate_subtitle_file(response.timepoints, mark_array)

    #print(f"📜 생성된 자막 파일: {subtitle_file}")


### 🚀 **터미널에서 사용자 입력을 받아 음성 출력 및 자막 생성**
def main():
    print(" 음성 변환 프로그램 실행 중... (종료하려면 'exit' 입력)")

    while True:
        user_input = input("\n 사용자 입력: ")
        if user_input.lower() == "exit":
            print("프로그램 종료!")
            break

        generate_audio_and_subtitle(user_input)


if __name__ == "__main__":
    main()
