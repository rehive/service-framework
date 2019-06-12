import uuid

from rehive import Rehive, APIException
from rest_framework import serializers
from django.db import transaction

from {{cookiecutter.module_name}}.models import Company, User


class ActivateSerializer(serializers.Serializer):
    """
    Serialize the activation data, should be a token that represents an admin
    user.
    """

    token = serializers.CharField(write_only=True)
    id = serializers.CharField(source='identifier', read_only=True)
    name = serializers.CharField(read_only=True)
    secret = serializers.UUIDField(read_only=True)

    def validate(self, validated_data):
        token = validated_data.get('token')
        rehive = Rehive(token)

        try:
            user = rehive.auth.tokens.verify(token)
            groups = [g['name'] for g in user['groups']]
            if len(set(["admin", "service"]).intersection(groups)) <= 0:
                raise serializers.ValidationError(
                    {"token": ["Invalid admin user."]})
        except APIException:
            raise serializers.ValidationError({"token": ["Invalid user."]})

        try:
            company = rehive.admin.company.get()
        except APIException:
            raise serializers.ValidationError({"token": ["Invalid company."]})

        if Company.objects.filter(
                identifier=company['id'],
                active=True).exists():
            raise serializers.ValidationError(
                {"token": ["Company already activated."]})

        validated_data['user'] = user
        validated_data['company'] = company

        return validated_data

    @transaction.atomic
    def create(self, validated_data):
        token = validated_data.get('token')
        rehive_user = validated_data.get('user')
        rehive_company = validated_data.get('company')

        # Activate an existing company.
        try:
            company = Company.objects.get(
                identifier=rehive_company.get('id')
            )
        # Ceate a new company and activate it.
        except Company.DoesNotExist:
            with transaction.atomic():
                user = User.objects.create(
                    token=token,
                    identifier=uuid.UUID(rehive_user['id'])
                )
                company = Company.objects.create(
                    admin=user,
                    identifier=rehive_company.get('id'),
                    name=rehive_company.get('name')
                )
            user.company = company
            user.save()
        else:
            company.admin.token = token
            company.active = True
            company.admin.save()
            company.save()

        return company


class DeactivateSerializer(serializers.Serializer):
    """
    Serialize the deactivation data, should be a token that represents an admin
    user.
    """
    token = serializers.CharField(write_only=True)

    def validate(self, validated_data):
        token = validated_data.get('token')
        rehive = Rehive(token)

        try:
            user = rehive.auth.tokens.verify(token)
            groups = [g['name'] for g in user['groups']]
            if len(set(["admin", "service"]).intersection(groups)) <= 0:
                raise serializers.ValidationError(
                    {"token": ["Invalid admin user."]})
        except APIException:
            raise serializers.ValidationError({"token": ["Invalid user."]})

        try:
            validated_data['company'] = Company.objects.get(
                identifier=user['company'])
        except Company.DoesNotExist:
            raise serializers.ValidationError(
                {"token": ["Company has not been activated yet."]})

        return validated_data

    def delete(self):
        company = self.validated_data['company']
        company.active = False
        company.admin.token = None
        company.save()
        company.admin.save()



class AdminCompanySerializer(serializers.ModelSerializer):
    """
    Serialize company, update and delete.
    """
    id = serializers.CharField(source='identifier', read_only=True)
    secret = serializers.UUIDField(read_only=True)
    name = serializers.CharField()

    class Meta:
        model = Company
        fields = ('id', 'identifier', 'secret', 'name',)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
