from flask import Flask, render_template, request, Response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import time

# Loading the environment variables
load_dotenv()

SCOPE1 = os.getenv("SCOPE1")
SCOPE2 = os.getenv("SCOPE2")
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")
CLIENT_SECRETS = os.getenv("CLIENT_SECRETS")

""" Setting up access to the Spreadsheet File """
# Creating Scope for File Editing
SCOPE = [SCOPE1, SCOPE2]
CREDS = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRETS, scopes=SCOPE)
CLIENT = gspread.authorize(CREDS)  # authorizing the gspread object using the credentials

# Initializing the row index for the spreadsheet to 2 because the first row serves as the headers.
row_index = 2

""" Flask Server Section """
app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def receive_data():
    if request.method == "POST":
        # Retrieving the values inputted into the form
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")

        # Basic validation for first and last names
        if int(first_name) and int(last_name):
            return Response(response="Invalid first or last names given.", status=400)

        email = request.form.get("email")
        phone_number = request.form.get("phoneNumber")
        volunteer_type = request.form.get("volunteerType")

        # writing the values to the sheet
        write_to_sheet([first_name, last_name, email, phone_number, volunteer_type])
        return render_template("form-success.html")


def write_to_sheet(iterable):
    global row_index

    arise_conference = CLIENT.open_by_url(SPREADSHEET_URL)

    arise_conference.sheet1.insert_row(iterable, row_index)  # inserting the iterable into the sheet as a row

    time.sleep(1)    # using time.sleep to slow down the API calls / requests
    row_index += 1
