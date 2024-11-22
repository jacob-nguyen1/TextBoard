from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="https://text-board.netlify.app")

board = []

@app.route('/api/board', methods=['GET', 'POST', 'OPTIONS'])
def handle_board():
  global board
  if request.method == 'OPTIONS':
      # Handle CORS preflight requests
      return '', 204
  elif request.method == 'GET':
      return jsonify({'board': board})
  elif request.method == 'POST':
      new_msg = request.json.get('message', '')
      if new_msg:
          board.insert(0, new_msg)
          socketio.emit('update_board', {'board': board})
      return jsonify({'board': board})

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=8080)
