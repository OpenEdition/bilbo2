class BilboError(Exception):
    "A base class for MyProject exceptions."""
    pass


class EstimatorError(BilboError):
    def __init__(self, msg):
        super().__init__(msg)
