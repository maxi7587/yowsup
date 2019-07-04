import requests
import json
from datetime import datetime
import pytz
import time
import urllib # by pablorsk
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
            date = datetime.now(pytz.utc)
            formatted_date = date.strftime("%Y-%m-%dT%H:%M:%S%z")

            ## change, by pablorsk, read please
            formatted_date = urllib.quote_plus(formatted_date) # by pablorsk
            ##>>> f = { 'eventName' : 'myEvent', 'eventDescription' : 'cool event'}
            ## >>> urllib.urlencode(f)
            ## 'eventName=myEvent&eventDescription=cool+event'

            url = self.api_url + "/receipts?include=message,number,line&filter[enviado][lt]=5&filter[message.method]=whatsapp&filter[message.fecha][until]=%s&internal_key=%s" %(str(formatted_date), str(self.internal_key))
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
            lines_dict = {}
            receipts_list = []

            # If there are no messages, log info and return
            if len(messages_json['data']) == 0:
                print('No new messages to send.')
                return receipts_list;

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
                # Format lines
                if include['type'] == 'lines':
                    smsc_line = SMSCLine(**include['attributes'])
                    smsc_line.id = include['id']
                    lines_dict[smsc_line.id] = smsc_line

            # Extract receipts
            for receipt in messages_json['data']:
                if receipt['attributes']['enviado'] == 20:
                    continue

                # Fix to receipts without line
                if receipt['relationships']['line']['data'] == None:
                    print('Invalid data recieved in receipt ', receipt['id'])
                    continue
                # Format receipts
                smsc_receipt = SMSCReceipt(**receipt['attributes'])
                smsc_receipt.id = receipt['id']
                smsc_receipt.addRelationship(numbers_dict[receipt['relationships']['number']['data']['id']], 'number')
                smsc_receipt.addRelationship(messages_dict[receipt['relationships']['message']['data']['id']], 'message')
                smsc_receipt.addRelationship(lines_dict[receipt['relationships']['line']['data']['id']], 'line')
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
            if raw_sent_receipt.status_code == 200:
                print('Updated sent receipt in SMSC!')
            else:
                success = False

        except Exception as e:
            success = False
            print('ERROR: Could not update sent resources in SMSC')
            print(e)

        return success
        # TODO: return confiramtion code of the request status and add to method documentation

    def getLinesCollection(self):
        profiles_collection = {}

        try:
            config_manager = ConfigManager()

            # Get lines from SMSC API
            lines_url = self.api_url + "/lines?include=number&filter[whatsapp_config][ne]=&internal_key=%s&page[size]=100" %(str(self.internal_key))
            raw_lines = requests.get(lines_url, headers=self.headers)
            print('Lines response code:', raw_lines.status_code)
            print('Lines response content:', raw_lines.content)
            lines_json = raw_lines.json()

            if len(lines_json['data']) == 0:
                print('Any number can send messages through whatsapp...')
                return profiles_collection;

            included = lines_json['included']
            lines_data = lines_json['data']

            # TODO: uncomment and complete when api supports pagination
            # page = lines_json['meta']['page']
            # resources_per_page = lines_json['meta']['resources_per_page']
            # total_resources = lines_json['meta']['total_resources']

            # while total_resources > resources_per_page:
            #     lines_url = self.api_url + "/lines?include=number&filter[whatsapp_config][ne]=&internal_key=%s&page[number]=" %(str(self.internal_key), str())
            #     raw_lines = requests.get(lines_url, headers=self.headers)
            #     print('Lines response code:', raw_lines.status_code)
            #     print('Lines response content:', raw_lines.content)
            #     lines_json = raw_lines.json()
            #
            #     page = lines_json['meta']['page']
            #     resources_per_page = lines_json['meta']['resources_per_page']
            #     total_resources = lines_json['meta']['total_resources']


            # instance lines and numbers
            numbers_dict = {}
            for include in included:
                # Format numbers
                if include['type'] == 'numbers':
                    smsc_number = SMSCNumber(**include['attributes'])
                    smsc_number.id = include['id']
                    numbers_dict[smsc_number.id] = smsc_number

            # Extract lines
            for line in lines_data:
                # search lines that have whatsapp_config attributes set
                if line['attributes']['whatsapp_config'] == '':
                    print('NO WHATSAPP CONFIG FOR THIS NUMBER...')
                    continue
                smsc_line = SMSCLine(**line['attributes'])
                smsc_line.id = line['id']
                print("---------------line['id']--------------")
                print(line['id'])
                print("---------------------------------------")
                smsc_line.addRelationship(numbers_dict[line['relationships']['number']['data']['id']], 'number')
                phone_number = '549' + str(smsc_line.relationships['number']['data'].attributes['prefijo']) + str(smsc_line.relationships['number']['data'].attributes['fijo'])
                config_file_path = 'whatsapp_daemon/config/' + phone_number + '.json'
                with open(config_file_path, 'w+') as config_file:
                    config_file.write(smsc_line.attributes['whatsapp_config'])
                config = config_manager.load(config_file_path)
                profiles_collection[smsc_line.id] = {
                    'profile': YowProfile(phone_number, config),
                    'line': smsc_line
                }

            # @testing: following group of lines are for testing with personal number (uncomment for testing)
            # profiles_collection = {}
            # config = config_manager.load('whatsapp_daemon/config/542604268467.json')
            # smsc_number = SMSCNumber(**{'prefijo': '260', 'fijo': '4268467' })
            # smsc_line = SMSCLine(**{'numero': '268467', 'whatsapp_config': ''})
            # smsc_line.id = '268467'
            # smsc_line.addRelationship(smsc_number, 'number')
            # phone_number = '54' + smsc_number.attributes['prefijo'] + smsc_number.attributes['fijo']
            # profiles_collection[phone_number] = {
            #     'profile': YowProfile(phone_number, config),
            #     'line': smsc_line
            # }

            return profiles_collection

        except Exception as e:
            print('ERROR: could not fetch lines from SMSC API')
            print(e)
            return profiles_collection


    def saveReceivedMessage(self, received_message):
        try:
            received_message_json = json.dumps({'data': received_message.toServer()})
            received_message_url = self.api_url + "/received_messages?internal_key=%s" %(str(self.internal_key))
            raw_received_message = requests.post(received_message_url, received_message_json, headers=self.headers)
            print(raw_received_message.status_code)
            if raw_received_message.status_code == 201:
                print('Saved received message in SMSC!')
            else:
                print('ERROR: Failed to save received message in SMSC!')

        except Exception as e:
            print('ERROR: could not save received message to SMSC')
            print(e)
