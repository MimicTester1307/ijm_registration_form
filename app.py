from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

""" Setting up access to the Spreadsheet File """
# Creating Scope for File Editing
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("arise-conference-2021-beff271a724d.json", SCOPE)
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
        email = request.form.get("email")
        phone_number = request.form.get("phoneNumber")
        volunteer_type = request.form.get("volunteerType")

        # writing the values to the sheet
        write_to_sheet([first_name, last_name, email, phone_number, volunteer_type])
        return render_template("form-success.html")


def write_to_sheet(iterable):
    global row_index

    arise_conference = CLIENT.open_by_url(
        "https://docs.google.com/spreadsheets/d/1IbNNh4IMtbPp7igSVHkXwc_bFlzfYRRSR8iAyIe35IE")

    arise_conference.sheet1.insert_row(iterable, row_index)  # inserting the iterable into the sheet as a row

    row_index += 1


if __name__ == '__main__':
    app.run(debug=True)
