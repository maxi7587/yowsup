from whatsapp_daemon.smsc import SMSCClass


class SMSCLine(SMSCClass):
    """SMSC Receipt implementation.
    :param numero: the id of the number that sent the message
    :type numero: string
    :param whatsapp_config: whatsapp configuration json (as string) for this line
    :type whatsapp_config: str
    """

    type = 'lines'

    def __init__(self, numero, whatsapp_config):
        SMSCClass.__init__(self)
        self.attributes['numero'] = numero
        self.attributes['whatsapp_config'] = whatsapp_config
        self.relationships = {
            'number': {}
        }
