#!/bin/python3

from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

def get_election_and_rep_info():
    api_key = "REPLACE THIS"  # Replace with your actual API key
    address = "REPLACE THIS"  # Replace with your address
    election_url = f"https://www.googleapis.com/civicinfo/v2/voterinfo?key={api_key}&address={address}"
    representative_url = f"https://www.googleapis.com/civicinfo/v2/representatives?key={api_key}&address={address}"

    try:
        # Fetch election information
        election_response = requests.get(election_url)
        election_response.raise_for_status()
        election_data = election_response.json()

        # Fetch representative information
        representative_response = requests.get(representative_url)
        representative_response.raise_for_status()
        representative_data = representative_response.json()
        
        # Example data extraction (adjust according to the API response structure)
        election_name = election_data.get("election", {}).get("name", "Unknown Election")
        polling_location = election_data.get("pollingLocations", [{}])[0].get("address", {}).get("locationName", "Unknown Location")
        
        # Example extraction of representative information
        representatives = []
        for office in representative_data.get("offices", []):
            for official_index in office.get("officialIndices", []):
                representative = representative_data.get("officials", [])[official_index]
                representatives.append({
                    "name": representative.get("name", "Unknown"),
                    "party": representative.get("party", "Unknown"),
                    "office": office.get("name", "Unknown")
                })
        
        return election_name, polling_location, representatives
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, None, []
    except (KeyError, IndexError) as e:
        print(f"Error processing response: {e}")
        return None, None, []


@app.route("/")
def index():
    election_name, polling_location, representatives = get_election_and_rep_info()
    if election_name and polling_location:
        return render_template("election_and_rep_info.html", election_name=election_name, polling_location=polling_location, representatives=representatives)
    else:
        return "Failed to load election and representative information", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
