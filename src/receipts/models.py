from django.db import models

class Receipt(models.Model):
    fiscal_drive_num = models.IntegerField(blank=False, null=False) # фн 16
    fiscal_doc_num = models.IntegerField(blank=False, null=False) # фд 13 
    fiscal_sign = models.IntegerField(blank=False, null=False) # фпд 13
