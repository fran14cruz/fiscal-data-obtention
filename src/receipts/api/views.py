from rest_framework import generics
from receipts.models import Receipt
from .serializers import ReceiptSerializer

from django.http import JsonResponse

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

        status = True
        response_data = {
            "status": str(status),
            "receipt": serializer.data
        }
        return JsonResponse(response_data, status=201)

class ReceiptRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipt.objects.all()
