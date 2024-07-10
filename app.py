#!/bin/python3

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace 'your_api_key' with your actual Congress.gov API key
API_KEY = 't9HEFXwJ6j0xblfeJMxLL81VN2dY59tus8vjamXC'

def get_recent_members():
    url = f"https://api.congress.gov/v3/member?api_key={API_KEY}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['members']
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

@app.route("/")
def index():
    members = get_recent_members()
    if members:
        return render_template("index.html", members=members)
    else:
        return "Failed to load membes of congress", 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

