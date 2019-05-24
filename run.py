from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.config.manager import ConfigManager
from yowsup.profile.profile import YowProfile
import sys
import json

class YowsupEchoStack(object):
    def __init__(self, profile):
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(EchoLayer)\
            .build()

        self._stack.setProfile(profile)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    def start(self):
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()


def startEcho():
    config_manager = ConfigManager()
    _config_phone = '542604268467'
    # TODO: if everything works fine, remoce following commented line
    # _config = config_manager.load(_config_phone)
    _config = config_manager.load_path('config/542604268467.json')
    _profile = YowProfile(_config_phone, _config)
    _layer_network_dispatcher = None
    from yowsup.demos import echoclient
    try:
        print('starting stack')
        stack = YowsupEchoStack(_profile)
        if _layer_network_dispatcher is not None:
            stack.set_prop(YowNetworkLayer.PROP_DISPATCHER, _layer_network_dispatcher)
        stack.start()
    except KeyboardInterrupt:
        print("\nYowsdown")
        sys.exit(0)


if __name__==  "__main__":
    startEcho()
