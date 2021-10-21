import pytz
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.conf import settings


tz = pytz.timezone(settings.TIME_ZONE)


class NotAcceptableError(Exception):

    def __init__(self, response="", meta="", status=400):
        self.response = response
        self.status = status
        self.meta = meta
        super(Exception, self).__init__(
            meta + ". Status Code: " + str(status))

    def __str__(self):
        return ("Response: {response}, Meta: {meta}, Status: {status}".format(
            response=self.response, meta=self.meta, status=self.status))

        
class Date(object):

    @classmethod
    def now(cls):
        return timezone.localtime(timezone.now())


def error_wrapper(x):
    """
    x is will be a dictionary with the following structure
    {"error_type_1": [error1, error2], "error_type_1": [error1, error2] .....}
    return a list of the type
    ["error1", "error2", ...]
    """
    errors = list()
    for error_key, error_list in list(x.items()):
        for error in error_list:
            if error_key == 'non_field_errors':
                errors.append(error)
            else:
                errors.append("%s: %s" % (error_key, error))
    return errors


