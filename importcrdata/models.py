from django.core.validators import MinValueValidator, MaxValueValidator
from pymongo import MongoClient
from django.db import models
from django.conf import settings
import re


class PadronElectoral(models.Model):
    cedula = models.CharField(max_length=9)
    codele = models.CharField(max_length=6)
    sexo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    fechacaduc = models.CharField(max_length=8)
    junta = models.CharField(max_length=5)
    nombre_completo = models.CharField(max_length=150)

    class Meta:
        ordering = ['id']


class Distelec(models.Model):
    codele = models.CharField(max_length=6)
    provincia = models.CharField(max_length=50)
    canton = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50)

    def __str__(self):
        return "%s " % self.provincia




class MongoDB_DBMS:
    collection = None
    db = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)[settings.MONGO_DATABASE_NAME]

    def __init__(self, collection):
        self.collection = self.db[collection]

    def get_all(self):
        return self.collection.find()

    def limit(self, _limit=0):
        return self.collection.find().limit(_limit)

    def filter(self, **kwargs):
        kwargs = dict(map(self.format_filter_kwargs, zip(kwargs.keys(), kwargs.values())))
        return self.collection.find(kwargs)

    def format_filter_kwargs(self, key_value_pair):
        """
        :param key_value_pair: A tuple with a key and a value to format to be used in mongodb
        :return: Formated key_value_pair
        """
        special_indicator = "__"
        special_insensitive_indicator = "__i"
        value = key_value_pair[1]
        if special_indicator in key_value_pair[0]:
            if special_insensitive_indicator in key_value_pair[0]:
                key_pos = key_value_pair[0].find(special_insensitive_indicator)
                key = key_value_pair[0][:key_pos]
                operator = key_value_pair[0][key_pos+3:]
                if operator == "exact":
                    value = f"^{value}$"
                elif operator == "contains":
                    value = f"{value}"
                value = {"$regex": value, "$options": "i"}
                formatted_pair = (key, value)
            else:
                key_pos = key_value_pair[0].find(special_indicator)
                key = key_value_pair[0][:key_pos]
                operator = key_value_pair[0][key_pos+2:]
                if operator == "exact":
                    value = f"^{value}$"
                elif operator == "contains":
                    value = f"{value}"
                formatted_pair = (key, value)
                value = {"$regex": value}
            return formatted_pair
        return key_value_pair



class PostgreSQL_DBMS:
    model = None

    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def limit(self, _limit=0):
        return self.model.objects.all()[:_limit]

    def filter(self, **kwargs):
        return self.model.objects.filter(**kwargs)


class PadronElectoralFactory:
    dbms = None

    def __init__(self):
        if settings.USE_DATABASE == settings.AVAILABLE_DATABASES["postgresql"]:
            self.dbms = PostgreSQL_DBMS(PadronElectoral)
        elif settings.USE_DATABASE == settings.AVAILABLE_DATABASES["mongodb"]:
            self.dbms = MongoDB_DBMS("padron_electoral")
        else:
            raise ValueError(
                f"{settings.USE_DATABASE} is not a correct database option try using {settings.AVAILABLE_DATABASES}")
