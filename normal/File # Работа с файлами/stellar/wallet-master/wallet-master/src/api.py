import json
import os

from flask import Flask
from flask import request
from flask import make_response

from pywallet import wallet

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    req_dist = json.loads(request.data)
    print(req_dist)

    intent = req_dist['queryResult']['intent']['displayName']

    if intent == 'ถามหนังน่ารดู'
        speech = 'ได้เลย'
    else:
        speech = "ผมไม่เข้าใจ คุณต้องการอะไร"

    res = makeWebhookResult(speech)
    return res


def makeWebhookResult(speech):

    return {
        "fulfillmentText": speech
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
