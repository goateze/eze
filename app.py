import urllib.parse
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

def kakao_text(text):
    """카카오톡 텍스트 응답 규격 생성 (1000자 제한 안전장치)"""
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
    return "Naver News Crawler Server is running."

@app.route("/naver-news", methods=["POST"])
def naver_news_skill():
    data = request.get_json(silent=True) or {}
    # 카카오톡 파라미터에서 검색어를 가져옵니다.
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
        for title in news_titles[:5]: # 상위 5개 추출
            titles.append(title.get_text())

        if titles:
            result = f"📰 ['{user_input}'] 네이버 뉴스 검색 결과:\n\n" + "\n\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
        else:
            result = f"['{user_input}']에 대한 네이버 뉴스 검색 결과를 찾지 못했습니다."

    except Exception as e:
        result = f"네이버 뉴스 조회 중 오류 발생: {str(e)}"

    return jsonify(kakao_text(result))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
