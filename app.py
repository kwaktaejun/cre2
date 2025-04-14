
from flask import Flask, render_template, request, send_file
import openpyxl
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        table_data = request.form.get('tableData')
        memo = request.form.get('memo')
        rows = [row.split("\t") for row in table_data.strip().split("\n") if row.strip()]
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "업로드 데이터"
        headers = ["구분", "계약여부", "식별번호", "계약금액", "제품모델명", "품명", "모델명", "규격", "수량", "원산지", "구성종류", "제품원가", "원천제조사", "수익률", "비고", "메모"]
        ws.append(headers)
        for row in rows:
            ws.append(row + [""] * (16 - len(row)))  # 빈 칸 보정

        memo_ws = wb.create_sheet("업로드 메모")
        memo_ws.append(["업로드 메모"])
        memo_ws.append([memo])

        file_stream = BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        filename = f"마스터시트_업로드_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(file_stream, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    return render_template('index.html')
