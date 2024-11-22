from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

board = []

@app.route('/', methods=['GET', 'POST'])
def handle_board():
  if request.method == 'GET':
    return jsonify({'board': board})
  elif request.method == 'POST':
    new_msg = request.json.get('message', '')
    if new_msg:
      board.insert(0, new_msg)
    return jsonify({'board': board})

if __name__ == '__main__':
  app.run()

