# coding=utf-8
import datetime
import re
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.db.models import fields
from core.validators import ogrn_validator, inn_validator

phone_validator = RegexValidator(regex="\(\d{3}\)\s\d{3}-\d{2}-\d{2}", message=u"Телефон должен быть в формате (455) 123-45-67")
#ogrn_validator = RegexValidator(regex="[1-3,5]\d{12}", message=u"ОГРН не соответствует стандарту. Подробнее на http://ru.wikipedia.org/wiki/Основной_государственный_регистрационный_номер")
#inn_validator = RegexValidator(regex="\d{12}", message=u"ИНН не соответствует стандарту. Подробнее на http://ru.wikipedia.org/wiki/Идентификационный_номер_налогоплательщика")

class BaseModel(models.Model):
    created_at = fields.DateTimeField(u"Дата создания", auto_now_add=True)
    modified_at = fields.DateTimeField(u"Дата изменения", auto_now=True)
    deleted_at = fields.DateTimeField(u"Дата удаления", null=True, blank=True)

    class Meta:
        abstract = True


class NamedModel(BaseModel):
    name = fields.CharField(u"Наименование", max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class HealthObjectType(NamedModel):
    """
    Типы объектов здравоохранения
    """

    class Meta:
        verbose_name = u"тип объекта здравоохранения"
        verbose_name_plural = u"типы объектов здравоохранения"


class Position(NamedModel):
    """
    Должности
    """

    class Meta:
        verbose_name = u"должность"
        verbose_name_plural = u"должности"


class ServiceType(NamedModel):
    """
    Специальности
    """

    class Meta:
        verbose_name = u"услуга"
        verbose_name_plural = u"услуги"


class StreetObject(BaseModel):
    name = fields.CharField(u"Название", max_length=128, null=False, db_index=True)
    valid = fields.BooleanField(u"Действующее название улицы", null=False, default=True)


class DistrictObject(BaseModel):
    name = fields.CharField(u"Название", max_length=128, unique=True, null=False)


class AddressObject(BaseModel):
    zip_code = fields.CharField(u"Индекс", max_length=6)
    area = fields.CharField(u"Область", max_length=128)
    district = models.ForeignKey(DistrictObject, verbose_name=u"Район", null=False)
    city_type = fields.CharField(u"Тип нас. пункта", max_length=128)
    city = fields.CharField(u"Нас. пункт", max_length=128)
    street = models.ForeignKey(StreetObject, verbose_name=u"Улица", null=False)
    house = fields.CharField(u"Дом", max_length=6)
    house_letter = fields.CharField(u"буква", max_length=2, blank=True)
    housing = fields.CharField(u"Корпус", max_length=2, blank=True)
    building = fields.CharField(u"Строение", max_length=2, blank=True)

    class Meta:
        verbose_name = u"адрес"
        verbose_name_plural = u"адреса"


SEX_CHOICE = (
    ('M', "Мужской"),
    ('F', "Женский"),
)


class ChiefModelMixin(BaseModel):
    chief_first_name = fields.CharField(u"Имя руководителя", max_length=256)
    chief_middle_name = fields.CharField(u"Отчество руководителя", max_length=256)
    chief_last_name = fields.CharField(u"Фамилия руководителя", max_length=256)
    chief_sex = fields.CharField(u"Пол руководителя", max_length=1, choices=SEX_CHOICE)
    chief_speciality = models.ForeignKey(Position, verbose_name=u"Специальность руководителя")
    chief_phone = models.CharField(u"Телефон руководителя", max_length=128, null=True, blank=True, validators=[phone_validator])

    class Meta:
        abstract = True


class LegalEntity(ChiefModelMixin):
    """
    Юридические лица
    """
    name = fields.CharField(u"Наименование", max_length=128, help_text=u"Наименование юр. лица из устава")
    ogrn_code = fields.CharField(u"ОГРН", max_length=256, validators=[ogrn_validator], null=True, blank=True, help_text=u"Основной государственный регистрационный номер")
    inn_code = fields.CharField(u"ИНН", max_length=256, validators=[inn_validator])
    jur_address = models.ForeignKey(AddressObject, verbose_name=u"Юридический адрес", related_name='registered_entities')
    fact_address = models.ForeignKey(AddressObject, verbose_name=u"Фактический адрес", null=True, blank=True, related_name='operating_entities')

    info = models.TextField(u"Дополнительная информация", null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"юридическое лицо"
        verbose_name_plural = u"юридические лица"


class Service(ChiefModelMixin):
    """
    Услуги
    """
    legal_entity = models.ForeignKey(LegalEntity, verbose_name=u"Юридическое лицо", related_name='services')
    healing_object = models.ForeignKey('HealingObject', verbose_name=u"Объект здравоохранения", related_name='services')
    service = models.ForeignKey(ServiceType, related_name='healing_objects', verbose_name=u"Услуга")
    phone = models.CharField(u"Телефон", max_length=256, validators=[phone_validator])
    fax = models.CharField(u"Факс", max_length=256, validators=[phone_validator], null=True, blank=True)
    site_url = models.URLField(u"Адрес сайта", max_length=1024, null=True, blank=True)
    info = models.TextField(u"Дополнительная информация", null=True, blank=True)
    workdays = models.CharField(u"Рабочие дни", max_length=128)
    workhours = models.CharField(u"Часы работы", max_length=128)
    daysoff = models.CharField(u"Нерабочие дни", null=True, blank=True, max_length=128)
    daysoff_restrictions = models.CharField(u"Ограничения выходных дней", null=True, blank=True, max_length=256)
    specialization = models.CharField(u"Специализация", max_length=256, null=True, blank=True)
    paid_services = models.CharField(u"Платные услуги", max_length=256, null=True, blank=True)
    free_services = models.CharField(u"Бесплатные услуги", max_length=256, null=True, blank=True)
    drug_provisioning = models.CharField(u"Лекарственное обеспечение", max_length=256, null=True, blank=True)
    hospital_beds = models.CharField(u"Койкофонд", max_length=256, null=True, blank=True)
    departments = models.CharField(u"Перечень отделений", max_length=256, null=True, blank=True)
    hospital_levels = models.CharField(u"Уровень стационара", max_length=256, null=True, blank=True)
    tour = models.CharField(u"Смена", max_length=256, null=True, blank=True)
    receipes_provisioning = models.CharField(u"Обеспечение рецептов", max_length=256, null=True, blank=True)
    aptheke_type = models.CharField(u"Тип аптеки", max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = u"услуга"
        verbose_name_plural = u"услуги"
        unique_together = ('legal_entity', 'healing_object', 'service')


class HealingObject(BaseModel):
    """
    Объект здравоохранения
    """
    address = models.ForeignKey(AddressObject)
    object_type = models.ForeignKey(HealthObjectType, related_name='healing_objects', verbose_name=u"Тип")
    legal_entities = models.ManyToManyField(LegalEntity, through=Service, related_name='healing_objects')

    full_name = fields.CharField(u"Полное наименование", max_length=2048,
                                 help_text=u"Государственное казенное учреждение здравоохранения города Москвы «Десткая городская психоневрологическая больница № 32 Департамента здравоохранения города Москвы»")
    name = fields.CharField(u"Наименование", max_length=1024, help_text=u"ГКУЗ «Десткая городская психоневрологическая больница № 32»")
    short_name = fields.CharField(u"Наименование", max_length=1024, help_text=u"ДГПНБ № 32")
    global_id = fields.CharField(u"Глобальный идентификатор", max_length=128, null=True, blank=True)
    info = models.TextField(u"Дополнительная информация", null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"объект здравоохранения"
        verbose_name_plural = u"объекты здравоохранения"


