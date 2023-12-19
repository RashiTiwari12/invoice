from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .serializers import UserSerializer, InvoiceSerializer, ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .data import *
import jwt

# Create your views here.


class UserSignUp(APIView):
    def post(self, request):
        data = request.data
        data["user_id"] = len(user_data) + 1
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user_data.append(serializer.data)
            return Response("Account has been created", status=201)
        return Response(serializer.errors, status=400)


class UserSignIn(APIView):
    def post(self, request):
        data = request.data
        for val in user_data:
            if val["email"] == data["email"] and val["password"] == data["password"]:
                token = jwt.encode(
                    {"user_id": val["user_id"], "email": data["email"]},
                    "secret",
                    algorithm="HS256",
                )
                return Response(
                    {"message": "Login succesful", "token": str(token)}, status=200
                )
        return Response("Email or password does not match", status=401)


class Invoiceview(APIView):
    def get(self, request):
        serializer = InvoiceSerializer(invoices_data, many=True).data
        return Response(serializer)

    def post(self, request):
        data = request.data
        data["invoice_id"] = len(invoices_data) + 1
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            invoices_data.append(serializer.data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SpecificInvoice(APIView):
    def get(self, request, id):
        for val in invoices_data:
            if val["invoice_id"] == id:
                serializer = InvoiceSerializer(val).data
                return Response(serializer)
        return Response({"message": "Invoice is not found"}, status=404)


class AddItemview(APIView):
    def post(self, request, invoice_id):
        for val in invoices_data:
            if val["invoice_id"] == invoice_id:
                data = request.data
                serializer = ItemSerializer(data=data)
                if serializer.is_valid():
                    val["items"].append(serializer.data)
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
        return Response({"message": "Invoice not found"}, status=404)
