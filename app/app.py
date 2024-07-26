from flask import Flask, request, jsonify
from models import db, Message
from sqlalchemy.exc import SQLAlchemyError
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

logging.basicConfig(level=logging.INFO)

@app.route('/get/messages/<account_id>', methods=['GET'])
def get_messages(account_id):
    try:
        messages = Message.query.filter_by(account_id=account_id).all()
        return jsonify([message.to_dict() for message in messages]), 200
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/create', methods=['POST'])
def create_message():
    data = request.get_json()
    try:
        new_message = Message(
            account_id=data['account_id'],
            message_id=data['message_id'],
            sender_number=data['sender_number'],
            receiver_number=data['receiver_number']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except KeyError as e:
        logging.error(f"Missing key: {e}")
        return jsonify({"error": f"Missing key: {e}"}), 400

@app.route('/search', methods=['GET'])
def search_messages():
    try:
        query = Message.query
        if 'message_id' in request.args:
            message_ids = request.args.get('message_id').split(',')
            query = query.filter(Message.message_id.in_(message_ids))
        if 'sender_number' in request.args:
            sender_numbers = request.args.get('sender_number').split(',')
            query = query.filter(Message.sender_number.in_(sender_numbers))
        if 'receiver_number' in request.args:
            receiver_numbers = request.args.get('receiver_number').split(',')
            query = query.filter(Message.receiver_number.in_(receiver_numbers))
        messages = query.all()
        return jsonify([message.to_dict() for message in messages]), 200
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

if __name__ == '__main__':
    app.run(host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')))
