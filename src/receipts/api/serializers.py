"""
This script converts data to JSON
and validates passed data
"""

from rest_framework import serializers
from receipts.models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = [
            'pk',
            'fiscal_drive_num',
            'fiscal_doc_num',
            'fiscal_sign'
        ]