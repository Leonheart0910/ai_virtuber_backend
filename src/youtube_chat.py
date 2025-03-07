import pytchat  # 실시간 댓글 크롤링
import pafy  # 유튜브 정보
import pandas as pd

api_key = ''  # GCP YouTube Data API에서 API 키 생성
pafy.set_api_key(api_key)

video_id = 'JdC_gOAEqjg'  # [LIVE] 대한민국 24시간 뉴스채널 YTN
file_path = './live.csv'

empty_frame = pd.DataFrame(columns=['댓글 작성자', '댓글 내용', '댓글 작성 시간'])
chat = pytchat.create(video_id=video_id)

while chat.is_alive():
    cnt = 0
    try:
        data = chat.get()
        items = data.items
        for c in items:
            print(f"{c.datetime} [{c.author.name}]- {c.message}")
            data.tick()
            data2 = {
                '댓글 작성자': [c.author.name],
                '댓글 내용': [c.message],
                '댓글 작성 시간': [c.datetime]
            }
            result = pd.DataFrame(data2)
            result.to_csv(file_path, mode='a', header=False)
        cnt += 1
        if cnt == 5:
            break
    except KeyboardInterrupt:
        chat.terminate()
        break

df = pd.read_csv(file_path, names=['댓글 작성자', '댓글 작성시간', '댓글내용'])
df.head(30)
