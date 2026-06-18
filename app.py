import os
import urllib.parse
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from google import genai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# 구글 제미나이 클라이언트 초기화 (Render Environment에 GEMINI_API_KEY가 있어야 합니다)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def kakao_text(text):
    """카카오톡 텍스트 응답 규격 생성"""
    safe_text = text[:950] + "..." if len(text) > 950 else text
    return {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": safe_text
                }
            }]
        }
    }

@app.route("/", methods=["GET"])
def home():
    return "서버가 정상적으로 켜져 있습니다!"

# 📰 쌤이 알려주신 상세 주소 방식 1 (네이버 뉴스)
@app.route("/naver-news", methods=["POST"])
def naver_news_skill():
    data = request.get_json(silent=True) or {}
    user_input = data.get("action", {}).get("params", {}).get("파라미터", "").strip()
    
    if not user_input:
        user_input = data.get("userRequest", {}).get("utterance", "").strip()

    if not user_input:
        return jsonify(kakao_text("검색어가 없습니다."))

    query = urllib.parse.quote(user_input)
    url = f"https://search.naver.com/search.naver?where=news&query={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        news_titles = soup.select(".news_tit")
        
        titles = []
        for title in news_titles[:5]:
            titles.append(title.get_text())

        if titles:
            result = f"📰 ['{user_input}'] 네이버 뉴스 검색 결과:\n\n" + "\n\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
        else:
            result = f"['{user_input}']에 대한 뉴스 검색 결과를 찾지 못했습니다."
    except Exception as e:
        result = f"뉴스 조회 중 오류 발생: {str(e)}"

    return jsonify(kakao_text(result))

# 🤖 쌤이 알려주신 상세 주소 방식 2 (구글 제미나이 AI)
@app.route("/gemini-param", methods=["POST"])
def gemini_skill():
    data = request.get_json(silent=True) or {}
    user_question = data.get("action", {}).get("params", {}).get("파라미터", "").strip()

    if not user_question:
        return jsonify(kakao_text("질문 내용(파라미터)이 비어있습니다."))

    if not os.getenv("GEMINI_API_KEY"):
        return jsonify(kakao_text("GEMINI_API_KEY 환경변수가 설정되지 않았습니다."))

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_question,
        )
        result_text = response.text.strip()
    except Exception as e:
        result_text = f"Gemini 호출 중 오류 발생: {str(e)}"

    return jsonify(kakao_text(result_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
