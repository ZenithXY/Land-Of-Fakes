from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key")  # Needed for session

def load_codes():
    with open('codes.json') as f:
        return json.load(f)

def save_codes(codes):
    with open('codes.json', 'w') as f:
        json.dump(codes, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('access_code')
        codes = load_codes()

        if code in codes and codes[code] == "valid":
            # Store access in session
            session['authenticated'] = True
            session['code'] = code
            codes[code] = "used"
            save_codes(codes)
            return redirect('/gallery')
        else:
            return render_template('error.html')

    return render_template('index.html')

@app.route('/gallery')
def gallery():
    if not session.get('authenticated'):
        return redirect('/')
    return redirect('https://landoffakes.pixieset.com')  # Or render_template if embedding

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
