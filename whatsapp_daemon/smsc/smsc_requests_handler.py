import requests
import json
import datetime
import time
from whatsapp_daemon.smsc import SMSCReceipt, SMSCNumber, SMSCMessage, SMSCRecievedMessage
from yowsup.config.manager import ConfigManager
from yowsup.profile.profile import YowProfile

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
    internal_key = 'TBNiK0IsGYqDrbZiVCz1'
    busy = False

    def getUnsentReceipts(self):
        try:
            self.busy = True
            """Get unsent messages from the API."""
            date = datetime.date.today()
            formatted_date = date.strftime("%Y/%m/%d")
            print(formatted_date, 'formatted_date')
            url = self.api_url + "/receipts?include=message,number&filter[enviado]=0&filter[message.method]=whatsapp&filter[message.fecha][until]=%s&internal_key=%s" %(str(formatted_date), str(self.internal_key))
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

    def saveSentReceipt(self, receipt):
        """Save a sent message to the API.
        Args:
        message (SMSCMessage): an instance of SMSCMessage to save to the API
        """
        try:
            success = True
            receipt.attributes['enviado'] = 20
            sent_receipt_url = self.api_url + "/receipts?internal_key=%s" %(str(self.internal_key))
            raw_sent_receipt = requests.patch(sent_receipt_url, receipt.__dict__, headers=self.headers)
            print(raw_sent_receipt.status_code)
            if raw_sent_receipt.status_code == 200:
                print('Updated sent receipt in SMSC!')
            else:
                success = False
                print('ERROR: Failed to update sent receipt in SMSC!')

            # TODO: get cc form API when it is suppported and add it tho the phone_number
            cc = '549'
            prefijo = receipt.relationships['number']['data'].attributes['prefijo']
            fijo = receipt.relationships['number']['data'].attributes['fijo']
            phone_number = "%s%s" %(prefijo, fijo)
            message = receipt.relationships['message']['data'].attributes['text']
            recieved_message = SMSCRecievedMessage(phone_number, message)
            recieved_message_url = self.api_url + "/received_messages?internal_key=%s" %(str(self.internal_key))
            raw_recieved_message = requests.post(recieved_message_url, recieved_message.__dict__, headers=self.headers)
            print(raw_recieved_message.status_code)
            if raw_recieved_message.status_code == 200:
                print('Saved recieved message in SMSC!')
            else:
                success = False
                print('ERROR: Failed to save recieved message in SMSC!')

        except Exception as e:
            success = False
            print('ERROR: Could not update sent resources in SMSC')
            print(e)

        return success
        # TODO: return confiramtion code of the request status and add to method documentation

    def getNumberConfig(self, number):
        # TODO: check the posiibility to store axolotl.db file in a server to avoid "IcorrectMessage or KeyId ERROR in Yowsup" when using in other PC
        url = self.api_url + "/whatsapp/%s/config" %(str(phone_number))
        raw_config = requests.get(url, headers=self.headers)
        config_json = raw_config.json()
        print('config_json: ', config_json)
        # TODO: return configuration for the passed number and add to method documentation

    def getLinesCollection(self):
        config_manager = ConfigManager()
        # TODO: get lines from SMSC API
        phone_number = '542604268467'
        config = config_manager.load_path('whatsapp_daemon/config/542604268467.json')
        profiles_collection = {}
        profiles_collection[phone_number] = YowProfile(phone_number, config)

        return profiles_collection
