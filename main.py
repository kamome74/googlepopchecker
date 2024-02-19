import google.cloud.logging
from google.oauth2 import service_account
from flask import Flask, render_template, request
import json
import airportsdata

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    sessionId = request.headers.get('X-Cloud-Trace-Context')
    return render_template('index.html', title="Home", isPost = False, XCloudTrace = sessionId )

@app.route("/", methods=["POST"])
def main_post():
    sessionId = request.form['XCloudTrace']

    projectId = "lgnet-ic-test-project"
    credential = service_account.Credentials.from_service_account_file('[Your Service Account JSON Credential]')
    filter = "resource.type=\"http_load_balancer\" AND trace=\"projects/[Your GCP Project ID]]/traces/" + sessionId + "\""

    client = google.cloud.logging.Client(project=projectId, credentials=credential)

    entry = list(client.list_entries(filter_=filter))

    if len(entry) == 0:
        return render_template('index.html', title="Home", isPost = True, isFound = False, XCloudTrace = sessionId )
    else:
        IATAcodes = airportsdata.load('IATA')
        popLocation = entry[0].payload["cacheId"].split("-")[0]

        payload = entry[0].payload
        payload["XCloudTrace"] = sessionId
        payload["agentId"] = entry[0].http_request["userAgent"]
        payload["popIATA"] = IATAcodes[popLocation]["city"] + ", " + IATAcodes[popLocation]["country"]
        return render_template('index.html', title="Home", isPost = True, isFound = True, result = payload)

if __name__ == "__main__":
    # This is used when running locally only.
    app.run(host="127.0.0.1", port=8080, debug=True)