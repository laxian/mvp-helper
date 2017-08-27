import abc


class Api(object):

    def __init__(self):
        pass

    @abc.abstractclassmethod
    def holder_list(self):
        pass

    @abc.abstractclassmethod
    def key_list(self):
        pass



