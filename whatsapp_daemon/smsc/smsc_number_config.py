class SMSCNumberConfig(object):
    """SMSC Number configuration for yowsup.
    :param cc: this number's cc config data
    :type cc: string
    :param client_static_keypair: this number's client_static_keypair config data
    :type client_static_keypair: string
    :param expid: this number's expid config data
    :type expid: string
    :param fdid: this number's fdid config data
    :type fdid: string
    :param id: this number's id config data
    :type id: string
    :param mcc: this number's mcc config data
    :type mcc: string
    :param mnc: this number's mnc config data
    :type mnc: string
    :param phone: this number's phone config data
    :type phone: string
    :param server_static_public: this number's server_static_public config data
    :type server_static_public: string
    :param sim_mcc: this number's sim_mcc config data
    :type sim_mcc: string
    :param sim_mnc: this number's sim_mnc config data
    :type sim_mnc: string
    :param login: this number's login config data
    :type login: string
    """

    def __init__( self, cc, client_static_keypair, expid, fdid, id, mcc, mnc, phone, server_static_public, sim_mcc, sim_mnc, login, **kwargs):
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
