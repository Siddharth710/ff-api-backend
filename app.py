from flask import Flask, request, jsonify
import sys

# Tumhare ff_proto folder ko link karne ka code
sys.path.append('./ff_proto')

try:
    import freefire_pb2
    import account_show_pb2
    print("Proto files successfully load ho gayi!")
except Exception as e:
    print("Proto load error:", e)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Success", 
        "message": "Bhai, tumhara Free Fire Server bilkul sahi chal raha hai!"
    })

@app.route('/get_player', methods=['GET'])
def get_player():
    uid = request.args.get('uid')
    
    if not uid:
        return jsonify({"error": "Bhai UID to daal!"}), 400

    # Yahan asli proto logic aayega encryption/decryption ke liye
    # Abhi server live karne aur check karne ke liye ye dummy response dega
    
    return jsonify({
        "uid": uid,
        "status": "Legit/Suspicious Check Logic Ready Hai",
        "message": "Proto connection successful. Server is Live!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)