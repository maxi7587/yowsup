from yowsup.stacks import  YowStackBuilder
from layer import WhatsappDaemonLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.config.manager import ConfigManager
from yowsup.profile.profile import YowProfile
import sys
import json
import threading
import time
from whatsapp_daemon.smsc import SMSCRequestsHandler
from random import randint


# NOTE: decorator used to thread methods
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper


class YowsupDaemonStack(object):
    def __init__(self, profile):
        stackBuilder = YowStackBuilder()

        # TODO: checkif instantiation works, else return to old way
        self.whatsapp_daemon_layer = WhatsappDaemonLayer()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(self.whatsapp_daemon_layer)\
            .build()

        self._stack.setProfile(profile)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    # @threaded
    def start(self):
        print('inside start begin')
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        # TODO: check if it works fine without the following line
        # self._stack.loop()

@threaded
def stacksLauncher(profiles_collection, stacks_collection):
    """Start one stask per whatsapp registered line
    :param profiles_collection: collection of yowsup profiles
    :type profiles_collection: collection of yowsup profiles
    :param stacks_collection: collection of yowsup stacks
    :type stacks_collection: collection of yowsup stacks
    """
    for profile in profiles_collection:
        stacks_collection[profile] = YowsupDaemonStack(profiles_collection[profile])
        # stacks_collection[profile]['daemon_thread'] = stacks_collection[profile]['stack'].start()
        # stacks_collection[profile].broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        stacks_collection[profile].start()

def startDaemon():
    # config_manager = ConfigManager()
    smsc_requests_handler = SMSCRequestsHandler()
    # TODO: when @pablorsk implements whatsapp in smsc API, get numbers and config from API
    # TODO: add support for multiple numbers (get them from SMSC API)
    # _config_phone = '542604268467'
    # _config = config_manager.load_path('whatsapp_daemon/config/542604268467.json')
    # _profile = YowProfile(_config_phone, _config)
    # NOTE: do not remove following line with no reason (tgalal added it to his demos)
    # _layer_network_dispatcher = None
    stacks_collection = {}

    try:
        profiles_collection = smsc_requests_handler.getLinesCollection()
        # for profile in profile_collection:
        #     stacks_collection[profile]['stack'] = YowsupDaemonStack(profile_collection[profile])
        #     stacks_collection[profile]['daemon_thread'] = threading.Thread(target=stacks_collection[profile]['stack'].start)
        # for stack in stacks_collection:
        # whatsapp_daemon_thread = threading.Thread(target=stack.start)
        whatsapp_daemon_thread = threading.Thread(target=stacksLauncher, args=(profiles_collection, stacks_collection))
        whatsapp_daemon_thread.start()

        # NOTE: do not remove following 2 lines with no reason (tgalal addedthem to his demos)
        # if _layer_network_dispatcher is not None:
        #     stack.set_prop(YowNetworkLayer.PROP_DISPATCHER, _layer_network_dispatcher)

        # TODO: UNCOMMENT folowing three lines
        # whatsapp_daemon_thread = threading.Thread(target=stack.start)
        # whatsapp_daemon_thread.start()

        print(whatsapp_daemon_thread.is_alive())
        while True:
            print('inside while loop')
            try:
                time.sleep(5)
                if smsc_requests_handler.busy:
                    print("I'm still sending messges from the last request... wait a minute!")
                else:
                    unsent_receipts = smsc_requests_handler.getUnsentReceipts()
                    try:
                        print('Sending messages...')
                        for receipt in unsent_receipts:
                            # TODO: add country code to numbers resource
                            cc = '549'
                            prefijo = receipt.relationships['number']['data'].attributes['prefijo']
                            fijo = receipt.relationships['number']['data'].attributes['fijo']
                            message = receipt.relationships['message']['data'].attributes['text']
                            # TODO: replace hasrdcoded number for the line that should send the message
                            line = '542604268467'
                            stack = stacks_collection[line]
                            sent_message = stack.whatsapp_daemon_layer.sendTextMessage(
                                # TODO: remove following line and uncomment next
                                '5492604332205',
                                # "%s%s%s" %(cc, prefijo, fijo),
                                message
                            )
                            print(sent_message)
                            if sent_message:
                                print('Mensaje enviado, actualizando estado en SMSC...')
                                saved_sent_message = smsc_requests_handler.saveSentReceipt(receipt)
                                if saved_sent_message:
                                    print('Succesfully updated receipt and saved recieved message!')
                                else:
                                    print('ERROR: could not update receipt and/or save recieved message')
                            else:
                                print('No se pudo enviar el mansaje a %s%s%s' %(cc, prefijo, fijo))
                            # wait a random amount of time between messages to avoid whatsapp blocks
                            time.sleep(randint(4,9))

                        smsc_requests_handler.busy = False

                    except Exception as e:
                        smsc_requests_handler.busy = False
                        print('ERROR: Failed to send message...')
                        print e

                # TODO: when @pablorsk implements whatsapp in smsc API, use this loop to instantiate SMSCRequestsHandler and get messages to send from API
                # print(threading.enumerate())

                # TODO: remove following line, it's just for testing send method
                # stack.whatsapp_daemon_layer.sendTextMessage('5492604332205', 'Hola Maxi')
            except IOError:
                print('\nIOERror')
                pass #Gets thrown when we interrupt the join
    except KeyboardInterrupt:
        print("\nYowsdown")
        sys.exit(0)


if __name__==  "__main__":
    startDaemon()
