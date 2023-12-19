from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("signup/", csrf_exempt(UserSignUp.as_view()), name="user-signup"),
    path("invoices/", csrf_exempt(Invoiceview.as_view()), name="invoices"),
    path(
        "invoices/<int:id>/",
        csrf_exempt(SpecificInvoice.as_view()),
        name="specific-invoices",
    ),
    path(
        "invoices/<int:invoice_id>/items",
        csrf_exempt(AddItemview.as_view()),
        name="add-item",
    ),
    path("login/", csrf_exempt(UserSignIn.as_view()), name="user-signin"),
]
