from peewee import *

db = SqliteDatabase("report.db")


class Racer(Model):
    position = IntegerField()
    driver = CharField()
    car = CharField()
    start = DateTimeField()
    end = DateTimeField()
    time = CharField()
    disqualified = CharField()
    result = CharField()
    key = CharField(unique=True)

    class Meta:
        database = db
        table_name = 'Racers'
        order_by = ('position',)

