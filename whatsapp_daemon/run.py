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

    @threaded
    def start(self):
        print('inside start begin')
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()


def startDaemon():
    config_manager = ConfigManager()
    # TODO: when @pablorsk implements whatsapp in smsc API, get numbers and config from API
    # TODO: add support for multiple numbers (get them from SMSC API)
    _config_phone = '542604268467'
    _config = config_manager.load_path('whatsapp_daemon/config/542604268467.json')
    _profile = YowProfile(_config_phone, _config)
    # NOTE: do not remove following line with no reason (tgalal added it to his demos)
    # _layer_network_dispatcher = None
    stacks_list = []
    # TODO: get lines from SMSC API
    lines = ['542604268467']

    try:
        smsc_requests_handler = SMSCRequestsHandler()
        stack = YowsupDaemonStack(_profile)
        # NOTE: do not remove following 2 lines with no reason (tgalal addedthem to his demos)
        # if _layer_network_dispatcher is not None:
        #     stack.set_prop(YowNetworkLayer.PROP_DISPATCHER, _layer_network_dispatcher)

        # TODO: UNCOMMENT folowing three lines
        # whatsapp_daemon_thread = threading.Thread(target=stack.start)
        # whatsapp_daemon_thread.start()

        # print(whatsapp_daemon_thread.is_alive())
        while True:
            try:
                time.sleep(5)
                if smsc_requests_handler.busy:
                    print("I'm still sending messges from the last request... wait a minute!")
                else:
                    unsent_receipts = smsc_requests_handler.getUnsentReceipts()
                    try:
                        print('Sending messages...')
                        for receipt in unsent_receipts:
                            # wait a random amount of time between messages to avoid whatsapp blocks
                            # TODO: add country code to numbers resource
                            cc = '549'
                            print('cc', cc)
                            prefijo = receipt.relationships['number']['data'].attributes['prefijo']
                            print('prefijo', prefijo)
                            fijo = receipt.relationships['number']['data'].attributes['prefijo']
                            print('fijo', fijo)
                            message = receipt.relationships['message']['data'].attributes['text']
                            stack.whatsapp_daemon_layer.sendTextMessage(
                                # remove following line and uncomment next
                                '5492604332205',
                                # "%s%s%s" %(cc, prefijo, fijo),
                                message
                            )
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
