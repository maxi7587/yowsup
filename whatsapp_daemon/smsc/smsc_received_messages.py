from whatsapp_daemon.smsc import SMSCClass


class SMSCReceivedMessage(SMSCClass):
    """SMSC Received Message implementation.
    :param from: the number that sent the message
    :type from: number
    :param text: the text sent in the message
    :type text: str
    """

    # TODO: remove hardcoded relationship when bask end supports lines

    type = 'received_messages'

    # TODO: from is really to... tawk with @pablorsk
    def __init__(self, from_number, text, **kwargs):
        SMSCClass.__init__(self)
        self.attributes['from'] = from_number
        self.attributes['text'] = text
        self.attributes['method'] = 'whatsapp'
        # TODO: complete this code...
        self.relationships = {
            'line': {}
        }
