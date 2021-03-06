# coding=utf-8
import datetime
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.db.models import fields, permalink
from django.utils import timezone
from core.managers import HealingObjectManager, LegalEntityManager, ServiceManager
from core.validators import ogrn_validator, inn_validator

phone_validator = RegexValidator(regex="\(\d{3}\) \d{3}-\d{2}-\d{2}", message=u"Телефон должен быть в формате (455) 123-45-67")


class BaseModel(models.Model):
    created_at = fields.DateTimeField(u"Дата создания", default=timezone.now)
    modified_at = fields.DateTimeField(u"Дата изменения", default=timezone.now)
    deleted_at = fields.DateTimeField(u"Дата удаления", null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        # Этот код не удалять, auto_now и т.п. ведут к проблемам в админке
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.modified_at = datetime.datetime.today()
        return super(BaseModel, self).save(*args, **kwargs)


class NamedModel(BaseModel):
    name = fields.CharField(u"Наименование", max_length=128, unique=True)

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
        verbose_name = u"тип услуги"
        verbose_name_plural = u"типы услуг"


class StreetObject(BaseModel):
    bti_id = fields.CharField(u"Уникальный код улицы", max_length=16, null=True, blank=True, unique=True)
    name = fields.CharField(u"Наименование", max_length=128)
    type = fields.CharField(u"Тип топонима", max_length=128)
    iname = fields.CharField(u"Название для поиска, сортировки", max_length=256)
    valid = fields.BooleanField(u"Действующее", null=False, default=True)

    def __unicode__(self):
        return self.iname

    class Meta:
        verbose_name = u"улица"
        verbose_name_plural = u"улицы"


class DistrictObject(NamedModel):
    class Meta:
        verbose_name = u"административный округ"
        verbose_name_plural = u"административные округа"


status_choices = (
    ('OK', u"Проверен"),
    ('E', u"С ошибками"),
    ('W', u"В работе"),
    ('A', u"Требует актуализации"),
)


class AddressObject(BaseModel):
    bti_id = fields.CharField(u"Уникальный идентификатор записи каталога", max_length=16, null=True, blank=True, unique=True)
    zip_code = fields.CharField(u"Индекс", max_length=6)
    area = fields.CharField(u"Область", max_length=128, blank=True)
    district = models.ForeignKey(DistrictObject, verbose_name=u"Район", null=True, blank=True)
    city_type = fields.CharField(u"Тип нас. пункта", max_length=128)
    city = fields.CharField(u"Нас. пункт", max_length=128)
    street = models.ForeignKey(StreetObject, verbose_name=u"Улица", null=False)
    house = fields.CharField(u"Дом", max_length=16, null=False, blank=True)
    house_letter = fields.CharField(u"буква", max_length=16, null=False, blank=True)
    housing = fields.CharField(u"Корпус", max_length=16, null=False, blank=True)
    building = fields.CharField(u"Строение", max_length=16, null=False, blank=True)
    full_address_string = fields.CharField(u"Полная адресная строка", max_length=512, null=True, blank=True, db_index=True)

    def full_string(self):
        house = u""
        if self.house:
            house = u"д. %s%s " % (self.house.strip(), self.house_letter.strip())

        housing = u""
        if self.housing:
            housing = u"корп. %s " % self.housing.strip()

        building = u""
        if self.building:
            building = u"стр. %s " % self.building.strip()
        str = u"%s %s%s%s" % (self.street.iname, house, housing, building)

        if self.city:
            str = self.city + "; " + str

        return str.strip()

    full_string.short_description = u"Полное наименование"

    def __unicode__(self):
        return self.full_string()

    class Meta:
        verbose_name = u"адрес"
        verbose_name_plural = u"адреса"
        index_together = [['house', 'house_letter', 'housing', 'building', 'street'], ]


SEX_CHOICE = (
    ('M', "Мужской"),
    ('F', "Женский"),
)


class ChiefModelMixin(BaseModel):
    chief_original_name = fields.TextField(u"Ф.И.О. руководителя", blank=True, null=True)
    chief_first_name = fields.CharField(u"Имя руководителя", max_length=256, blank=True, null=True)
    chief_middle_name = fields.CharField(u"Отчество руководителя", max_length=256, blank=True, null=True)
    chief_last_name = fields.CharField(u"Фамилия руководителя", max_length=256, blank=True, null=True)
    chief_sex = fields.CharField(u"Пол руководителя", max_length=1, choices=SEX_CHOICE, blank=True, null=True)
    chief_position = models.ForeignKey(Position, verbose_name=u"Должность руководителя", blank=True, null=True)
    chief_phone = models.CharField(u"Телефон руководителя", max_length=128, null=True, blank=True
    #    , validators=[phone_validator]
    )

    class Meta:
        abstract = True


class LegalEntity(ChiefModelMixin):
    """
    Юридические лица
    """
    name = fields.CharField(u"Наименование", max_length=256, help_text=u"Наименование юр. лица из устава", unique=True)
    original_name = fields.CharField(u"Наименование (исх.)", max_length=256, null=True, blank=True)
    ogrn_code = fields.CharField(u"ОГРН", max_length=256, validators=[ogrn_validator], null=True, blank=True,
                                 help_text=u"Основной государственный регистрационный номер")
    inn_code = fields.CharField(u"ИНН", max_length=256, null=True, blank=True, validators=[inn_validator])
    jur_address = models.ForeignKey(AddressObject, verbose_name=u"Юридический адрес", null=True, blank=True, related_name='registered_entities')
    fact_address = models.ForeignKey(AddressObject, verbose_name=u"Фактический адрес", null=True, blank=True, related_name='operating_entities')
    original_address = models.TextField(u"Исходный адрес", null=True, blank=True)
    info = models.TextField(u"Дополнительная информация", null=True, blank=True)
    errors = models.TextField(u"Ошибки импорта", null=True, blank=True)
    manager_user = models.EmailField(u"E-mail (логин)", null=True, blank=True)
    status = models.CharField(u"Статус", max_length=5, db_index=True, default='OK', choices=status_choices)

    objects = LegalEntityManager()

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('legal_entity', [self.id])

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    class Meta:
        verbose_name = u"юридическое лицо"
        verbose_name_plural = u"юридические лица"
        permissions = (('viewall_legalentity', u"Просматривать полный писок юрлиц"),\
                       ('view_legalentity', u"Просмотреть юрлицо"),)


class Service(ChiefModelMixin):
    """
    Услуги
    """
    healing_object = models.ForeignKey('HealingObject', verbose_name=u"Объект здравоохранения", related_name='services')
    service = models.ForeignKey(ServiceType, related_name='healing_objects', verbose_name=u"Услуга")
    phone = models.CharField(u"Телефон", max_length=256, blank=True, null=True)
    fax = models.CharField(u"Факс", max_length=256, null=True, blank=True)
    site_url = models.URLField(u"Адрес сайта", max_length=1024, null=True, blank=True)
    info = models.TextField(u"Дополнительная информация", null=True, blank=True)
    workdays = models.CharField(u"Рабочие дни", max_length=1024, blank=True, null=True)
    workhours = models.CharField(u"Часы работы", max_length=1024, blank=True, null=True)
    daysoff = models.CharField(u"Нерабочие дни", null=True, blank=True, max_length=1024)
    daysoff_restrictions = models.CharField(u"Ограничения выходных дней", null=True, blank=True, max_length=1024)
    specialization = models.TextField(u"Специализация", null=True, blank=True)
    paid_services = models.CharField(u"Платные услуги", max_length=1024, null=True, blank=True)
    free_services = models.TextField(u"Бесплатные услуги", null=True, blank=True)
    drug_provisioning = models.CharField(u"Лекарственное обеспечение", max_length=1024, null=True, blank=True)
    hospital_beds = models.CharField(u"Койкофонд", max_length=256, null=True, blank=True)
    departments = models.TextField(u"Перечень отделений", null=True, blank=True)
    hospital_levels = models.CharField(u"Уровень стационара", max_length=1024, null=True, blank=True)
    tour = models.CharField(u"Смена", max_length=1024, null=True, blank=True)
    receipes_provisioning = models.CharField(u"Обеспечение рецептов", max_length=1024, null=True, blank=True)
    drugstore_type = models.CharField(u"Тип аптеки", max_length=256, null=True, blank=True)
    hospital_type = models.CharField(u"Тип стационара", max_length=256, null=True, blank=True)

    objects = ServiceManager()

    def __unicode__(self):
        return "%s" % self.service.name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    class Meta:
        verbose_name = u"услуга"
        verbose_name_plural = u"услуги"
        unique_together = ('healing_object', 'service')


class HealingObject(BaseModel):
    """
    Объект здравоохранения
    """
    object_type = models.ForeignKey(HealthObjectType, related_name='healing_objects', verbose_name=u"Тип")
    legal_entity = models.ForeignKey(LegalEntity, verbose_name=u"Юридическое лицо", related_name='healing_objects', null=True, blank=False)
    address = models.ForeignKey(AddressObject, verbose_name=u"Адрес", null=True, blank=True)
    original_address = models.TextField(u"Исходный адрес", null=True, blank=True)

    full_name = fields.CharField(u"Полное наименование", max_length=2048,
                                 help_text=u"Например: Государственное казенное учреждение здравоохранения города Москвы «Десткая городская психоневрологическая больница № 32 Департамента здравоохранения города Москвы»")
    name = fields.CharField(u"Наименование", max_length=1024, help_text=u"Например: ГКУЗ «Десткая городская психоневрологическая больница № 32»")
    short_name = fields.CharField(u"Краткое наименование", max_length=1024, help_text=u"Например: ДГПНБ № 32", null=True, blank=True)
    global_id = fields.CharField(u"Глобальный идентификатор", max_length=128, null=True, blank=True)
    info = models.TextField(u"Дополнительная информация", null=True, blank=True)
    errors = models.TextField(u"Ошибки импорта", null=True, blank=True)
    parent = models.ForeignKey('self', related_name='branches', null=True, blank=True, verbose_name=u"Главное ЛПУ")
    manager_user = models.EmailField(u"E-mail (логин)", null=True, blank=True)
    status = models.CharField(u"Статус", max_length=5, db_index=True, default='OK', choices=status_choices)

    is_closed = fields.BooleanField(u"Признак закрытого ЛПУ", null=False, default=False)
    closed_at = fields.DateField(u"Дата закрытия", null=True, blank=True)
    closing_reason = fields.CharField(u"Причина закрытия", null=True, blank=True, max_length=1024)
    reopened_at = fields.DateField(u"Дата повторного открытия после закрытия", null=True, blank=True)

    objects = HealingObjectManager()

    def __unicode__(self):
        return self.name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    class Meta:
        verbose_name = u"объект здравоохранения"
        verbose_name_plural = u"объекты здравоохранения"
        permissions = (('viewall_healingobject', u"Просматривать полный писок МУ"),)


