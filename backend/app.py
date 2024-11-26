from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def initialize_board():
   try:
      connection = get_mysql_connection()
      cursor = connection.cursor()
      cursor.execute('CREATE TABLE IF NOT EXISTS board_messages (id INT AUTO_INCREMENT PRIMARY KEY, message TEXT NOT NULL)')
      cursor.execute('SELECT message FROM board_messages ORDER BY id DESC')
      messages = cursor.fetchall()
      connection.close()
      return [message[0] for message in messages]
   except Exception as e:
      print(f"Error initializing board: {e}")
      return []

board = initialize_board()

@app.route('/api/board', methods=['GET', 'POST'])
def handle_board():
    global board
    try:
        if request.method == 'GET':
            print(f"BOARD: {board}")
            return jsonify({'board': board})
        elif request.method == 'POST':
            new_msg = request.json.get('message', '')
            print(new_msg)
            if new_msg:
                connection = get_mysql_connection()
                cursor = connection.cursor()
                cursor.execute('INSERT INTO board_messages (message) VALUES (%s)', (new_msg,))
                connection.commit()
                connection.close()
                board = initialize_board()
                socketio.emit('update_board', {'board': board})
            return jsonify({'board': board})
    except Exception as e:
        print(f"Error in /api/board route: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=8080)
