from django.conf.urls import url
from .views import ReceiptRudView, ReceiptPostAPIView

urlpatterns = [
    url(r'^$', ReceiptPostAPIView.as_view(), name="post-create"),
    url(r'^(?P<pk>\d+)/$', ReceiptRudView.as_view(), name="post-rud")
]