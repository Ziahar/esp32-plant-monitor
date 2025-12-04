# ... весь твій попередній код залишається без змін ...

from datetime import datetime

# Нова сторінка історії
@app.route('/history')
def history_page():
    return render_template('history.html')

# Новий API — повертає дані тільки за вибраний період
@app.route('/api/history')
def api_history():
    start_str = request.args.get('start')
    end_str   = request.args.get('end')

    if not start_str or not end_str:
        return jsonify([])

    try:
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        end_dt   = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
    except:
        return jsonify([]), 400

    all_data = []
    db_files = sorted([f for f in os.listdir(DB_DIR) if f.endswith('.db')])

    for db_file in db_files:
        db_path = os.path.join(DB_DIR, db_file)
        try:
            db = get_db(db_path)
            measurements = db.session.query(Measurement)\
                .filter(Measurement.timestamp >= start_dt)\
                .filter(Measurement.timestamp <= end_dt)\
                .order_by(Measurement.timestamp).all()
            all_data.extend([m.to_dict() for m in measurements])
            db.session.close()
        except:
            continue

    return jsonify(all_data)
