from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# ⭐️ 카카오 챗봇 퀴즈 블록 ID 5개 세팅
QUIZ_BLOCK_IDS = [
    "6a178630a473984e628570b2",
    "6a1786f534f90d922e3fe88f",
    "6a17872470e65519fcd3dc7a",
    "6a1787ce568d272d8eb10783",
    "6a178a26a473984e62857169"
]

@app.route('/api/random-quiz', methods=['POST'])
def redirect_to_random_quiz():
    # 5개의 블록 ID 중 하나를 랜덤으로 무작위 선택
    chosen_block_id = random.choice(QUIZ_BLOCK_IDS)
    
    # 카카오톡이 해당 블록으로 자동 이동하도록 리다이렉트 응답 구성
    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": []  # 화면 텍스트 없이 바로 블록 이동
        },
        "context": {
            "values": []
        },
        "data": {
            "blockId": chosen_block_id
        }
    }
    
    return jsonify(kakao_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
