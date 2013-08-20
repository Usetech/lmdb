# coding=utf-8
from django.core.management import BaseCommand

from django.db import connection
from django.db import transaction
from core.models import AddressObject, DistrictObject, StreetObject, ServiceType, HealingObject, LegalEntity, Position, HealthObjectType, Service

__author__ = 'pparkhomenko'


class Command(BaseCommand):
    help = "Create full data view"

    __address_view = "core_whole_address"
    __full_view = "core_full"
    __disabled_fields = {u"created_at", u"modified_at", u"deleted_at"}

    def handle(self, *args, **options):
        transaction.enter_transaction_management()
        cursor = connection.cursor()
        cursor.execute("DROP VIEW IF EXISTS core_whole_address CASCADE")
        cursor.execute("DROP VIEW IF EXISTS core_whole_data CASCADE")
        cursor.close()
        address_fields = self.create_whole_address_view(connection)
        self.create_full_view(connection, address_fields)
        transaction.commit()

    def retrieve_fields(self, connection, table, exclude):
        cursor = connection.cursor();
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", [table, ])
        rows = cursor.fetchall();
        fields = []
        for row in rows:
            field = row[0]
            if not field in self.__disabled_fields and not field in exclude:
                fields.append(field)
        cursor.close()
        return fields

    def create_whole_address_view(self, connection):
        fields = []
        fields_string = ""
        address_table = AddressObject._meta.db_table
        address_fields = self.retrieve_fields(connection, address_table, {u"district_id", u"street_id"})
        district_table = DistrictObject._meta.db_table
        district_fields = self.retrieve_fields(connection, district_table, {})
        street_table = StreetObject._meta.db_table
        street_fields = self.retrieve_fields(connection, street_table, {})
        for field in address_fields:
            if field == u"id":
                field_alias = "_id"
            elif field == u"bsi_id":
                field_alias = "id"
            else:
                field_alias = field
            fields.append(field_alias)
            fields_string += "a." + field + " AS " + field_alias + ", "
        for field in district_fields:
            field_alias = "district_" + field
            fields.append(field_alias)
            fields_string += "d." + field + " AS " + field_alias + ", "
        for field in street_fields:
            field_alias = "street_" + field
            fields.append(field_alias)
            fields_string += "s." + field + " AS " + field_alias + ", "
        fields_string = fields_string.rstrip(", ")
        request = "CREATE VIEW " + self.__address_view + " AS SELECT " + fields_string + " FROM " + address_table +\
                  " AS a JOIN " + street_table + " AS s ON a.street_id = s.id JOIN " + district_table +\
                  " AS d ON a.district_id = d.id";
        #print request
        cursor = connection.cursor()
        cursor.execute(request)
        cursor.close()
        return fields

    def create_full_view(self, connection, address_fields):
        service_table = Service._meta.db_table
        service_alias = "service"
        service_prefix = "service_"
        service_fields = self.retrieve_fields(connection, service_table,
                                              {u"id", u"healing_object_id", u"service_id", u"chief_position_id"})
        tables = (
            {
                "name": ServiceType._meta.db_table,
                "alias": "st",
                "prefix": "servicetype_",
                "fields": self.retrieve_fields(connection, ServiceType._meta.db_table, {u"id",}),
                "outer": False,
                "condition": service_alias + ".service_id = st.id",
            },
            {
                "name": HealingObject._meta.db_table,
                "alias": "ho",
                "prefix": "healingobject_",
                "fields": self.retrieve_fields(connection, HealingObject._meta.db_table,
                                               {u"id", u"address_id", u"legal_entity_id", u"object_type_id",
                                                u"parent_id"}),
                "outer": False,
                "condition": service_alias + ".healing_object_id = ho.id",
            },
            {
                "name": LegalEntity._meta.db_table,
                "alias": "le",
                "prefix": "legalentity_",
                "fields": self.retrieve_fields(connection, LegalEntity._meta.db_table,
                                               {u"id", u"chief_position_id", u"jur_address_id", u"fact_address_id",}),
                "outer": False,
                "condition": "ho.legal_entity_id = le.id",
            },
            {
                "name": Position._meta.db_table,
                "alias": "scp",
                "prefix": service_prefix + "chief_position_",
                "fields": self.retrieve_fields(connection, Position._meta.db_table, {u"id",}),
                "outer": True,
                "condition": service_alias + ".chief_position_id = scp.id",
            },
            {
                "name": HealthObjectType._meta.db_table,
                "alias": "hot",
                "prefix": "healinobject_type_",
                "fields": self.retrieve_fields(connection, Position._meta.db_table, {u"id",}),
                "outer": False,
                "condition": "ho.object_type_id = hot.id",
            },
            {
                "name": self.__address_view,
                "alias": "hoa",
                "prefix": "healinobject_address_",
                "fields": address_fields,
                "outer": True,
                "condition": "ho.address_id = hoa._id",
            },
            {
                "name": self.__address_view,
                "alias": "leja",
                "prefix": "legalentity_jur_address_",
                "fields": address_fields,
                "outer": True,
                "condition": "le.jur_address_id = leja._id",
            },
            {
                "name": self.__address_view,
                "alias": "lefa",
                "prefix": "legalentity_fact_address_",
                "fields": address_fields,
                "outer": True,
                "condition": "le.fact_address_id = lefa._id",
            },
            {
                "name": Position._meta.db_table,
                "alias": "lecp",
                "prefix": "legalentity_chief_position_",
                "fields": self.retrieve_fields(connection, Position._meta.db_table, {u"id",}),
                "outer": True,
                "condition": service_alias + ".chief_position_id = scp.id",
            },
        )

        fields_string = ""
        for field in service_fields:
            fields_string += service_alias + "." + field + " AS " + service_prefix + field + ", "

        join_string = ""
        for table in tables:
            alias = table["alias"]
            for field in table["fields"]:
                if not field.startswith(u"_"):
                    fields_string += alias + "." + field + " AS " + table["prefix"] + field + ", "
            if table["outer"]:
                join_string += " LEFT OUTER"
            join_string += " JOIN " + table["name"] + " " + alias + " ON " + table["condition"]

        fields_string = fields_string.rstrip(", ")
        request = "CREATE VIEW " + self.__full_view + " AS SELECT " + fields_string + " FROM " + service_table + " " +\
                  service_alias + join_string
        #print request
        cursor = connection.cursor()
        cursor.execute(request)
        cursor.close()
