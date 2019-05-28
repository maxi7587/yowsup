from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from whatsapp_daemon.smsc                              import SMSCMessage
from yowsup.common.tools import Jid


class WhatsappDaemonLayer(YowInterfaceLayer):

    def sendTextMessage(self, number, content):
        if self.assertConnected():
            try:
                outgoingMessage = TextMessageProtocolEntity(content, to=self.aliasToJid(number))
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
            # smsc_message = SMSCMessage(
            #     message_from,
            #     username,
            #     message_body,
            #     message_time,
            #     'recieved',
            #     ''
            # )

            # print('smsc_message ---> ', smsc_message.__dict__)
            # TODO: when @pablorsk implements whatsapp in smsc API, instantiate SMSCRequestsHandler and save sent messages

        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        # TODO: actually, the app is making ECHO to check that it works, when everything works fine, comment the following line to disable ECHO
        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print('inside onReceipt method')
        self.toLower(entity.ack())

    # NOTE: following method is just to check ECHO works
    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    # NOTE: following method is just to check ECHO works
    def onMediaMessage(self, messageProtocolEntity):
        print('recieved media', messageProtocolEntity.__dict__)
        # just print info
        if messageProtocolEntity.media_type == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "contact":
            print("Echoing contact (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
