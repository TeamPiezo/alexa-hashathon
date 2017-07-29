"""
Helper functions for Potts
"""
from datetime import datetime


def add_am_pm(timedigit):
    if int(timedigit) == 0:
        return '12 am'
    elif int(timedigit) < 12:
        return str(timedigit) + ' am'
    elif int(timedigit) == 12:
        return str(timedigit) + ' pm'
    return str(timedigit-12) + ' pm'


def get_time_strings(time_objs):
    """

    :param time_list:
    :return:
    """
    ampm_list = list(map(add_am_pm, time_objs))
    response = ', '.join(ampm_list[:-1])
    return response + ' and ' + ampm_list[-1]
