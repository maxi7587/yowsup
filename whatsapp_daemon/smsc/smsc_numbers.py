from whatsapp_daemon.smsc import SMSCClass


class SMSCNumber(SMSCClass):
    """SMSC Number implementation.
    :param prefijo: the prefix of the number
    :type prefijo: str
    :param fijo: the fixed part of the number
    :type fijo: str
    """

    type = 'numbers'

    def __init__(self, prefijo, fijo):
        SMSCClass.__init__(self)
        print('attributes i number class', self.attributes)
        self.attributes['prefijo'] = prefijo
        self.attributes['fijo'] = fijo
