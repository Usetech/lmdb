# coding=utf-8

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.validators import RegexValidator

__author__ = 'yveretelnikov'
phone_validator = RegexValidator(regex="\(\d{3}\) \d{3}-\d{2}-\d{2}",
                                 message=u"Телефон должен быть в формате (455) 123-45-67")


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

    def __init__(self, object_type_names, validators):
        super(TypeCodedCustomValidator, self).__init__(validators)
        self.object_type_names = object_type_names

    def apply(self, obj, value):
        for v in self.validators:
            v(obj, value)


def hv_full_name(obj, value):
    """
    Full name validation
    """
    # if value is not None:
    #    return True
    raise ValidationError("Full name error")


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
