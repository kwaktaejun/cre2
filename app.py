import os
import pandas as pd
import requests
import time
from flask import Flask, request, render_template

app = Flask(__name__)

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_DB_ID = "1d555b3f92ba8104a80eda4755e07e54"
NOTION_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

@app.route('/')
def index():
    return "Hello from Flask!"

@app.route('/upload_excel_notion', methods=['GET', 'POST'])
def upload_excel_notion():
    if request.method == 'GET':
        return render_template('upload_excel_notion.html')

    file = request.files['file']
    filepath = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)

    df = pd.read_excel(filepath, sheet_name='영상감시시스템')

    for i, row in df.iterrows():
        payload = {
            "parent": { "database_id": NOTION_DB_ID },
            "properties": {
                "구분": {"select": {"name": row["구분"]}},
                "계약여부": {"select": {"name": row["계약여부"]}},
                "식별번호": {"number": int(row["식별번호"])},
                "계약금액": {"number": int(row["계약금액"])},
                "제품모델명": {"title": [{"text": {"content": row["제품모델명"]}}]},
                "품명": {"rich_text": [{"text": {"content": row["품명"]}}]},
                "모델명": {"rich_text": [{"text": {"content": row["모델명"]}}]},
                "규격": {"rich_text": [{"text": {"content": row["규격"]}}]},
                "수량": {"rich_text": [{"text": {"content": str(row["수량"])}}]},
                "원산지": {"rich_text": [{"text": {"content": row["원산지"]}}]},
                "비고": {"rich_text": [{"text": {"content": str(row["비고"])}}]},
            }
        }
        res = requests.post(NOTION_API_URL, headers=headers, json=payload)
        print(f"[{i}] 상태: {res.status_code}, 응답: {res.text}")
        time.sleep(0.5)

    return "전송 완료"

if __name__ == "__main__":
    app.run(debug=True)
