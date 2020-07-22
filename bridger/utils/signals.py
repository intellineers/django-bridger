class Signal:
    """A convinience class that encapsulates a signal in order to
       be used in the DisconnectedSignals context manager
    """

    def __init__(self, signal, receiver, sender):
        self.signal = signal
        self.receiver = receiver
        self.sender = sender

    def connect(self):
        self.signal.connect(receiver=self.receiver, sender=self.sender)

    def disconnect(self):
        self.signal.disconnect(receiver=self.receiver, sender=self.sender)


class DisconnectSignals:
    """A Context-Manager to temporarily disable a set of signals
    """

    def __init__(self, signals):
        self.signals = signals

    def __enter__(self):
        for signal in self.signals:
            signal.disconnect()

    def __exit__(self, type, value, traceback):
        for signal in self.signals:
            signal.connect()
