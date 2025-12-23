import flask
from flask import request, render_template, jsonify
import mysql.connector
from mysql.connector import pooling
from contextlib import closing

app = flask.Flask(__name__)

DB_CONFIG = {
    "host": "192.168.0.199",
    "user": "root",
    "password": "1234",
    "database": "miniproject",
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci"
}

cnxpool = pooling.MySQLConnectionPool(
    pool_name="mpool",
    pool_size=5,
    **DB_CONFIG
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/query", methods=["GET", "POST"])
def query_data():
    """
    - GET:  /query?u=1&v=2
    - POST: form-data/body 에 u, v 전달
    반환: distance, line_type, time_of_day 컬럼들을 JSON으로 응답
    """
    # (1) 입력값 수집
    if request.method == "GET":
        u_val = request.args.get("u", "").strip()
        v_val = request.args.get("v", "").strip()
    else:
        u_val = (request.form.get("u") or "").strip()
        v_val = (request.form.get("v") or "").strip()

    # (2) 유효성 검사 + 형 변환
    if not u_val or not v_val:
        return jsonify({"error": "u와 v 값을 모두 입력하세요."}), 400

    try:
        u_int = int(u_val)
        v_int = int(v_val)
    except ValueError:
        return jsonify({"error": "u와 v는 정수여야 합니다."}), 400

    # (3) SQL 준비 (반드시 파라미터 바인딩 사용)
    sql = """
        SELECT distance, line_type, time_of_day
        FROM dummy
        WHERE u = %s AND v = %s
    """

    # (4) 커넥션 풀에서 커넥션을 얻어 안전하게 사용
    try:
        # get_connection()으로 풀에서 커넥션 획득
        with closing(cnxpool.get_connection()) as conn:
            # dictionary=True: 결과를 dict로 받음 (JSON 변환 용이)
            with closing(conn.cursor(dictionary=True)) as cur:
                cur.execute(sql, (u_int, v_int))
                rows = cur.fetchall()
    except mysql.connector.Error as e:
        # DB 오류를 잡아 사용자에게 간결히 전달(로그는 서버에 남기는 것을 권장)
        return jsonify({"error": f"데이터베이스 오류: {e.msg}"}), 500

    # (5) 결과 반환
    if not rows:
        return jsonify({"message": "조건에 맞는 데이터가 없습니다."}), 200

    # 필요하다면 여기서 값 매핑(예: line_type 0/1 → 버스/지하철) 수행 가능
    # for r in rows:
    #     r["line_type_label"] = "버스" if r["line_type"] == 0 else "지하철"

    return jsonify(rows), 200

if __name__ == '__main__':
    app.run(debug=True)