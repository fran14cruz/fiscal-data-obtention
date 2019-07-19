from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect

from pages.forms import ReceiptForm
from django.views.generic import TemplateView
#from rest_framework.generics import CreateAPIView
#from receipts.models import Receipt
from rest_framework import generics
from receipts.models import Receipt
import json

def home_view(request, *args, **kwargs):
    #return HttpResponse("<p>こんにちは！<br>This is the Receipt server!</p>")
    return render(request, "home.html", {})

#def post_receipt(request, *args, **kwargs):
#    return render(request, "post.html")

class ReceiptView(TemplateView):
    template_name = 'post.html'

    def get(self, request):
        form = ReceiptForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        #if request.method == "POST":
        #    print(request.POST)
        form = ReceiptForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            form = ReceiptForm()

            args = {'form': form, 'text': text}
            #json_data = jason.loads(request.body)
            #return StreamingHttpResponse(str(json_data))
            return render(request, self.template_name, args)
        #else:
        #    return redirect('/')
