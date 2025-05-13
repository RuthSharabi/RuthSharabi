from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_map_data = {
    "robot_path": [],
    "detections": []
}

@app.route('/updateMap', methods=['POST'])
def update_map():
    global latest_map_data
    latest_map_data = request.get_json()
    print("עודכן map_data מ־Robot:", latest_map_data)
    return jsonify({"status": "received"})

@app.route("/getMap", methods=["GET"])
def get_map():
    return jsonify({
        "robot_path": robot_path,
        "detections": detections
    })
#
# @app.route('/map-data', methods=['GET'])
# def get_map_data():
#     return jsonify(latest_map_data)

if __name__ == '__main__':
    app.run(debug=True)
