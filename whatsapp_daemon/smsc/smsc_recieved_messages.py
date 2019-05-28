from whatsapp_daemon.smsc import SMSCClass


class SMSCRecievedMessage(SMSCClass):
    """SMSC Recieved Message implementation.
    :param from: the number that sent the message
    :type from: number
    :param text: the text sent in the message
    :type text: str
    """

    relationships = {
        'line': {}
    }
    type = 'receipts'

    def __init__(self, from_number, text):
        self.attributes['from'] = from_number
        self.attributes.text = text
