import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from flask import Flask, request, jsonify
import sys
import json
import requests 

sys.path.append('./ff_proto')

try:
    import freefire_pb2
    import account_show_pb2
    print("Proto files successfully load ho gayi!")
except Exception as e:
    print("Proto load error:", e)

app = Flask(__name__)

def load_token(region):
    filename = f'token_{region}.json'
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                # Yahan fix kiya hai: Agar file me list hai to usko pehla item nikal kar dictionary bana dega
                if isinstance(data, list):
                    if len(data) > 0:
                        if isinstance(data[0], dict):
                            return data[0]
                        else:
                            return {"token": str(data[0])}
                    else:
                        return {"error": "Token file khali hai!"}
                return data # Agar pehle se dictionary hai to direct bhej dega
        except:
            return {"error": "Token read nahi hua!"}
    return {"error": f"Region '{region}' ka token nahi mila!"}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Success", "message": "Global Free Fire API Live Hai!"})

@app.route('/get_player', methods=['GET'])
def get_player():
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind')
    
    if not uid:
        return jsonify({"error": "Bhai UID to daal!"}), 400

    token_data = load_token(region)
    if "error" in token_data:
        return jsonify(token_data), 400

    try:
        # Free Fire Server par request bhejna
        game_url = token_data.get('url', f"https://client.{region}.freefiremobile.com/GetPlayerPersonalProfile")
        
        headers = {
            "Authorization": f"Bearer {token_data.get('token', '')}",
            "Content-Type": "application/x-protobuf"
        }
        
        # Asli server hit!
        response = requests.get(f"{game_url}?uid={uid}", headers=headers, timeout=10)
        
        # Agar game server ne data diya, toh proto se decode karo
        if response.status_code == 200:
            player_data = account_show_pb2.AccountProfile()
            player_data.ParseFromString(response.content)
            
            # Yahan decode kiya hua data bhej rahe hain
            return jsonify({
                "status": "Success",
                "uid": uid,
                "region": region,
                "nickname": player_data.nickname if hasattr(player_data, 'nickname') else "Unknown",
                "message": "Data successfully fetched from game server!"
            })
        else:
            return jsonify({"error": "Game server ne block kar diya ya Token expire ho gaya"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"Data lane me dikkat: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
