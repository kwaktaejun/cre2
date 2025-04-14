
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import requests
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_TOKEN = "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"
NOTION_DB_ID = "1c255b3f92ba807db04be2edf1ac5f36"
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_excel_notion', methods=['GET', 'POST'])
def upload_excel_notion():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            df = pd.read_excel(filepath, sheet_name='영상감시시스템')
            df = df.fillna("")

            columns = [
                "구분", "계약여부", "식별번호", "계약금액", "제품모델명",
                "품명", "모델명", "규격", "수량", "원산지 / 제조사",
                "구성종류", "제품원가", "원천제조사", "수익률"
            ]
            df = df[columns]

            success, fail = 0, 0
            for _, row in df.iterrows():
                props = {}
                for col in columns:
                    val = row[col]
                    if col in ["수량", "수익률"]:
                        props[col] = {"number": float(val) if val != "" else 0}
                    else:
                        props[col] = {"rich_text": [{"text": {"content": str(val)}}]}
                payload = {
                    "parent": {"database_id": NOTION_DB_ID},
                    "properties": props
                }
                res = requests.post(NOTION_API_URL, headers=headers, json=payload)
                if res.status_code == 200:
                    success += 1
                else:
                    fail += 1

            return render_template('result.html', success=success, fail=fail)
    return render_template('upload.html')
