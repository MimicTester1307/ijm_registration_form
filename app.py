from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

""" Setting up access to the Spreadsheet File """
# Creating Scope for File Editing
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

creds = ServiceAccountCredentials.from_json_keyfile_name("arise-conference-2021-beff271a724d.json", scope)
client = gspread.authorize(creds)  # authorizing the gspread object using the credentials

""" Flask Server Section """
app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def receive_data():
    error = None
    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        phone_number = request.form.get("phoneNumber")
        volunteer_type = request.form.get("volunteerType")

        return f"{first_name} {last_name} {email} {phone_number} {volunteer_type}"


def write_to_sheet(iterable: list) -> None:
    pass


if __name__ == '__main__':
    app.run(debug=True)
