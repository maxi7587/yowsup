class SMSCMessage(object):
    """SMSC Message implementation.
    Init args:
    phone_number_from (str): the number that is sending the message
    phone_number_to (str): the number that will recieve the messge
    message (str): the message to be sent
    timestamp (number): tiemstamp of the last status update
    status (str): message status ('sent', 'unsent', 'failed', 'recieved')
    status_details (str): used to store details regarding the message's status
    """

    def __init__(self, phone_number_from, phone_number_to, message, timestamp, status, status_details):
        # self.from = phone_number_from
        self.from_number = phone_number_from
        self.to_number = phone_number_to
        self.message = message
        self.timestamp = timestamp
        self.status = status
        self.status_details = status_details

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
