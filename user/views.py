from django.shortcuts import render
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from user.utils import error_wrapper
from user.decorators import session_authorize, catch_exception
from user.services.filter_service import FilterService
from user import models

# Create your views here.



class UserLogin(APIView):
    """Login for User"""
    @catch_exception()
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            return Response(response,
                            status=status.HTTP_200_OK)
        return Response({'error': error_wrapper(serializer.errors)},
                        status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    @catch_exception()
    @session_authorize(user_id_key="user_id")
    def post(self, request, auth_data):
        """Post details to create new User"""
        if auth_data.get("authorized"):
            serializer = serializers.UserLogoutSerializer(
                data=request.data)
            if serializer.is_valid():
                response = serializer.save(
                    session_token=auth_data.get("session_token"),
                    user_id=auth_data.get("user_id"))
                return Response(response, status=status.HTTP_200_OK)
            return Response({'error': error_wrapper(serializer.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistration(APIView):
    """Sign Up API for User"""
    @catch_exception()
    def post(self, request):
        """Post User details"""
        serializer = serializers.UserRegistrationSerializer(
            data=request.data)
        if serializer.is_valid():
            response = serializer.save(role="user", is_admin=False)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'error': error_wrapper(serializer.errors)},
                            status=status.HTTP_400_BAD_REQUEST)


class AdminUser(APIView):

    @catch_exception()
    @session_authorize(user_id_key="admin_id")
    def post(self, request, auth_data):
        """Post details to create new User"""
        if auth_data.get("authorized") and auth_data.get("is_admin"):
            serializer = serializers.UserRegistrationSerializer(
                data=request.data)
            if serializer.is_valid():
                response = serializer.save(role=None, is_admin=True)
                return Response(response, status=status.HTTP_201_CREATED)
            return Response({'error': error_wrapper(serializer.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        """Get queryset for User list"""
        queryset = models.User.objects.all()
        return queryset

    @catch_exception()
    @session_authorize("admin_id")
    def get(self, request, auth_data):
        """Get User List API"""
        if auth_data.get("authorized") and auth_data.get("is_admin"):
            queryset = self.get_queryset()

            # filtering queryset depending upon request
            queryset = FilterService().filter_user(
                request=self.request, queryset=queryset)
            count = queryset.count()

            # limiting queryset according to page number
            page = request.GET.get("page")
            if not page:
                page = 1

            page_size = request.GET.get("page_size")
            if not page_size:
                # setting default page count to 50
                page_size = 50
            limit = (int(page) - 1) * int(page_size)
            queryset = queryset[limit: limit + int(page_size)]

            serializer = serializers.UserListSerializer(
                queryset, many=True)

            response = {
                "count": count,
                "results": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class AdminModifyUser(APIView):

    @catch_exception()
    @session_authorize(user_id_key="admin_id")
    def delete(self, request, auth_data, user_id):
        """Delete User"""
        if auth_data.get("authorized") and auth_data.get("is_admin"):
            user = models.User.objects.filter(id=user_id)
            if user:
                user.delete()
                return Response({"message": "User Deleted Successfully"}, 
                    status=status.HTTP_200_OK)
            return Response({'error': 'User Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception()
    @session_authorize(user_id_key="admin_id")
    def patch(self, request, auth_data, user_id):
        """Post details to create new User"""
        if auth_data.get("authorized") and auth_data.get("is_admin"):
            serializer = serializers.AdminModifyUserSerializer(
                data=request.data)
            if serializer.is_valid():
                response = serializer.save(user_id=user_id)
                return Response(response, status=status.HTTP_200_OK)
            return Response({'error': error_wrapper(serializer.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
