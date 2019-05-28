class SMSCMessage(object):
    """SMSC Message implementation.
    :param phone_number_from: the number that is sending the message
    :type phone_number_from: str
    :phone_number_to: the number that will recieve the messge
    :type phone_number_to: str
    :message: the message to be sent
    :type messge: str
    :timestamp: tiemstamp of the last status update
    :type timestamp: number
    :status: message status ('sent', 'unsent', 'failed', 'recieved')
    :type status: str
    :status_details: used to store details regarding the message's status
    :type status_details: str
    """

    attributes = {}

    def __init__(self, phone_number_from, phone_number_to, message, timestamp, status, status_details):
        # self.from = phone_number_from
        self.attributes.from_number = phone_number_from
        self.attributes.to_number = phone_number_to
        self.attributes.message = message
        self.attributes.timestamp = timestamp
        self.attributes.status = status
        self.attributes.status_details = status_details

    def setFrom(self, phone_number_from):
        """Sets that is sending the message"""
        # self.from = phone_number_from
        self.from_number = phone_number_from

    def setTo(self, phone_number_to):
        """Sets that will recieve the message"""
        self.to_number = phone_number_to

    def setMessage(self, message):
        """Sets the body of the message"""
        self.message = message

    def setTimestamp(self, timestamp):
        """Sets the tiemstamp of the SMSCMessage instance"""
        self.timestamp = timestamp

    def setStatus(self, status):
        """Sets the status of the message ('sent', 'unsent', 'falied', 'recieved')"""
        self.status = status

    def setStatusDetails(self, status_details):
        """Sets details regarding the status of the message"""
        self.status_details = status_details
