from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    code = request.form.get("code")
    return redirect(f'https://localhost:5000/?code={code}')

if __name__ == '__main__':
    app.run(debug=True)
