from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_profiles.protocolentities  import SetStatusIqProtocolEntity
from yowsup.layers.protocol_presence.protocolentities.presence import PresenceProtocolEntity
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from whatsapp_daemon.smsc                              import SMSCMessage, SMSCReceivedMessage, SMSCRequestsHandler
from yowsup.common.tools import Jid


class WhatsappDaemonLayer(YowInterfaceLayer):

    def __init__(self, line):
        YowInterfaceLayer.__init__(self)
        self.connected = False
        self.smscRequestsHandler = SMSCRequestsHandler()
        self.line = line

    def setPresenceName(self, name):
        if self.assertConnected():
            entity = PresenceProtocolEntity(name = name)
            self.toLower(entity)

    def setProfileStatus(self, text):
        if self.assertConnected():

            def onSuccess(resultIqEntity, originalIqEntity):
                print('Status updated successfully')

            def onError(errorIqEntity, originalIqEntity):
                print('ERROR: Error updating status')

            entity = SetStatusIqProtocolEntity(text)
            self._sendIq(entity, onSuccess, onError)

    def sendTextMessage(self, number, content):
        if self.assertConnected():
            try:
                outgoingMessage = TextMessageProtocolEntity(content, to=self.aliasToJid(number))
                print('outgoingMessage -------------------->', outgoingMessage.__dict__)
                self.toLower(outgoingMessage)
                return True
            except Exception as e:
                print('ERROR: Could not send message to %s' %(number))
                return False
        else:
            return False

    def assertConnected(self):
        if self.connected:
            return True
        else:
            print('ERROR: NOT CONNECTED')
            # TODO: when smsc API is ready, set message as failed and save to API
            return False

    def aliasToJid(self, calias):
        return Jid.normalize(calias)

    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        self.connected = True
        self.setPresenceName('SMSC')
        self.setProfileStatus('Sistema SMSC')
        print('-----------------------------------------------')
        print('------------------ onSuccess END ------------------')
        print('-----------------------------------------------')

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)

            message_time = str(messageProtocolEntity.getTimestamp())
            message_body = messageProtocolEntity.getBody()
            message_from = messageProtocolEntity.getFrom().split('@')[0]
            stack = self.getStack()
            profile = stack.getProp('profile')
            username = profile.username

            smsc_received_message = SMSCReceivedMessage(message_from, message_body)
            smsc_received_message.addRelationship(self.line, 'line')
            self.smscRequestsHandler.saveReceivedMessage(smsc_received_message)

        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        # @TESTING: uncomment following line to enable ECHO (for testing)
        # self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        # TODO: use this method to check if messages were received and save to API
        print('inside onReceipt method entity', entity.__dict__)
        print('inside onReceipt method self', self.__dict__)
        self.toLower(entity.ack())

    # NOTE: following method is just to check ECHO works
    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    # NOTE: following method is just to check ECHO works
    def onMediaMessage(self, messageProtocolEntity):
        print('received media', messageProtocolEntity.__dict__)
        # just print info
        if messageProtocolEntity.media_type == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "contact":
            print("Echoing contact (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
