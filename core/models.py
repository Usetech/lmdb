# coding=utf-8
import datetime
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.db.models import fields

phone_validator = RegexValidator(regex="\(\d3\) \d3-\d2-\d2", message=u"Телефон должен быть в формате (455) 123 45 67")
ogrn_validator = RegexValidator(regex="[1-3,5]\d12", message=u"ОГРН не соответствует стандарту. Подробнее на http://ru.wikipedia.org/wiki/Основной_государственный_регистрационный_номер")
inn_validator = RegexValidator(regex="\d12", message=u"ИНН не соответствует стандарту. Подробнее на http://ru.wikipedia.org/wiki/Идентификационный_номер_налогоплательщика")


class BaseModel(models.Model):
    created_at = fields.DateTimeField(u"Дата создания")
    modified_at = fields.DateTimeField(u"Дата изменения")
    deleted_at = fields.DateTimeField(u"Дата удаления", null=True, blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.modified_at = datetime.datetime.today()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class NamedModel(BaseModel):
    name = fields.CharField(u"Наименование", max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class AddressObjectType(NamedModel):
    """
    Типы адресных объектов
    """

    class Meta:
        verbose_name = u"тип адресного объекта"
        verbose_name_plural = u"типы адресных объектов"


class HeadSpeciality(NamedModel):
    """
    Специальности
    """

    class Meta:
        verbose_name = u"специальность"
        verbose_name_plural = u"специальности"


class AddressObjectService(NamedModel):
    """
    Специальности
    """

    class Meta:
        verbose_name = u"услуга"
        verbose_name_plural = u"услуги"


class LegalEntity(BaseModel):
    """
    Юридические лица
    """
    name = fields.CharField(u"Наименование", max_length=128, help_text=u"Наименование юр. лица из устава")
    ogrn_code = fields.CharField(u"ОГРН", max_length=256, validators=[ogrn_validator], null=True, blank=True, help_text=u"Основной государственный регистрационный номер")
    inn_code = fields.CharField(u"ИНН", max_length=256,
                                validators=[RegexValidator(regex="\d+", message=u"ИНН может содержать только цифры")])
    chief_name = fields.CharField(u"ФИО руководителя", max_length=256)
    jur_address = fields.CharField(u"Юр. адрес", max_length=1024)
    fact_address = fields.CharField(u"Факт. адрес", max_length=1024, null=True, blank=True)
    head_physician = fields.CharField(u"Реквизиты глав. врача", max_length=1024, null=True, blank=True)
    reception_phone = fields.CharField(u"Тел. приёмной", max_length=1024, validators=[phone_validator], null=True,
                                       blank=True)
    registry_phone = fields.CharField(u"Тел. регистратуры", max_length=1024, validators=[phone_validator], null=True,
                                      blank=True)
    worktime = fields.CharField(u"Время работы", max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"юридическое лицо"
        verbose_name_plural = u"юридические лица"

SEX_CHOICE = (
    ('M', "Мужской"),
    ('F', "Женский"),
)


class AddressObject(BaseModel):
    """
    Адресные объекты
    """
    owner = models.ForeignKey(LegalEntity, related_name='address_objects', verbose_name=u"Юр. лицо")
    type = models.ForeignKey(AddressObjectType, related_name='address_objects', verbose_name=u"Тип")
    services = models.ManyToManyField(AddressObjectService, related_name='address_objects', verbose_name=u"Услуги")
    full_name = fields.CharField(u"Полное наименование", max_length=2048,
                                 help_text=u"Государственное казенное учреждение здравоохранения города Москвы «Десткая городская психоневрологическая больница № 32 Департамента здравоохранения города Москвы»")
    name = fields.CharField(u"Наименование", max_length=1024, help_text=u"ГКУЗ «Десткая городская психоневрологическая больница № 32»")
    short_name = fields.CharField(u"Наименование", max_length=1024, help_text=u"ДГПНБ № 32")
    okrug = fields.CharField(u"Округ", max_length=1024, help_text=u"Административный округ по территориальной принадлежности")
    address = fields.CharField(u"Адрес", max_length=1024)
    chief = fields.CharField(u"Руководитель", max_length=128, help_text=u"ФИО руководителя")
    chief_sex = fields.CharField(u"Пол руководителя", max_length=1, choices=SEX_CHOICE)
    chief_speciality = models.ForeignKey(HeadSpeciality, verbose_name=u"Специальность руководителя")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"адресный объект"
        verbose_name_plural = u"адресные объекты"