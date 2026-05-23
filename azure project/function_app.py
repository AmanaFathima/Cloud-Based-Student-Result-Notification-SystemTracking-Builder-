import logging
import azure.functions as func
import csv
import io
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ResultTrigger")
def ResultTrigger(req: func.HttpRequest) -> func.HttpResponse:

    try:
        csv_data = """
name,email,marks,result
Rahul,rahul@gmail.com,88,Pass
Anu,anu@gmail.com,92,Pass
"""
        csv_reader = csv.DictReader(io.StringIO(csv_data.strip()))

        SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
        SENDER_EMAIL     = os.environ["amanafathimaek23@gmail.com"]      # ← fixed

        sg = SendGridAPIClient(SENDGRID_API_KEY)

        sent = []

        for row in csv_reader:
            message = Mail(
                from_email   = amanafathimaek23@gmail.com,               # ← fixed
                to_emails    = row['email'],
                subject      = 'Exam Result Notification',
                html_content = f"""
                    Hello {row['name']},<br><br>
                    Your result has been published.<br><br>
                    Marks: {row['marks']}<br>
                    Result: {row['result']}<br><br>
                    Regards,<br>
                    Examination Cell
                """
            )
            sg.send(message)
            sent.append(row['name'])
            logging.info(f"Email sent to {row['name']} at {row['email']}")

        return func.HttpResponse(f"Emails sent to: {', '.join(sent)}")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)