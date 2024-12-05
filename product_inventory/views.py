from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from product_inventory.models import Products, User
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.viewsets import ViewSet
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.permissions import AllowAny


from product_inventory import models
from product_inventory.serializers import UserSerializer, AuthTokenSerializer


@api_view(['GET'])
def products_view(Request,productid):
    try:
        product_object = models.Products.objects.get(product_id=productid)
        if product_object.quantity > 0:
            product_object.quantity -= 1
            product_object.save()
            data = {'message':'success!'}
            return Response(data)
        else:
            data = {'message':'Out of stock!'}
            return Response(data)
    except Products.DoesNotExist:
        data = {'message': 'product does not exist'}
        return Response(data)


class UserCreationView(ViewSet):
    permission_classes = [AllowAny]
    @action(methods=['POST'], detail=False)
    def create_user(self,request):
        serializer = UserSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'user created'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class OAuth2TokenViewSet(ViewSet):

    @action(methods=['POST'], detail=False)
    def create_token(self,request):
        print("Authentication Classes:", self.authentication_classes)
        serializer = AuthTokenSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            user= serializer.validated_data['user']

            application = Application.objects.first()

            access_token = AccessToken.objects.create(
                user=user,
                application=application,
                expires=now() + timedelta(hours=1),
                scope='read write',
            )

            return Response({
                'access_token':access_token.token,
                'expires_in': 3600,
                'token_type': 'Bearer',
                'scope': access_token.scope,
            }, status=201)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



