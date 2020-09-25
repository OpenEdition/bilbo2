""" Timer class """
import time

class Timer(object):
    """
    Simple timer class
    """
    
    def __init__(self, name='', autostart=True):
        """
        Instanciate a new named timer
        """
        self._name = name
        self._start = None
        self._all = []
        self._autostart = autostart
        self._last = None
        if autostart:
            self.start()

    @property
    def name(self):
        return self._name

    @property
    def last(self):
        return self._last

    def start(self):
        """
        Starts the timer
        """
        self._start = time.time()

    def reset(self, name=None):
        """
        Reset the timer and store ellapsed time
        
        :param name: str: new timer name. If giver stored datas are errased
        """
        if name is not None:
            self._name = name
            if self._autostart:
                self.start()
            self._all = []
            return
        self._all.append(self.t())
        self._start = None

    def mean(self):
        """
        :returns: the average of recorded timers
        """
        return sum(self._all) / len(self._all)

    def t(self):
        """
        :returns: elapsed seconds since last start() call
        """
        if self._start is None:
            raise RuntimeError('Timer not started')
        return time.time() - self._start

    def __str__(self):
        """
        :returns: name + ellapsed time and reset the timer
        """
        res = ''
        if len(self._name) > 0:
            res = '%s : ' % self._name
        res += '%0.4f' % self.t()
        self._last = res
        self.reset()
        return res
