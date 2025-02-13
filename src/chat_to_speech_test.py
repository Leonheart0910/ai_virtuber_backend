import pytchat
import asyncio
from texttospeech_google import generate_audio_and_subtitle  # 텍스트를 음성으로 변환하는 함수

# YouTube Video ID for live stream (실시간 방송의 비디오 ID)
video_id = 'JdC_gOAEqjg'  # YTN 방송 예시
file_path = './live.csv'

# 실시간 채팅을 받기 위한 pytchat 설정
chat = pytchat.create(video_id=video_id)

# 새로운 채팅을 받아서 GPT 응답 후 음성으로 변환하는 비동기 함수
async def process_chat_message(message):
    # GPT 응답 생성 후 음성으로 변환
    await asyncio.to_thread(generate_audio_and_subtitle, message)  # 비동기로 실행

# 실시간 채팅을 처리하는 비동기 함수
async def capture_and_convert_chat():
    cnt = 0
    last_message_time = None  # 마지막으로 처리된 메시지의 시간

    while chat.is_alive():
        try:
            data = chat.get()
            items = data.items
            for c in items:
                # 이미 처리한 메시지는 건너뛰기 (중복 메시지 방지)
                if last_message_time == c.datetime:
                    continue

                print(f"{c.datetime} [{c.author.name}] - {c.message}")

                # 메시지를 비동기로 처리하여 GPT 응답을 음성으로 변환
                await process_chat_message(c.message)

                # 마지막 메시지 시간 업데이트
                last_message_time = c.datetime

            # 일정 시간마다 채팅을 확인하고 처리하도록 설정
            await asyncio.sleep(1)

            cnt += 1
            if cnt == 5:
                break  # 5번의 채팅 이후 종료 (조정 가능)

        except KeyboardInterrupt:
            chat.terminate()
            break

# 비동기 이벤트 루프 시작
if __name__ == "__main__":
    asyncio.run(capture_and_convert_chat())
