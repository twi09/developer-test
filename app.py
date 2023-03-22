from flask import Flask, request, jsonify, render_template
import json 
import os 
from compute_solutions import give_me_the_odds_from_files
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has a file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        # Check if the file is a JSON file
        if file.filename.endswith('.json'): 
            # Load empire.json from request 
            data_empire =json.loads(file.read())
            # Load millennium-falcon.json file 
            path_milenium = "examples/example2/millennium-falcon.json"
            with open(path_milenium) as f:
                data_milenium = json.load(f)
            # Load the database with the routes  
            routes_path = os.path.dirname(path_milenium) + "/" + data_milenium["routes_db"]
            # Compute the odds
            odds = give_me_the_odds_from_files(data_milenium,data_empire,routes_path) 
            return render_template('results.html',odds=odds)
        
        
        else:
            return jsonify({'error': 'File must be a JSON file'}), 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
