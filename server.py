from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open("database.txt", mode="a") as database:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f"\n{name}, {email}, {subject}, {message}")

def write_to_csv(data):
    file_is_empty = os.stat("database.csv").st_size == 0
    with open("database.csv", mode="a", newline='') as database2:
        csv_writer = csv.writer(database2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if file_is_empty:
            csv_writer.writerow(["name", "email", "subject", "message"])
        name = data.get("name", "")
        email = data.get("email", "")
        subject = data.get("subject", "")
        message = data.get("message", "")
        csv_writer.writerow([name, email, subject, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
          data = request.form.to_dict()
          write_to_csv(data)
          return redirect("/thankyou.html")
        except:
            return 'Did not save to database'
    else:
        return 'something went wrong. Try again!'
