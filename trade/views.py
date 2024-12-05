from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Trade
from .serializers import TradeSerializer

# Create your views here.

class TradeViewSet(ViewSet):

    @action(['POST'],detail=False)
    def create_trade(self,request):
        serializer = TradeSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(data = {"message":"trade data saved"}, status=status.HTTP_201_CREATED)
        return Response(data={"message":"trade data saved"}, status=status.HTTP_400_BAD_REQUEST)

    @action(['GET'],detail=True)
    def get_trade(self,request,pk=None):
        """Handles retrieving a specific trade ID."""
        try:
            trade = Trade.objects.get(pk=pk)
        except Trade.DoesNotExist:
            return Response(data={"error":"Trade not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TradeSerializer(trade)
        return Response(data=serializer.data, status= status.HTTP_200_OK)

