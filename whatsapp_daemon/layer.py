from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity


class EchoLayer(YowInterfaceLayer):

    def sendTextMessage(self, target, body):
        print('send message')
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(body, target)
        self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)

            # Save messages to file
            with open('messages_recieved.txt', 'a+') as f:
                message_time = str(messageProtocolEntity.getTimestamp())
                message_body = messageProtocolEntity.getBody()
                message_from = messageProtocolEntity.getFrom()
                stack = self.getStack()
                profile = stack.getProp('profile')
                username = profile.username
                f.write(str('--- new message ---\n'))
                f.write(str(message_time) + '\n')
                f.write(str(message_body) + '\n')
                f.write(str(message_from) + '\n')
                f.write(str(username) + '\n')
                f.write(str('-------------------\n'))

        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.media_type == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "contact":
            print("Echoing contact (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
