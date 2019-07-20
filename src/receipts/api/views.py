from rest_framework import generics
from receipts.models import Receipt
from .serializers import ReceiptSerializer
from django.http import JsonResponse

# Import modules
import sys
sys.path.insert(0, '/Users/a1/desktop/practice2019/receipt-rest/Nikita/')
sys.path.insert(0, '/Users/a1/desktop/practice2019/receipt-rest/Roman/')
from receipt import get, save
from API_OFD import get_data

class ReceiptPostAPIView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipt.objects.all() 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        fields = request.data
        fields_list = list(fields.values())

        # Check if receipt is in database
        db_receipt = get(fields_list[0], fields_list[1], fields_list[2])
        ofd_receipt = {}
        status = False
        if not db_receipt:
            # Check if receipt is in ОФД
            ofd_receipt = get_data(fields_list[0], fields_list[1], fields_list[2])
            if ofd_receipt:
                # Save receipt to database
                save(ofd_receipt)
                status = True

        response_data = {
            "status": str(status),
            "receipt": ofd_receipt #serializer.data
        }
        return JsonResponse(response_data, status=201)

class ReceiptRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipt.objects.all()
