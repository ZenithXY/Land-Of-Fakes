from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# Load access codes
def load_codes():
    with open('codes.json') as f:
        return json.load(f)

# Save updated codes
def save_codes(codes):
    with open('codes.json', 'w') as f:
        json.dump(codes, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('access_code')
        codes = load_codes()

        if code in codes and codes[code] == "valid":
            # Invalidate the code (one-time use)
            codes[code] = "used"
            save_codes(codes)
            return redirect('/gallery')
        else:
            return render_template('error.html')

    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
