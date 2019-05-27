from yowsup.stacks import  YowStackBuilder
from layer import WhatsappDaemonLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.config.manager import ConfigManager
from yowsup.profile.profile import YowProfile
import sys
import json
import threading


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
    # TODO: when @pablorsk implements whatsapp in smsc API, instantiate SMSCRequestsHandler and get messages to send from API
    # TODO: add support for multiple numbers
    _config_phone = '542604268467'
    _config = config_manager.load_path('whatsapp_daemon/config/542604268467.json')
    _profile = YowProfile(_config_phone, _config)
    # _layer_network_dispatcher = None
    # from yowsup.demos import whatsapp_daemonclient

    try:
        print('starting stack')
        stack = YowsupDaemonStack(_profile)
        # if _layer_network_dispatcher is not None:
        #     stack.set_prop(YowNetworkLayer.PROP_DISPATCHER, _layer_network_dispatcher)
        whatsapp_daemon_thread = threading.Thread(target=stack.start)
        whatsapp_daemon_thread.start()

        print(whatsapp_daemon_thread.is_alive())
        while True:
            try:
                import time
                time.sleep(3)
                print(threading.enumerate())
                stack.whatsapp_daemon_layer.sendTextMessage('5492604332205', 'Hola Maxi')
                # whatsapp_daemon_thread.stop()
            except IOError:
                print('\nIOERror')
                pass #Gets thrown when we interrupt the join
            # except KeyboardInterrupt:
            #     print("\nYowsdown")
            #     sys.exit(0)
    except KeyboardInterrupt:
        print("\nYowsdown")
        sys.exit(0)


if __name__==  "__main__":
    startDaemon()
