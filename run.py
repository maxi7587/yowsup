from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
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


class YowsupEchoStack(object):
    def __init__(self, profile):
        stackBuilder = YowStackBuilder()

        # TODO: checkif instantiation works, else return to old way
        self.echo_layer = EchoLayer()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(self.echo_layer)\
            .build()

        self._stack.setProfile(profile)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    @threaded
    def start(self):
        print('inside start begin')
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()


def startEcho():
    config_manager = ConfigManager()
    _config_phone = '542604268467'
    # TODO: if everything works fine, remoce following commented line
    # _config = config_manager.load(_config_phone)
    _config = config_manager.load_path('config/542604268467.json')
    _profile = YowProfile(_config_phone, _config)
    # _layer_network_dispatcher = None
    # from yowsup.demos import echoclient

    try:
        print('starting stack')
        stack = YowsupEchoStack(_profile)
        # if _layer_network_dispatcher is not None:
        #     stack.set_prop(YowNetworkLayer.PROP_DISPATCHER, _layer_network_dispatcher)
        echo_thread = threading.Thread(target=stack.start)
        echo_thread.start()

        print(echo_thread.is_alive())
        while True:
            try:
                print('main thread try')
                # echo_thread.join(timeout = 0.1)
                # echo_thread.join(4)
                import time
                time.sleep(3)
                print(threading.enumerate())
                # echo_thread.stop()
            except IOError:
                print('IOERror')
                pass #Gets thrown when we interrupt the join
            except KeyboardInterrupt:
                print("\nYowsdown")
                sys.exit(0)
        # print('--------------------------------------')
        # print(stack._stack.__dict__)
        # print('--------------------------------------')
    except KeyboardInterrupt:
        print("\nYowsdown")
        echo_thread_killer.set()
        sys.exit(0)


if __name__==  "__main__":
    startEcho()


# from threading import Thread;
# from threading import Event;
# import time;
#
#
# class ChildThread(Thread):
#     myStopSignal = 0
#
#     def __init__(self,aStopSignal):
#
#         Thread.__init__(self)
#         self.myStopSignal = aStopSignal
#
#     # def run(self):
#     def run(self):
#         print("Child Thread:Started")
#         for i in range(1,10):
#             if(self.myStopSignal.wait(0)):
#                 print ("ChildThread:Asked to stop")
#                 break;
#
#             print("Doing some low priority task taking long time")
#             time.sleep(2) #Just simulating time taken by task with sleep
#
#         print("Child Thread:Exiting")
#
#
# if __name__==  "__main__":
#     print("Main Thread:Started")
#     aStopSignal = Event()
#     aChildThread = ChildThread(aStopSignal)
#     aChildThread.daemon = True
#     aChildThread.start()
#     aChildThread.join(4) # I can wait for 4 seconds only
#
#     # if aChildThread.is_alive() is True:
#     #     print('is_alive!!!')
#     #     aStopSignal.set()
#     #     aChildThread.join()
#
#     print("Main Thread; Exiting")
