from whatsapp_daemon.smsc import SMSCClass


class SMSCRecievedMessage(SMSCClass):
    """SMSC Recieved Message implementation.
    :param from: the number that sent the message
    :type from: number
    :param text: the text sent in the message
    :type text: str
    """

    # TODO: remove hardcoded relationship when bask end supports lines
    relationships = {
        'line': {
            'type': 'lines',
            'id': '1'
        }
    }
    type = 'received_messages'

    # TODO: from is really to... tawk with @pablorsk
    def __init__(self, from_number, text):
        self.attributes['from'] = from_number
        self.attributes['text'] = text
