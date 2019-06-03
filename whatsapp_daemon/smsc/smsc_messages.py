from whatsapp_daemon.smsc import SMSCClass


class SMSCMessage(SMSCClass):
    """SMSC Message implementation.
    :param date: the date of the message
    :type date: str
    :param fecha: the fecha of the messge
    :type fecha: str
    :param text: the text to be sent
    :type text: str
    :param priority: tiemstamp priority of the message
    :type priority: number
    """

    type = 'messages'

    def __init__(self, date, fecha, text, method, priority):
        SMSCClass.__init__(self)
        self.attributes['date'] = date
        self.attributes['fecha'] = fecha
        self.attributes['text'] = text
        self.attributes['method'] = method
        self.attributes['priority'] = priority
