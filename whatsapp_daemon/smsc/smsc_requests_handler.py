import requests
import json
import datetime
import time
from whatsapp_daemon.smsc import SMSCReceipt, SMSCNumber, SMSCMessage, SMSCReceivedMessage, SMSCLine
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
            print('will GET receipts from URL: ', url)
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
                print('include --->', include)
                if include['type'] == 'numbers':
                    smsc_number = SMSCNumber(**include['attributes'])
                    smsc_number.id = include['id']
                    numbers_dict[smsc_number.id] = smsc_number
                    print('number attributes --->', smsc_number.attributes)
                # Format messages
                if include['type'] == 'messages':
                    smsc_message = SMSCMessage(**include['attributes'])
                    smsc_message.id = include['id']
                    messages_dict[smsc_message.id] = smsc_message
                # Format lines
                if include['type'] == 'lines':
                    smsc_line = SMSCLine(**include['attributes'])
                    smsc_line.id = include['id']
                    lines_dict[smsc_line.id] = smsc_line

            # Extract receipts
            for receipt in messages_json['data']:
                if receipt['attributes']['enviado'] == 20:
                    continue
                # Format receipts
                smsc_receipt = SMSCReceipt(**receipt['attributes'])
                smsc_receipt.id = receipt['id']
                smsc_receipt.addRelationship(numbers_dict[receipt['relationships']['number']['data']['id']], 'number')
                smsc_receipt.addRelationship(messages_dict[receipt['relationships']['message']['data']['id']], 'message')
                receipts_list.append(smsc_receipt)

            if len(receipts_list) == 0:
                print('No new messages to send.')

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
            sent_receipt_url = self.api_url + "/receipts/%s?internal_key=%s" %(str(receipt.id), str(self.internal_key))
            receipt_json = json.dumps({'data': receipt.toServer()})
            raw_sent_receipt = requests.patch(sent_receipt_url, receipt_json, headers=self.headers)
            print(raw_sent_receipt.status_code)
            sent_receipt_response = raw_sent_receipt.content
            print('-----------sent_receipt_response-------------')
            print(sent_receipt_response)
            print('---------------------------------------------')
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
            received_message = SMSCReceivedMessage(phone_number, message)
            received_message_json = json.dumps({'data': received_message.toServer()})
            received_message_url = self.api_url + "/received_messages?internal_key=%s" %(str(self.internal_key))
            raw_received_message = requests.post(received_message_url, received_message_json, headers=self.headers)
            print(raw_received_message.status_code)
            if raw_received_message.status_code == 200:
                print('Saved received message in SMSC!')
            else:
                success = False
                print('ERROR: Failed to save received message in SMSC!')

        except Exception as e:
            success = False
            print('ERROR: Could not update sent resources in SMSC')
            print(e)

        return success
        # TODO: return confiramtion code of the request status and add to method documentation

    def getLinesCollection(self):
        config_manager = ConfigManager()

        # Get lines from SMSC API
        lines_url = self.api_url + "/lines?include=number&internal_key=%s" %(str(self.internal_key))
        raw_lines = requests.get(lines_url, headers=self.headers)
        lines_json = raw_lines.json()

        # instance lines and numbers
        numbers_dict = {}
        for include in lines_json['included']:
            # Format numbers
            print('include --->', include)
            if include['type'] == 'numbers':
                smsc_number = SMSCNumber(**include['attributes'])
                smsc_number.id = include['id']
                numbers_dict[smsc_number.id] = smsc_number

        # Extract lines
        for line in lines_json['data']:
            # search lines that have whatsapp_config attributes set
            if line['attributes']['whatsapp_config'] == '':
                continue
            smsc_line = SMSCLine(**line['attributes'])
            smsc_line.id = line['id']
            smsc_line.addRelationship(numbers_dict[line['relationships']['number']['data']['id']], 'number')
            phone_number = '549' + smsc_line.relationships['number'].attributes['prefijo'] + smsc_line.relationships['number'].attributes['fijo']
            config_file_path = 'whatsapp_daemon/config/' + phone_number + '.json'
            with open(config_file_path, 'w+') as config_file:
                config_file.write(line['whatsapp_config'])
            config = config_manager.load_path(config_file_path)
            profiles_collection[phone_number] = YowProfile(phone_number, config)

        # TODO: following 4 lines are for testing with personal number (comment or remove them)
        phone_number = '542604268467'
        config = config_manager.load_path('whatsapp_daemon/config/542604268467.json')
        profiles_collection = {}
        profiles_collection[phone_number] = YowProfile(phone_number, config)

        return profiles_collection
