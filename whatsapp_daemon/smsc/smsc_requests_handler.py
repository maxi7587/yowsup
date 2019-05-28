import requests
import json
import datetime


class SMSCRequestsHandler(object):
    """Requests handler for SMSC API
    Requires the file smsc-config.json in the config folder to be properly configured
    """

    api_url = "https://api.smsc.com.ar/v1"
    headers = {
        # 'Authorization': self.token,
        'content-type': 'application/json'
    }

    # def __init__(self):
    #     # with open('../config/smsc-config.json', 'r') as config:
    #     #     config_json = json.read(config)
    #     #     self.token = config_json.token
    #     #     self.api_url = config_json.api_url
    #     #     self.headers = {
    #     #         # 'Authorization': self.token,
    #     #         'content-type': 'application/json'
    #     #     }
    #     self.api_url = "https://api.smsc.com.ar/v1"
    #     self.headers = {
    #         # 'Authorization': self.token,
    #         'content-type': 'application/json'
    #     }

    def getUnsentReceipts(self, phone_number):
        """Get unsent messages from the API.
        Args:
        phone_number (str/number): the whatsapp phone number to pull unsent messages from
        """
        date = datetime.date.today()
        formatted_date = today_date.strftime("%Y/%m/%d")
        print(formatted_date, 'formatted_date')
        internal_key = 'TBNiK0IsGYqDrbZiVCz1'
        url = self.api_url + "/receipts?include=message,number&filter[enviado]=0&filter[message.method]=whatsapp&filter[message.fecha][until]=%s&internal_key=%s" %(str(formatted_date), str(internal_key))
        raw_messages = requests.get(url, headers=self.headers)
        messages_json = raw_messages.json()
        print('Request made. The response is:\n')
        print(raw_messages.status_code)
        print(messages_json)
        # TODO: parse messages_json to populate a list of SMSCMessage instances
        # TODO: return unsent messages in a list and add to method documentation

    def saveSentReceipt(self, message):
        """Save a sent message to the API.
        Args:
        message (SMSCMessage): an instance of SMSCMessage to save to the API
        """
        internal_key = 'TBNiK0IsGYqDrbZiVCz1'
        url = self.api_url + "/received_messages?internal_key=%s" %(str(internal_key))
        raw_sent_message = requests.patch(url, message.__dict__, headers=self.headers)
        # TODO: return confiramtion code of the request status and add to method documentation

    def getNumberConfig(self, number):
        # TODO: check the posiibility to store axolotl.db file in a server to avoid "IcorrectMessage or KeyId ERROR in Yowsup" when using in other PC
        url = self.api_url + "/whatsapp/%s/config" %(str(phone_number))
        raw_config = requests.get(url, headers=self.headers)
        config_json = raw_config.json()
        print('config_json: ', config_json)
        # TODO: return configuration for the passed number and add to method documentation
