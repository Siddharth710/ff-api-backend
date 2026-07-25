# Ye 2 line proto ke saare version errors theek kar dengi
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from flask import Flask, request, jsonify
import sys
import json

# Tumhare ff_proto folder ko link karne ka code
sys.path.append('./ff_proto')

try:
    import freefire_pb2
    import account_show_pb2
    print("Proto files successfully load ho gayi!")
except Exception as e:
    print("Proto load error:", e)

app = Flask(__name__)

# Smart Token Loader
def load_token(region):
    filename = f'token_{region}.json'
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except Exception as e:
            return {"error": f"{filename} read nahi ho payi!"}
    else:
        return {"error": f"Region '{region}' ka token nahi mila!"}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Success", 
        "message": "Bhai, tumhara Global Free Fire Server chal raha hai!"
    })

@app.route('/get_player', methods=['GET'])
def get_player():
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind') 
    
    if not uid:
        return jsonify({"error": "Bhai UID to daal!"}), 400

    token_data = load_token(region)
    
    if "error" in token_data:
        return jsonify(token_data), 400

    return jsonify({
        "uid": uid,
        "region": region,
        "token_status": "Success - Token Loaded",
        "message": f"{region.upper()} server par direct hit karne ke liye ready hai!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
