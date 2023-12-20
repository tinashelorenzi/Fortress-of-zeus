from flask import Flask, request, jsonify
import firebase_handler

app = Flask(__name__)

@app.route('/')
def check_code():
    try:
        # Get the 'code' parameter from the URL
        code = int(request.args.get('code'))

        if firebase_handler.code_check('admin',code):
            return "Security check success"
        else:
            return "Code is not valid or expired"

    except ValueError:
        # Handle the case where 'code' is not a valid integer
        return jsonify({'error': 'Invalid code parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True)
