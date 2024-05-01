from flask import Flask, render_template, request, jsonify
from KWICPlus import KWICPlus

app = Flask(__name__)
kwic_plus = KWICPlus('kwic_data.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keywords = request.json.get('keywords')
    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400
    # Call KWIC+ search method
    search_results = kwic_plus.search(keywords)
    return jsonify(search_results)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    descriptor = request.json.get('descriptor')
    url = request.json.get('url')
    if not descriptor or not url:
        return jsonify({'error': 'Descriptor or URL missing'}), 400
    # Call KWIC+ add_entry_to_xml method
    kwic_plus.add_entry_to_xml(descriptor, url)
    return jsonify({'message': 'Entry added successfully'})

if __name__ == '__main__':
    app.run(debug=True)