from flask import Flask
from flask import render_template
from flask import request, jsonify
from datetime import datetime
from models import db, URL
from utils import generate_short_code

#fctfcj

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    short_code = generate_short_code()
    now = datetime.utcnow()
    new_url = URL(
        url=data['url'],
        short_code=short_code,
        created_at=now,
        updated_at=now,
        access_count=0
    )
    db.session.add(new_url)
    db.session.commit()

    return jsonify(new_url.serialize()), 201

@app.route('/shorten/<string:code>', methods=['GET'])
def get_url(code):
    url = URL.query.filter_by(short_code=code).first()
    if not url:
        return jsonify({'error': 'Short URL not found'}), 404
    url.access_count += 1
    db.session.commit()
    return jsonify(url.serialize()), 200

@app.route('/shorten/<string:code>', methods=['PUT'])
def update_url(code):
    url = URL.query.filter_by(short_code=code).first()
    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'New URL is required'}), 400

    url.url = data['url']
    url.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(url.serialize()), 200

@app.route('/shorten/<string:code>', methods=['DELETE'])
def delete_url(code):
    url = URL.query.filter_by(short_code=code).first()
    if not url:
        return jsonify({'error': 'Short URL not found'}), 404
    db.session.delete(url)
    db.session.commit()
    return '', 204

@app.route('/stats/<string:code>', methods=['GET'])
def get_stats(code):
    url = URL.query.filter_by(short_code=code).first()
    if not url:
        return jsonify({'error': 'Short URL not found'}), 404
    return jsonify(url.serialize(include_stats=True)), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures DB is ready
    app.run(debug=True)

