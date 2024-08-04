from flask import Flask, request, jsonify, render_template
import hashlib

app = Flask(__name__)

def calculate_hashes(file):
    file.seek(0)
    data = file.read()
    
    md5_hash = hashlib.md5(data).hexdigest()
    sha1_hash = hashlib.sha1(data).hexdigest()
    sha256_hash = hashlib.sha256(data).hexdigest()
    
    file.seek(0)  # Reset file pointer to the beginning
    
    return md5_hash, sha1_hash, sha256_hash

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
    
    md5_hash, sha1_hash, sha256_hash = calculate_hashes(file)
    filename = file.filename
    return jsonify({'filename': filename, 'md5': md5_hash, 'sha1': sha1_hash, 'sha256': sha256_hash})

if __name__ == '__main__':
    app.run(debug=True)
