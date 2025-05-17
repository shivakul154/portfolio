from flask import Flask, render_template, request
import pandas as pd
import os
import json

app = Flask(__name__)

# Initialize CSV file for storing contact messages
CONTACT_CSV = 'contact_messages.csv'
if not os.path.exists(CONTACT_CSV):
    pd.DataFrame(columns=['Name', 'Email', 'Message']).to_csv(CONTACT_CSV, index=False)

# Load data from JSON files
with open('data/person_info.json', 'r') as f:
    person_info = json.load(f)

with open('data/projects.json', 'r') as f:
    projects_data = json.load(f)

@app.route('/')
def home():
    return render_template('home.html', person=person_info)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_row = pd.DataFrame({"Name": [name], "Email": [email], "Message": [message]})
        # Save the new message to the CSV file
        new_row.to_csv(CONTACT_CSV, mode='a', header=False, index=False)
        return render_template('contact.html', success=True)
    return render_template('contact.html', success=False)

@app.route('/messages')
def view_messages():
    messages = pd.read_csv(CONTACT_CSV).to_dict(orient='records')
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)