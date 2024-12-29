import traceback

from monitor import Monitor
from logger import LoggerMethod
from settings import *
# from graph import Graph


def main():
    try:
        monitor = Monitor(interface=INTERFACE, logging_method=LOGGING_METHOD)
        monitor.start()
    #    start_graph()
    except Exception as e:
        print(traceback.format_exc())
        exit()

    while True:
        input("Press enter to exit. ")
        exit()


if __name__ == "__main__":
    main()
