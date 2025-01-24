from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

def initialize_board():
   with sqlite3.connect('board.db') as conn:
      cursor = conn.cursor()
      cursor.execute('SELECT message FROM board_messages ORDER BY id DESC')
      messages = cursor.fetchall()
      return [message[0] for message in messages]

try:
    board = initialize_board()
except:
    board = []

@app.route('/api/board', methods=['GET', 'POST'])
def handle_board():
    global board
    try:
        if request.method == 'GET':
            with sqlite3.connect('board.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT message FROM board_messages ORDER BY id DESC')
                messages = cursor.fetchall()
                board = [message[0] for message in messages]
            return jsonify({'board': board})

        elif request.method == 'POST':
            new_msg = request.json.get('message', '')
            print(new_msg)
            if new_msg:
                with sqlite3.connect('board.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('CREATE TABLE IF NOT EXISTS board_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT NOT NULL)')
                    cursor.execute('INSERT INTO board_messages (message) VALUES (?)', (new_msg,))
                    conn.commit()
                board = initialize_board()
                socketio.emit('update_board', {'board': board})
            return jsonify({'board': board})
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=8080)
