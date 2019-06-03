class SMSCClass(object):
    """SMSC Class implementation.
    """

    def __init__(self):
        self.id = 0
        self.attributes = {}
        self.relationships = {}

    def setAttribute(self, attribute_name, attribute_value):
        self.attributes[attribute_name] = attribute_value
        return self

    def addRelationship(self, related_object, type):
        self.relationships[type]['data'] = related_object
        return self

    def toServer(self):
        print('attributes of ', type(self).__name__, self.attributes)
        return {
            'id': self.id,
            'type': self.type,
            'attributes': self.attributes,
            'relationships': self.formatRelationshipsToServer()
        }

    def formatRelationshipsToServer(self):
        relationships = {}
        for rel in self.relationships:
            print(rel)
            relationships[rel] = {'data': self.relationships[rel]['data'].toServer()}
            # fix because toServer method is assigning parent attributes
            print(relationships[rel])
        return relationships
