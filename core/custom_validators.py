# coding=utf-8

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.validators import RegexValidator

__author__ = 'yveretelnikov'


class CustomValidators(object):
    """ Complex validators for data harmonization """
    def __init__(self, validators):
        self.validators = validators

    def apply(self, obj, value):
        pass


class TypeCodeValidators(CustomValidators):
    """
    Type coded business validation
    """
    def __init__(self, object_type_codes, validators):
        super(TypeCodeValidators, self).__init__(validators)
        self.object_type_codes = object_type_codes

    def apply(self, obj, value):
        if '*' in self.object_type_codes or obj.object_type.code in self.object_type_codes:
            for v in self.validators:
                v(obj, value)


def custom_max_len(max_len):
    def field_length(obj, value):
        if len(value) > max_len:
            raise ValidationError(u"Длина реквизита превышает максимально допустимую")
    return field_length

__person_name_validator = RegexValidator(regex=u"^[А-Яа-я\s]+$",
                                         message=u"Название объекта содержит недопустимые символы или излишние пробелы")


def custom_person_name(obj, value):
    """
    Person name validation
    """
    if value is None:
        raise __generate_error_empty()
    __person_name_validator(value)
    # if ok, test for excessive space symbols
    if u'  ' in value:
        raise ValidationError(u"Реквизит объекта не должен содаржать излишних пробельных символов")

__object_name_validator = RegexValidator(regex=u"^[0-9A-Za-zА-Яа-я\-№«»\s\(\)\,\.]+$",
                                         message=u"Название объекта содержит недопустимые символы или излишние пробелы")


def custom_object_name(obj, value):
    """
    Object name validation
    """
    if value is None:
        raise __generate_error_empty()
    __object_name_validator(value)
    # if ok, test for excessive space symbols
    if u'  ' in value:
        raise ValidationError(u"Реквизит объекта не должен содаржать излишних пробельных символов")


def custom_not_null(obj, value):
    """
    Checks value for null
    """
    if value is None:
        raise __generate_error_empty()

__phone_validator = RegexValidator(regex="^\(\d{3}\) \d{3}-\d{2}-\d{2}$",
                                   message=u"Телефон должен быть в формате (XXX) XXX-XX-XX")


def custom_phone_number(obj, value):
    """
    Checks for phone number
    """
    __phone_validator(value)


def custom_email(value):
    """
    Checks for email
    """
    return validate_email(value)

__postal_code_validator = RegexValidator(regex="\^d{6}\$",
                                         message=u"Почтовый индекс должен быть в формате XXXXXX")


def custom_postal_code(value):
    """
    Postal code validation
    """
    __postal_code_validator(value)


def custom_not_null_if_true(attr_name):
    """
    Validate attr != null only if `attr_name` attr exists and contains true
    """
    def __inner(object, value):
        if hasattr(object, attr_name):
            f = getattr(object, attr_name)
            if f and (value is None):
                raise __generate_error_empty()
    return __inner


def custom_not_null_only_when_true(attr_name):
    """
    Validate attr != null only if `attr_name` attr exists and contains false
    """
    def __inner(object, value):
        if hasattr(object, attr_name):
            f = getattr(object, attr_name)
            if f and (value is None):
                raise __generate_error_empty()
            if not f and (value is not None):
                raise __generate_error_not_empty()
    return __inner


def custom_null_if_false(attr_name):
    """
    Validate attr != null only if `attr_name` attr exists and contains false
    """
    def __inner(object, value):
        if hasattr(object, attr_name):
            f = getattr(object, attr_name)
            if (not f) and (value is not None):
                raise __generate_error_not_empty()
    return __inner


def __generate_error_empty():
    return ValidationError(u"Реквизит не может быть не заполненым")


def __generate_error_not_empty():
    return ValidationError(u"Реквизит не может быть заполненым")

def __generate_error_invalid_value():
    return ValidationError(u"Значение реквизита некорректно")


def greater_than(attr_name):
    """
    Validate attr != null only if `attr_name` attr exists and contains false
    """
    def __inner(object, value):
        if hasattr(object, attr_name):
            f = getattr(object, attr_name)
            if not(f is None) and not (value is None) and (value <= f):
                raise __generate_error_invalid_value()
    return __inner