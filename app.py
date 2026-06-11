from flask import Flask, jsonify
import random

app = Flask(__name__)

# ⭐️ 사용자님이 보내주신 퀴즈 블록 ID 5개 목록
QUIZ_BLOCK_IDS = [
    "6a178630a473984e628570b2",  # 1번퀴즈
    "6a1786f534f90d922e3fe88f",  # 2번퀴즈
    "6a17872470e65519fcd3dc7a",  # 3번퀴즈
    "6a1787ce568d272d8eb10783",  # 4번퀴즈
    "6a178a26a473984e62857169"   # 5번퀴즈
]

# 선생님이 가르쳐주신 기본 주소('/') 구조 그대로 사용합니다!
@app.route('/', methods=["GET", "POST"])
def index():
    # 5개의 퀴즈 블록 중 하나를 무작위 선택
    chosen_block_id = random.choice(QUIZ_BLOCK_IDS)
    
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    # ⚠️ 빈 말풍선(하얀 점) 버그를 막기 위해 안내 문구를 꼭 넣어줍니다.
                    "simpleText": {
                        "text": "🎯 문제를 무작위로 가져오고 있습니다!"
                    }
                }
            ]
        },
        "data": {
            # 카카오톡에게 랜덤으로 뽑힌 블록으로 이동하라고 명령하는 핵심 키
            "blockId": chosen_block_id
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
