class SMSCClass(object):
    """SMSC Class implementation.
    """

    id = 0
    attributes = {}
    relationships = {}

    def setAttribute(attribute_name, attribute_value):
        self.attributes[attribute_name] = attribute_value
        return self

    def addRelationship(self, related_object, type):
        this.relationships[type] = related_object
        return self
