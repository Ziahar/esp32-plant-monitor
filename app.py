from flask import Flask, request, jsonify, render_template
from database import get_db, Measurement
from datetime import datetime
import os

app = Flask(__name__)

DB_DIR = "/data" if os.path.exists("/data") else "."
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def get_current_db_path():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return os.path.join(DB_DIR, f"{today}.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history_page():
    return render_template('history.html')

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json(force=True)
        print(f"Отримано: {data}")

        db_path = get_current_db_path()
        db = get_db(db_path)
        m = Measurement(soil=int(data['soil']), temp=float(data['temp']), hum=float(data['hum']))
        db.session.add(m)
        db.session.commit()
        db.session.close()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Помилка: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/data')
def api_data():
    all_data = []
    for db_file in sorted([f for f in os.listdir(DB_DIR) if f
