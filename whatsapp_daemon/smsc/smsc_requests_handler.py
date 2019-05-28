import requests
import json
import datetime
import time
from whatsapp_daemon.smsc import SMSCReceipt, SMSCNumber, SMSCMessage


class SMSCRequestsHandler(object):
    """Requests handler for SMSC API
    Requires the file smsc-config.json in the config folder to be properly configured
    :return receipts list:
    :type return list:
    """

    api_url = "https://api.smsc.com.ar/v1"
    headers = {
        # 'Authorization': self.token,
        'content-type': 'application/json'
    }
    busy = False

    def getUnsentReceipts(self):
        try:
            self.busy = True
            """Get unsent messages from the API."""
            date = datetime.date.today()
            formatted_date = date.strftime("%Y/%m/%d")
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
            # {u'numero': 1385, u'enviado': 1}, u'type': u'receipts', u'id': u'26331062', u'links': {u'self': u'/receipts/26331062'}}
            numbers_dict = {}
            messages_dict = {}
            receipts_list = []

            # If there are no messages, log info and return
            if len(messages_json['data']) == 0:
                print('No new messages to send.')
                return;

            # Extract includes
            for include in messages_json['included']:
                # Format numbers
                if include['type'] == 'numbers':
                    smsc_number = SMSCNumber(**include['attributes'])
                    smsc_number.id = include['id']
                    numbers_dict[smsc_number.id] = smsc_number
                # Format messages
                if include['type'] == 'messages':
                    smsc_message = SMSCMessage(**include['attributes'])
                    smsc_message.id = include['id']
                    messages_dict[smsc_message.id] = smsc_message

            # Extract receipts
            for receipt in messages_json['data']:
                # Format receipts
                smsc_receipt = SMSCReceipt(**receipt['attributes'])
                smsc_receipt.id = receipt['id']
                smsc_receipt.addRelationship(numbers_dict[receipt['relationships']['number']['data']['id']], 'number')
                smsc_receipt.addRelationship(messages_dict[receipt['relationships']['message']['data']['id']], 'message')
                receipts_list.append(smsc_receipt)

            return receipts_list


        except Exception as e:
            self.busy = False
            print('ERROR: could not fetch messages from SMSC API')
            print(e)
            return []

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
