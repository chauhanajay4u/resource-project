"""All Filtering Services"""
from user import models


class FilterService(object):
    """Service to filter admin panel table data"""

    @classmethod
    def filter_user(cls, request=None, queryset=None):
        """filter user based on query params"""

        # filter by student id
        id = request.query_params.get("id")
        if id:
            queryset = queryset.filter(id=id)

        # filter by student name
        name = request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        # filter by phone
        phone = request.query_params.get("phone")
        if phone:
            queryset = queryset.filter(phone__icontains=phone)

        # filter by email
        email = request.query_params.get("email")
        if email:
            queryset = queryset.filter(email__icontains=email)

        # filter by role
        role = request.query_params.get("role")
        if role:
            queryset = queryset.filter(role__icontains=role)

        # filter by graityde
        city = request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)

        # filter by country
        country = request.query_params.get("country")
        if country:
            queryset = queryset.filter(country__icontains=country)

        # sort by
        sort = request.query_params.get('sort', None)
        if sort is not None and (sort != ''):
            sort_list = sort.split(',')
            queryset = queryset.order_by(*sort_list)

        return queryset

    @classmethod
    def filter_resource(cls, request=None, queryset=None):
        """filter user resource based on query params"""

        # filter by resource id
        id = request.query_params.get("id")
        if id:
            queryset = queryset.filter(id=id)

        # filter by user id
        user_id = request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        # filter by student name
        name = request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        # filter by type
        type = request.query_params.get("type")
        if type:
            queryset = queryset.filter(type__icontains=type)

        # sort by
        sort = request.query_params.get('sort', None)
        if sort is not None and (sort != ''):
            sort_list = sort.split(',')
            queryset = queryset.order_by(*sort_list)

        return queryset