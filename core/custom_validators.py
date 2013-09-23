# coding=utf-8

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.validators import RegexValidator

__author__ = 'yveretelnikov'
__phone_validator = RegexValidator(regex="\(\d{3}\) \d{3}-\d{2}-\d{2}",
                                   message=u"Телефон должен быть в формате (455) 123-45-67")
__object_name_validator = RegexValidator(regex=u"^[0-9A-Za-zА-Яа-я\-№«»\s\(\)\,\.]+$",
                                         message=u"Название объекта содержит недопустимые символы или излишние пробелы")


class CustomValidators(object):
    """ Complex validators for data harmonization """
    def __init__(self, validators):
        self.validators = validators

    def apply(self, obj, value):
        pass


class TypeCodedCustomValidator(CustomValidators):
    """
    Type coded business validation
    """

    def __init__(self, object_type_codes, validators):
        super(TypeCodedCustomValidator, self).__init__(validators)
        self.object_type_codes = object_type_codes

    def apply(self, obj, value):
        if '*' in self.object_type_codes or obj.object_type.code in self.object_type_codes:
            for v in self.validators:
                v(obj, value)


def hv_person_name(obj, value):
    """
    Full name validation
    """
    # if value is not None:
    #    return True
    raise ValidationError("hv_person_name error")


def hv_object_name(obj, value):
    """
    Full name validation
    """
    __object_name_validator(value)
    # if ok, test for excessive space symbols
    if u'  ' in value:
        raise ValidationError(u"Название объекта содержит излишние пробельные символы")

def hv_cannot_be_null(obj, value):
    """
    Checks value for null
    """
    if value is not None:
        return True
    raise ValidationError("Error")


def hv_phone_number(obj, value):
    """
    Checks for phone number
    """
    pass


def hv_email(value):
    """
    Checks for email
    """
    return validate_email(value)
