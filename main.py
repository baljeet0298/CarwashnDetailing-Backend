# The first step is always the same: import all necessary components:
from __future__ import print_function

import base64
import mimetypes
from email.message import EmailMessage

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://mail.google.com/']
import os
import pdfkit, json, datetime
from flask import Flask, render_template, request

app = Flask(__name__)
today = datetime.datetime.now().strftime("%m_%d_%Y");

filename = "members.json"
import pricelist
pricebook = pricelist.pricelist

non_negotiable_on_membership = ["Super Detailing", "Bike Ceramic Coating", "Ceramic Single Panel Coating",
                                "Ceramic Coating", "Paint Protection Film", "PPF Standard Kit", "Graphene Coating"]


@app.route('/')
def home():
    return render_template("create_invoice.html")


@app.route('/trial.html')
def home1():
    with open("members.json") as json_file:
        data = json.load(json_file)
    # print(data)
    return render_template("memberslist.html", data=data)


def take_membership(rg_number, total, vehicletype):
    with open(filename) as json_file:
        data = json.load(json_file)
        if rg_number in data.keys():
            ftotal = data[rg_number]["amount"] - total
            fdate = data[rg_number]["from"]
            to = data[rg_number]["to"]
        else:
            fdate = datetime.datetime.now().strftime("%m/%d/%Y")
            tdate = datetime.datetime.now() + datetime.timedelta(days=365)
            if vehicletype == 1:
                ftotal = 12000 - total
            elif vehicletype == 2:
                ftotal = 14000 - total
            elif vehicletype == 3:
                ftotal = 16000 - total

            to = tdate.strftime("%m/%d/%Y")
        y = {
            "amount": ftotal,
            "from": fdate,
            "to": to
        }
        data[rg_number] = y

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def getDiscount(total, discount):
    return total*(100-discount)/100


@app.route('/createinvoice', methods=["POST", "GET"])
def create_invoice():
    if request.method == 'POST':
        dis = 0 if request.form["discount"] == '' else int(request.form["discount"])
        war = 0 if request.form["warranty"] == '' else int(request.form["warranty"])
        data = {"Name": request.form["firstname"],

                "Vehicle Type": request.form["vehicletype"],
                "Email": request.form["email"],
                "Mobile": request.form["phone"],
                "City": request.form["city"],
                "Car Make": request.form["carmake"],
                "Car Model": request.form["carmodel"],
                "Registration Number": request.form["registrationnumber"],
                "Date": request.form["date"],
                "Delivery Date": request.form["deliverydate"],
                "Mudflap": request.form["mudflap"],
                "Service Taken": request.form.getlist("servicetaken"),
                "Accessories": request.form["accessories"],
                "discount": dis,
                "warranty": war,
                "Total": 0}
        vehicle_type = {"Small": 1, "Medium": 2, "Large": 3}
        membershipTaken = request.form["servicetype"]
        wantMembership = request.form["wantmembership"]
        pricelist = []
        total = 0
        index = vehicle_type[request.form["vehicletype"]]

        for i in request.form.getlist("servicetaken"):
            for j in pricebook:
                if j[0] == i:
                    if (membershipTaken == "Yes" or wantMembership == "Yes") and j[
                        index] >= 300 and i not in non_negotiable_on_membership:
                        rate = int(j[index] / 2);
                    else:
                        rate = j[index]
                    total = total + rate

                    an_item = dict(name=i, price=rate)
                    pricelist.append(an_item)
        total = getDiscount(total, dis)
        data["Service Taken"] = pricelist
        data["Total"] = total
        if wantMembership == "Yes" or membershipTaken == "Yes":
            take_membership(request.form["registrationnumber"], total, index)

        o = {
            "enable-local-file-access": ""
        }
        x = render_template("index2.html", data=data)
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(curr_dir)
        invoice_path = "Invoice/" + request.form["registrationnumber"]
        if not os.path.exists(invoice_path):
            #os.system(f"sudo mkdir {request.form['registrationnumber']}")
            os.mkdir(invoice_path)
        # print(x, invoice_path, today)
        config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        pdfkit.from_string(x, invoice_path + "/" + today + ".pdf", options=o,
                           configuration=config)

        # -------------------------main------------------------------------------------
        subject = "Car Wash N Detailing : Invoice"
        body = '''
Hello Sir/Madam,

Thank you for visiting Car Wash N Detailing, Jabalpur.
PFA.

For any query,
Get back to us at carwashndetailingjbp@gmail.com 
        '''

        sender_email = "carwashndetailingjbp@gmail.com"
        receiver_email = request.form["email"]
        password = "Sirat@2017"

        # Create a multipart message and set headers
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            service = build('gmail', 'v1', credentials=creds)
            message = EmailMessage()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message["Bcc"] = receiver_email  # Recommended for mass emails
            # Add body to email
            message.set_content(body)

            # message.attach(MIMEText(body, "html"))
            attachment_filename = invoice_path + "/" + today + ".pdf"  # In same directory as script
            # attachment_filename = r'C:\Users\Lenovo\PycharmProjects\carwashndetailing2\pricelist.py'
            # guessing the MIME type
            type_subtype, _ = mimetypes.guess_type(attachment_filename)
            maintype, subtype = type_subtype.split('/')

            with open(attachment_filename, 'rb') as fp:
                attachment_data = fp.read()
            message.add_attachment(attachment_data, maintype, subtype,  filename="invoice_carwashndetailing")

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            # encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

            create_message = {
                'raw': encoded_message
            }
            # pylint: disable=E1101
            send_message = (service.users().messages().send
                            (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None
        print(send_message)
        return render_template("./result.html")


if __name__ == '__main__':
    app.run(debug=True)
