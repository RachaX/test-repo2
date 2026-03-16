from pip._internal.utils import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import re
import os
from .service import ReportingService

from reporting.serializers import ReportSerializer

logger = logging.getLogger(__name__)


class ReportView(APIView):
    def post(self, request):

        # extract body data
        data = request.data

        print('Host: ', settings.EMAIL_HOST)
        print('PORT: ', settings.EMAIL_PORT)
        print('TLS: ', settings.EMAIL_USE_TLS)
        print('SSL: ', settings.EMAIL_USE_SSL)
        print('RECIPIENT: ', settings.EMAIL_RECIPIENT)
        print('HOST USER: ', settings.EMAIL_HOST_USER)
        print('HOST USER PASSWORD: ', settings.EMAIL_HOST_PASSWORD)

        serializer = ReportSerializer(data=data)
        if not serializer.is_valid():
            return Response({ 'error' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        # allowed customer contact methods
        contact_methods_allowed = ['email', 'phone_number']

        # required data
        user = data.get('user')
        contact_method = data.get('contact_method')
        contact_info = data.get('contact_info')
        msg = data.get('message')

        if user is None or contact_method is None or contact_info is None or msg is None:
            return Response({ 'error' : 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user or not contact_method or not contact_info or not msg:
            return Response('Invalid data provided.', status=status.HTTP_400_BAD_REQUEST)

        if contact_method not in contact_methods_allowed:
            return Response({ 'error' : 'Invalid contact method provided.' }, status=status.HTTP_400_BAD_REQUEST)

        # check if name correct entered
        name = user.split(' ')
        if len(name) < 2:
            return Response({ 'error' : 'Invalid contact name provided.' }, status=status.HTTP_400_BAD_REQUEST)

        if len(name[0]) < 3 or len(name[1]) < 3:
            return Response({ 'error' : 'Invalid contact name provided.' }, status=status.HTTP_400_BAD_REQUEST)

        if contact_method == 'email':
            is_valid = self.is_valid_email(contact_info)
            if not is_valid:
                return Response({ 'error' : 'Invalid mail contact address.' }, status=status.HTTP_400_BAD_REQUEST)

        if contact_method == 'phone_number':
            is_valid = self.is_valid_phone_number(contact_info)
            if not is_valid:
                return Response({ 'error' : 'Invalid phone number provided.' }, status=status.HTTP_400_BAD_REQUEST)


        context = {
            'user' : user,
            'contact_info' : contact_info,
            'message' : msg
        }

        sent_email = ReportingService.send_report(context, '../templates/email/reporting_template.html')

        if sent_email:
            return Response({ 'message' : 'Successfully sent email.'}, status=status.HTTP_200_OK)
        else :
            return Response({ 'message' : 'Failed to send email.'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_phone_number(phone_number):
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone_number))
