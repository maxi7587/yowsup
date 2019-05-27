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

    def __init__( self, cc, client_static_keypair, expid, fdid, id, mcc, mnc, phone, server_static_public, sim_mcc, sim_mnc, login):
        # self.from = phone_number_from
        self.__version__ = 1
        self.cc = cc
        self.client_static_keypair = client_static_keypair
        self.expid = expid
        self.fdid = fdid
        self.id = id
        self.mcc = mcc
        self.mnc = mnc
        self.phone = phone
        self.server_static_public = server_static_public
        self.sim_mcc = sim_mcc
        self.sim_mnc = sim_mnc
        self.login = login

    def setCc(self, cc):
        """Sets the cc for this number"""
        self.cc = cc
    def setClientStaticKeypair(self, client_static_keypair):
        """Sets the client_static_keypair for this number"""
        self.client_static_keypair = client_static_keypair
    def setExpid(self, expid):
        """Sets the expid for this number"""
        self.expid = expid
    def setFdid(self, fdid):
        """Sets the fdid for this number"""
        self.fdid = fdid
    def setId(self, id):
        """Sets the id for this number"""
        self.id = id
    def setMcc(self, mcc):
        """Sets the mcc for this number"""
        self.mcc = mcc
    def setMnc(self, mnc):
        """Sets the mnc for this number"""
        self.mnc = mnc
    def setPhone(self, phone):
        """Sets the phone for this number"""
        self.phone = phone
    def setServerStaticPublic(self, server_static_public):
        """Sets the server_static_public for this number"""
        self.server_static_public = server_static_public
    def setSimMcc(self, sim_mcc):
        """Sets the sim_mcc for this number"""
        self.sim_mcc = sim_mcc
    def setSimMnc(self, sim_mnc):
        """Sets the sim_mnc for this number"""
        self.sim_mnc = sim_mnc
    def setLogin(self, login):
        """Sets the login for this number"""
        self.login = login
