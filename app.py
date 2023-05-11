import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC6fdd3b2da26d4cfa0f3f98ae73d8df35'
    TWILIO_SYNC_SERVICE_SID = 'IS7f0393937ad5785513bc3e942163aea9'
    TWILIO_API_KEY = 'SK49ce36853fbabe2cd66691ab7e079de4'
    TWILIO_API_SECRET = 'gR69oYSORd9HPV4aGIfTnVZZkyehQGCT'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    main_text = request.form["text"]
    with open("workfile.txt", "w") as w:
        w.write(main_text)

    store_text = "workfile.txt"
    return send_file(store_text, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
