from django.db import models

class Receipt(models.Model):
    fiscal_drive_num = models.IntegerField(blank=False, null=False, unique=True) # фн 16
    fiscal_doc_num = models.IntegerField(blank=False, null=False, unique=True) # фд 13 
    fiscal_sign = models.IntegerField(blank=False, null=False, unique=True) # фпд 13

    def __str__(self):
        return str(self.fiscal_drive_num)