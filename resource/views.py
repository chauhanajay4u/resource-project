from django.shortcuts import render
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from . import serializers
from user.utils import error_wrapper
from user.decorators import session_authorize, catch_exception
from user.services.filter_service import FilterService
from . import models
from user.utils import NotAcceptableError


class AdminUserResource(GenericAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.AdminResourceListSerializer
        elif self.request.method == 'POST':
            return serializers.AdminCreateUserResourceSerializer
        return None

    @catch_exception()
    @session_authorize(user_id_key="admin_id")
    def post(self, request, auth_data):
        """Post details to create new User resource"""
        if auth_data.get("authorized") and auth_data.get("is_admin"):
            serializer = serializers.AdminCreateUserResourceSerializer(
                data=request.data)
            if serializer.is_valid():
                response = serializer.save()
                return Response(response, status=status.HTTP_200_OK)
            return Response({'error': error_wrapper(serializer.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        """Get queryset for User list"""
        queryset = models.Resources.objects.filter(
            is_active=True).order_by("-id")
        return queryset

    @catch_exception()
    @session_authorize("admin_id")
    def get(self, request, auth_data):
        """Get User List API"""
        if auth_data.get("authorized") and auth_data.get("is_admin"):
            queryset = self.get_queryset()

            # filtering queryset depending upon request
            queryset = FilterService().filter_resource(
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

            serializer = serializers.AdminResourceListSerializer(
                queryset, many=True)

            response = {
                "count": count,
                "results": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception()
    @session_authorize(user_id_key="admin_id")
    def delete(self, request, auth_data):
        """Delete User"""
        if auth_data.get("authorized") and auth_data.get("is_admin"):
            resource_id = request.query_params.get("resource_id")
            if not resource_id:
                raise NotAcceptableError("Please provide resource ID", status=400)
            resource = models.Resources.objects.filter(id=resource_id)
            if resource:
                resource.delete()
                return Response({"message": "User Resource Deleted Successfully"}, 
                    status=status.HTTP_200_OK)
            return Response({'error': 'Resource Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class UserResource(GenericAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.UserResourceListSerializer
        elif self.request.method == 'POST':
            return serializers.CreateUserResourceSerializer
        return None

    @catch_exception()
    @session_authorize(user_id_key="user_id")
    def post(self, request, auth_data):
        """Post details to create new User resource"""
        if auth_data.get("authorized"):
            serializer = serializers.CreateUserResourceSerializer(
                data=request.data)
            if serializer.is_valid():
                response = serializer.save(
                    user_id=auth_data.get("user_id"))
                return Response(response, status=status.HTTP_200_OK)
            return Response({'error': error_wrapper(serializer.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self, user_id):
        """Get queryset for User list"""
        queryset = models.Resources.objects.filter(
            user_id=user_id,
            is_active=True).order_by("-id")
        return queryset

    @catch_exception()
    @session_authorize("user_id")
    def get(self, request, auth_data):
        """Get User List API"""
        if auth_data.get("authorized"):
            queryset = self.get_queryset(user_id=auth_data.get("user_id"))

            # filtering queryset depending upon request
            queryset = FilterService().filter_resource(
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

            serializer = serializers.UserResourceListSerializer(
                queryset, many=True)

            response = {
                "count": count,
                "results": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception()
    @session_authorize(user_id_key="user_id")
    def delete(self, request, auth_data):
        """Delete User"""
        if auth_data.get("authorized"):
            resource_id = request.query_params.get("resource_id")
            if not resource_id:
                raise NotAcceptableError("Please provide resource ID", status=400)
            resource = models.Resources.objects.filter(
                user_id=auth_data.get("user_id"),
                id=resource_id)
            if resource:
                resource.delete()
                return Response({"message": "Resource Deleted Successfully"}, 
                    status=status.HTTP_200_OK)
            return Response({'error': 'Resource Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
