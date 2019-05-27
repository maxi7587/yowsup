import requests
import json


class SMSCRequestsHandler(object):
    """Requests handler for SMSC API
    Requires the file smsc-config.json in the config folder to be properly configured
    """

    def __init__(self):
        with open('./config/smsc-config.json', 'r') as config:
            config_json = json.read(config)
            self.token = config_json.token
            self.api_url = config_json.api_url
            self.headers = {
                'Authorization': self.token,
                'content-type': 'application/json'
            }

    def getUnsentMessages(self, phone_number):
        """Get unsent messages from the API.
        Args:
        phone_number (str/number): the whatsapp phone number to pull unsent messages from
        """
        url = self.api_url + "/whatsapp/%s/unsent_messages" %(str(phone_number))
        raw_messages = requests.get(url, headers=self.headers)
        messages_json = raw_messages.json()
        print('Request made. The response is:\n')
        print(raw_messages.status_code)
        print(messages_json)
        # TODO: return unsent messages in a list and add to method documentation

    def saveSentMessage(self, message):
        """Save a sent message to the API.
        Args:
        message (SMSCMessage): an instance of SMSCMessage to save to the API
        """

        url = self.api_url + "/whatsapp/%s/messages" %(str(phone_number))
        raw_sent_message = requests.patch(url, message.__dict__, headers=self.headers)
        # TODO: return confiramtion code of the request status and add to method documentation
