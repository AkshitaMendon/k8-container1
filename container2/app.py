from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Persistent Volume Directory
PV_DIR = "/akshita_PV_dir"

@app.route('/compute', methods=['POST'])
def compute_sum():
    
    request_data = request.get_json()

    if not request_data or 'file' not in request_data or not request_data['file'] or 'product' not in request_data or not request_data['product']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    filename = request_data['file']
    target_product = request_data['product']
    file_path = os.path.join(PV_DIR, filename)


    if not os.path.exists(file_path):
        return jsonify({"file": filename, "error": "File not found."}), 404

    try:
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            content = list(csv_reader)

        
        if len(content) < 2:
            return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400

        headers = [col.strip().lower() for col in content[0]]
        if headers != ["product", "amount"]:
            return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400


        total_amount = 0
        for entry in content[1:]:
            if len(entry) != 2:
                return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400

            try:
                product_name = entry[0].strip()
                amount_value = float(entry[1].strip())

                if product_name == target_product:
                    total_amount += amount_value
            except ValueError:
                return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400

        return jsonify({"file": filename, "sum": int(total_amount)}), 200

    except Exception as e:
        return jsonify({"file": filename, "error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
