from peewee import *

mysql_db = MySQLDatabase('xxxxxxx', user='root', password='xxxxxx',
                         host='127.0.0.1', port=3306)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = mysql_db

class Order(BaseModel):
    Id = IntegerField(primary_key=True)
    OrderText = TextField()
    IsComplete = BooleanField(default=False)
    PanelId = IntegerField()
    MessageId = IntegerField()
    PanelProduct = TextField()
    UserId = TextField()
    IsReplied = BooleanField(default=False)

    class Meta:
        db_table = 'order'
