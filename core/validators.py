# coding=utf-8

import re
from django.core.exceptions import ValidationError

__author__ = 'pparkhomenko'

__ogrn_regexp = re.compile(r"^([1-3,5]\d{11})(\d)$")
__ogrn_error_message = u"ОГРН не соответствует стандарту. " +\
                       u"Подробнее на http://ru.wikipedia.org/wiki/Основной_государственный_регистрационный_номер"


def ogrn_validator(value):
    result = __ogrn_regexp.match(value)
    if result is not None:
        number = int(result.group(1))
        expected = int(result.group(2))
        return __validate_checksum(number, expected, __ogrn_error_message)
    raise ValidationError(__ogrn_error_message)

__jur_inn_coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
__fiz_inn_coefficients1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
__fiz_inn_coefficients2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
__inn_error_message = u"ИНН не соответствует стандарту. " +\
                      u"Подробнее на http://ru.wikipedia.org/wiki/Идентификационный_номер_налогоплательщика"


def inn_validator(value):
    """ Tries to calc correct INN
    :param value: inn candidate string
    """
    if not value.isdigit():
        raise ValidationError(__inn_error_message)
    if len(value) == 10:
        index = 0
        checksum = 0
        for digit in value:
            digit = int(digit)
            if index < 9:
                checksum += __jur_inn_coefficients[index] * digit
            else:
                return __validate_checksum(checksum, digit, __inn_error_message)
            index += 1
    elif len(value) == 12:
        index = 0
        checksum1 = 0
        checksum2 = 0
        for digit in value:
            digit = int(digit)
            if index < 10:
                checksum1 += __fiz_inn_coefficients1[index] * digit
                checksum2 += __fiz_inn_coefficients2[index] * digit
            elif index == 10:
                __validate_checksum(checksum1, digit, __inn_error_message)
                checksum2 += __fiz_inn_coefficients2[index] * digit
            else:
                return __validate_checksum(checksum2, digit, __inn_error_message)
            index += 1
    raise ValidationError(__inn_error_message)


def __validate_checksum(checksum, expected, message):
    """ Validates checksum for expected value by using simple algo
    :param checksum:
    :param expected:
    :param message:
    :return: :raise:
    """
    checksum %= 11
    if checksum == 10:
        if expected == 0:
            return True
    elif checksum == expected:
        return True
    raise ValidationError(message)