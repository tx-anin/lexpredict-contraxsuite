"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
# -*- coding: utf-8 -*-

import coreapi
import coreschema

# Third-party imports
from rest_framework import serializers, routers, viewsets, schemas
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
import rest_framework.views

# Django imports
from django.conf.urls import url
from django.db.models import Q

# Project imports
import apps.common.mixins
from apps.common.models import Action, AppVar, ReviewStatusGroup, ReviewStatus, MenuGroup, MenuItem
from apps.common.api.permissions import ReviewerReadOnlyPermission
from apps.users.api.v1 import UserSerializer

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2020, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.5.0/LICENSE"
__version__ = "1.5.0"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


# --------------------------------------------------------
# AppVar Views
# --------------------------------------------------------

class AppVarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVar
        fields = ('name',)


class AppVarAPIView(rest_framework.views.APIView):
    """
    Based on custom AppVar model storage
    """
    permission_classes = (ReviewerReadOnlyPermission,)

    @property
    def schema(self):
        if self.request.method == 'GET':
            fields = [
                coreapi.Field(
                    "name",
                    required=False,
                    location="query",
                    schema=coreschema.String(max_length=30)
                ),
                coreapi.Field(
                    "name_contains",
                    required=False,
                    location="query",
                    schema=coreschema.String(max_length=30)
                )]
        elif self.request.method == 'POST':
            fields = [
                coreapi.Field(
                    "params",
                    required=True,
                    location="body",
                    schema=coreschema.Object()
                )]
        else:
            fields = [
                coreapi.Field(
                    "name",
                    required=True,
                    location="body",
                    schema=coreschema.String(max_length=30)
                )]
        return schemas.ManualSchema(fields=fields)

    def get(self, request, *args, **kwargs):
        """
        Retrieve App Variable(s)\n
            Params:
                - name: str - retrieve specific variable
        """
        var_name = request.GET.get('name')
        name_contains = request.GET.get('name_contains')
        result = AppVar.objects.all()
        if var_name:
            result = result.filter(name=var_name)
            if not result.exists():
                return Response(status=404)
        if name_contains:
            result = result.filter(name__contains=name_contains)
            if not result.exists():
                return Response(status=404)
        result = {i['name']: i['value'] for i in result.values('name', 'value')}
        return Response(result)

    def post(self, request, *args, **kwargs):
        """
        Create or update App Variables\n
            Params:
                key1: val1,
                key2: val2, etc
        """
        data = request.data
        for var_name, value in data.items():
            AppVar.set(var_name, value)
        return Response('Application settings updated successfully.')

    def delete(self, request, *args, **kwargs):
        """
        Delete specific App Variable by name
            Param:
                - name: str
        """
        var_name = request.data.get('name')

        if not var_name:
            raise APIException('Provide variable name to delete')

        AppVar.clear(var_name)
        return Response('OK')


# --------------------------------------------------------
# ReviewStatusGroup Views
# --------------------------------------------------------

class ReviewStatusGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStatusGroup
        fields = ['pk', 'name', 'code', 'order', 'is_active']


class ReviewStatusGroupViewSet(apps.common.mixins.JqListAPIMixin, viewsets.ModelViewSet):
    """
    list: ReviewStatusGroup List
    retrieve: Retrieve ReviewStatusGroup
    create: Create ReviewStatusGroup
    update: Update ReviewStatusGroup
    partial_update: Partial Update ReviewStatusGroup
    delete: Delete ReviewStatusGroup
    """
    queryset = ReviewStatusGroup.objects.all()
    serializer_class = ReviewStatusGroupSerializer
    permission_classes = (ReviewerReadOnlyPermission,)


# --------------------------------------------------------
# ReviewStatus Views
# --------------------------------------------------------

class ReviewStatusSerializer(serializers.ModelSerializer):
    group_data = ReviewStatusGroupSerializer(source='group', many=False)

    class Meta:
        model = ReviewStatus
        fields = ['pk', 'name', 'code', 'order', 'group', 'group_data', 'is_active']


class ReviewStatusViewSet(apps.common.mixins.JqListAPIMixin, viewsets.ModelViewSet):
    """
    list: ReviewStatus List
    retrieve: Retrieve ReviewStatus
    create: Create ReviewStatus
    update: Update ReviewStatus
    partial_update: Partial Update ReviewStatus
    delete: Delete ReviewStatus
    """
    queryset = ReviewStatus.objects.select_related('group')
    serializer_class = ReviewStatusSerializer
    permission_classes = (ReviewerReadOnlyPermission,)


# --------------------------------------------------------
# Action Views
# --------------------------------------------------------

class ActionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Action
        fields = ['pk', 'name', 'user', 'content_type', 'object_pk', 'date',
                  'app_label', 'model_name', 'object_str']


class ActionViewSet(apps.common.mixins.JqListAPIMixin, viewsets.ModelViewSet):
    """
    list: Action List
    retrieve: Retrieve Action
    """
    http_method_names = ['get']
    queryset = Action.objects.all().select_related('user', 'user__role', 'content_type')
    serializer_class = ActionSerializer
    permission_classes = (ReviewerReadOnlyPermission,)


# --------------------------------------------------------
# MenuGroup Views
# --------------------------------------------------------

class MenuItemPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_superuser:
            return obj.user == request.user and not obj.public
        return True


class MenuGroupSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MenuGroup
        fields = ['pk', 'name', 'public', 'order', 'user']

    def validate_public(self, value):
        if not self.context['request'].user.is_superuser and value is True:
            raise ValidationError('Non-admin users cannot create public link groups.')
        return value


class MenuGroupViewSet(apps.common.mixins.APIFormFieldsMixin, viewsets.ModelViewSet):
    """
    list: MenuGroup List
    retrieve: Retrieve MenuGroup
    create: Create MenuGroup
    update: Update MenuGroup
    partial_update: Partial Update MenuGroup
    delete: Delete MenuGroup
    """
    permission_classes = (IsAuthenticated, MenuItemPermissions)
    serializer_class = MenuGroupSerializer

    def get_queryset(self):
        qs = MenuGroup.objects.all()
        if not self.request.user.is_superuser:
            qs = qs.filter(Q(public=False, user=self.request.user) |
                           Q(public=True))
        return qs


# --------------------------------------------------------
# MenuItem Views
# --------------------------------------------------------

class MenuItemSerializer(MenuGroupSerializer):

    class Meta:
        model = MenuItem
        fields = ['pk', 'name', 'url', 'group', 'public', 'order', 'user']


class MenuItemViewSet(MenuGroupViewSet):
    """
    list: MenuItem List
    retrieve: Retrieve MenuItem
    create: Create MenuItem
    update: Update MenuItem
    partial_update: Partial Update MenuItem
    delete: Delete MenuItem
    """
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        qs = MenuItem.objects.select_related('group')
        if not self.request.user.is_superuser:
            qs = qs.filter(Q(public=False, user=self.request.user) |
                           Q(public=True))\
                .filter(Q(group__public=False, group__user=self.request.user) |
                        Q(group__public=True) |
                        Q(group__isnull=True))
        return qs


router = routers.DefaultRouter()
router.register(r'actions', ActionViewSet, 'actions')
router.register(r'review-status-groups', ReviewStatusGroupViewSet, 'review-status-group')
router.register(r'review-statuses', ReviewStatusViewSet, 'review-status')
router.register(r'menu-groups', MenuGroupViewSet, 'menu-group')
router.register(r'menu-items', MenuItemViewSet, 'menu-item')

urlpatterns = [
    url(r'^app-variables/$', AppVarAPIView.as_view(),
        name='app-variables'),
]
