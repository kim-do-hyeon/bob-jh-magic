from flask import Flask, request, jsonify, render_template
import hashlib

app = Flask(__name__)

def calculate_md5(file):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    file.seek(0)  # Reset file pointer to the beginning
    return hash_md5.hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    file_hash = calculate_md5(file)
    return jsonify({'hash': file_hash, 'message': 'File uploaded and hash calculated'})

if __name__ == '__main__':
    app.run(debug=True)
