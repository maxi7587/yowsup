from whatsapp_daemon.smsc import SMSCClass


class SMSCRecievedMessages(SMSCClass):
    """SMSC Receipt implementation.
    :param from: the number that sent the message
    :type from: number
    :param text: the text sent in the message
    :type text: str
    """

    type = 'lines'

    def __init__(self):
