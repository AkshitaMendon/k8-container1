from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Persistent Volume directory path
PV_DIR = "/akshita_PV_dir"


os.makedirs(PV_DIR, exist_ok=True)

@app.route('/store-file', methods=['POST'])
def store_file():

    data = request.json
    filename = data.get("file")
    content = data.get("data")

    if not filename or not content:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(PV_DIR, filename)

    try:
        with open(file_path, "w") as file:
            file.write(content)
        return jsonify({"file": filename, "message": "Success."}), 200
    except Exception as e:
        return jsonify({"file": filename, "error": f"Error while storing the file: {str(e)}"}), 500


@app.route('/calculate', methods=['POST'])
def calculate():

    request_data = request.get_json()
    filename = request_data.get('file')
    product = request_data.get('product')

    if not filename or not product:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(PV_DIR, filename)

    if os.path.exists(file_path):
        selected_file = filename
    else:
        selected_file = None
        base_filename, _ = os.path.splitext(filename)

        for existing_file in os.listdir(PV_DIR):
            existing_base, extension = os.path.splitext(existing_file)
            if existing_base == base_filename and extension.lower() in ['.csv', '.dat', '.yml', '.txt']:
                selected_file = existing_file
                break

    if not selected_file:
        return jsonify({"file": filename, "error": "File not found."}), 404

    try:
    
        response = requests.post('http://container2:7000/compute', json={"file": selected_file, "product": product})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with Container 2: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
