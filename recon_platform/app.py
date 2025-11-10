from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Transaction, MatchResult
from datetime import datetime
import pandas as pd
import io
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://brandonwong:password@localhost/recon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploaded")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def reconcile_files(df_source, df_target, keys, values):
    source_key, target_key = keys
    source_val, target_val = values

    df_source.columns = df_source.columns.str.strip()
    df_target.columns = df_target.columns.str.strip()

    # Merge on provided left/right keys
    merged = pd.merge(
        df_source,
        df_target,
        how='outer',
        left_on=source_key,
        right_on=target_key,
        suffixes=('_source', '_target'),
        indicator=True
    )

    # For merge with non-overlapping keys, all rows should be left_only or right_only
    # Mark a row as matched if it exists on both sides and the value columns (if present) match,
    # otherwise ALL rows are unmatched (if keys do not overlap)

    def is_match(row):
        # Only compare if merged, else always unmatched
        if row['_merge'] != 'both':
            return False
        v_src = row.get(source_val)
        v_tgt = row.get(target_val)
        if pd.isnull(v_src) or pd.isnull(v_tgt):
            return False
        return str(v_src).strip() == str(v_tgt).strip()

    merged['is_matched'] = merged.apply(is_match, axis=1)
    matched = merged[merged['is_matched']].copy()
    unmatched = merged[~merged['is_matched']].copy()  # This will now include left_only, right_only, and mismatches

    print(merged[['_merge', source_key, target_key, source_val, target_val]])
    print("Matched rows:", len(matched))
    print("Unmatched rows:", len(unmatched))

    return matched, unmatched


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    upload_type = request.args.get('type')  # 'source' or 'target'

    if not file or not upload_type:
        return jsonify({'error': 'file or type missing'}), 400

    # Save file with fixed filename
    save_path = os.path.join(UPLOAD_FOLDER, f"{upload_type}.csv")
    file.save(save_path)

    # Optionally, get column headers
    try:
        df = pd.read_csv(save_path, nrows=1)
        headers = df.columns.tolist()
    except Exception as e:
        headers = []
        print(f"Header read failed: {e}")

    return jsonify({'message': f'{upload_type} file uploaded', 'headers': headers})

@app.route('/match', methods=['POST'])
def match_files():
    config = request.json.get('config', {})
    source_key = config.get('sourceKey')  # source file key header
    target_key = config.get('targetKey')  # target file key header
    source_val = config.get('sourceVal')  # source file value header
    target_val = config.get('targetVal')  # target file value header

    df_source = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'source.csv'))
    df_target = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'target.csv'))

    try:
        matched, unmatched = reconcile_files(df_source, df_target, 
                                             keys=(source_key, target_key),
                                             values=(source_val, target_val))
    except KeyError as e:
        return jsonify({'error': str(e)}), 400
    
    return jsonify({
        'matched': matched.to_dict(orient='records'),
        'unmatched': unmatched.to_dict(orient='records'),
        'matched_count': len(matched),
        'unmatched_count': len(unmatched)
    })



@app.route('/exceptions', methods=['GET'])
def get_exceptions():
    exceptions = MatchResult.query.filter(MatchResult.status == 'exception').all()
    result = []
    for ex in exceptions:
        result.append({
            'id': ex.id,
            'transaction_1': ex.transaction_id_1,
            'transaction_2': ex.transaction_id_2,
            'status': ex.status,
            'approved': ex.approved
        })
    return jsonify(result)

@app.route('/approve/<int:match_id>', methods=['POST'])
def approve_match(match_id):
    match = MatchResult.query.get(match_id)
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    match.approved = True
    db.session.commit()
    return jsonify({'message': 'Match approved'})

@app.route('/config', methods=['POST'])
def save_config():
    config = request.json
    # You can save this config globally, in DB, or as needed for matching
    # Example: store in a global VARIABLE (for demo)
    global MATCH_CONFIG
    MATCH_CONFIG = config
    return jsonify({'message': 'Configuration saved'})

@app.route('/audit_logs', methods=['GET'])
def audit_logs():
    # For demo: return static sample logs
    sample_logs = [
        { 'timestamp': '2025-10-21T00:00:00Z', 'user': 'admin', 'action': 'Upload', 'details': 'Uploaded source_file_1.csv' },
        { 'timestamp': '2025-10-21T01:00:00Z', 'user': 'admin', 'action': 'Configure', 'details': 'Set match keys to transaction_id,date' },
        # Add real logs here
    ]
    return jsonify(sample_logs)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

