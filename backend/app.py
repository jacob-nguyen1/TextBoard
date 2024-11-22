from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

board = []

@app.route('/', methods=['GET', 'POST'])
def handle_board():
  global board
  if request.method == 'GET':
    return jsonify({'board': board})
  elif request.method == 'POST':
    new_msg = request.json.get('message', '')
    if new_msg:
      board.insert(0, new_msg)
      socketio.emit('update_board', {'board': board})
    return jsonify({'board': board})

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=8080)
