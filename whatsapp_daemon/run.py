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

from custom_asyncore_connection_dispatcher import CustomAsyncoreConnectionDispatcher
import inspect


# NOTE: decorator used to thread methods
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper


def __custom_create_dispatcher(self, dispatcher_type):
    print('INSIDE __custom_create_dispatcher')
    if dispatcher_type == self.DISPATCHER_ASYNCORE:
        logger.debug("Created asyncore dispatcher")
        return CustomAsyncoreConnectionDispatcher(self)
    else:
        logger.debug("Created socket dispatcher")
        return CustomSocketConnectionDispatcher(self)


class YowsupDaemonStack(object):
    def __init__(self, profile, line):
        stackBuilder = YowStackBuilder()

        # TODO: checkif instantiation works, else return to old way
        self.whatsapp_daemon_layer = WhatsappDaemonLayer(line)

        # custom_connect = inspect.getsource(YowNetworkLayer)
        # print('<--------------------------------------------------->')
        # print('custom_connect --------------------->', custom_connect)
        # print('<--------------------------------------------------->')

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(self.whatsapp_daemon_layer)\
            .build()

        self._stack.setProfile(profile)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    # @threaded
    def start(self):
        print('Starting Yowsup daemon stack...')
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        # TODO: check if it works fine without the following line
        # self._stack.loop()

@threaded
def stacksLauncher(profiles_collection, stacks_collection):
    """Start one stack per whatsapp registered line
    :param profiles_collection: collection of yowsup profiles
    :type profiles_collection: collection of yowsup profiles
    :param stacks_collection: collection of yowsup stacks
    :type stacks_collection: collection of yowsup stacks
    """
    for profile in profiles_collection:
        stacks_collection[profile] = YowsupDaemonStack(profiles_collection[profile]['profile'], profiles_collection[profile]['line'])
        # stacks_collection[profile]['daemon_thread'] = stacks_collection[profile]['stack'].start()
        # stacks_collection[profile].broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        stacks_collection[profile].start()
    import asyncore
    asyncore.loop(timeout=1)

def startDaemon():
    # config_manager = ConfigManager()
    smsc_requests_handler = SMSCRequestsHandler()
    # TODO: when @pablorsk implements whatsapp in smsc API, get numbers and config from API
    # TODO: get numbers and config from SMSC API)
    # _config_phone = '542604268467'
    # _config = config_manager.load_path('whatsapp_daemon/config/542604268467.json')
    # _profile = YowProfile(_config_phone, _config)
    # NOTE: do not remove following line with no reason (tgalal added it to his demos)
    # _layer_network_dispatcher = None
    # NOTE: do not move stacks_collection to stacksLauncher (it is used later in this function)
    stacks_collection = {}

    try:
        profiles_collection = smsc_requests_handler.getLinesCollection()
        if not profiles_collection:
            return
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

        print('stacks_collection --->', stacks_collection)
        print(whatsapp_daemon_thread.is_alive())
        time.sleep(15)
        launch_time = time.time()
        while True:
            try:
                time.sleep(5)

                # NOTE: this code stops the app after one hour
                run_time = time.time() - launch_time
                if run_time >= 3600:
                    print("\nYowsdown")
                    sys.exit(0)

                if smsc_requests_handler.busy:
                    print("I'm still sending messages from the last request... wait a minute!")
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
                            line = receipt.relationships['line']['data'].id
                            # @TESTING: the next line replaces the line that should send the message with hardcoded number (testing)
                            # line = '542604268467'
                            print('BEFORE searching line')
                            print('stacks collection')
                            for each_line in stacks_collection:
                                print('line:', each_line)
                                print('each_line:', each_line)
                                print('stacks_collection:', stacks_collection)
                            stack = stacks_collection[line]
                            print('AFTER searching line')
                            sent_message = stack.whatsapp_daemon_layer.sendTextMessage(
                                # @TESTING: uncomment following line and comment next for testing
                                # '5492604332205',
                                "%s%s%s" %(cc, prefijo, fijo),
                                message
                            )
                            print(sent_message)
                            if sent_message:
                                print('Mensaje enviado, actualizando estado en SMSC...')
                                saved_sent_message = smsc_requests_handler.saveSentReceipt(receipt)
                                if saved_sent_message:
                                    print('Succesfully updated receipt!')
                                else:
                                    print('ERROR: Failed to update sent receipt in SMSC!')
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
    YowNetworkLayer.__create_dispatcher = __custom_create_dispatcher
    startDaemon()
