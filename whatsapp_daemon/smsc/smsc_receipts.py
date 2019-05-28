from whatsapp_daemon.smsc import SMSCClass


class SMSCReceipt(SMSCClass):
    """SMSC Receipt implementation.
    :param numero: the number of the receipt
    :type numero: number
    :param enviado: 0 if the receipt has not been sent, 20 if it has been sent
    :type enviado: number
    """

    relationships = {
        'message': {},
        'number': {}
    }
    type = 'receipts'

    def __init__(self, numero, enviado):
        self.attributes['numero'] = numero
        self.attributes['enviado'] = enviado
