
class InAppValidationError(Exception):
    """ Base class for all validation errors """

    def __init__(self, msg, response=None):
        super(InAppValidationError, self).__init__(msg)
        self.response = response

