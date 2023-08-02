# coding=utf-8
import logging
import sys

from tools.singleton import Singleton


class LoggerHelper(Singleton):
    def __init__(self):
        logging.basicConfig(filename='oper.log', filemode='w', level=logging.DEBUG)
        self.__logger = logging.getLogger('test')
        self.__logger.addHandler(logging.StreamHandler(stream=sys.stdout))

    def get_logger(self):
        return self.__logger