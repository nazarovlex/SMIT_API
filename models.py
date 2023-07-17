from tortoise import fields
from tortoise.models import Model


class Tariff(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    cargo_type = fields.CharField(max_length=255)
    rate = fields.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        table = "tariff"
        unique_together = [("date", "cargo_type")]
