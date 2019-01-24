from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from GoriberFitbit.api.serializers import UserSerializer, GroupSerializer
from .forms import SignupForm
from .tokens import account_activation_token


class Home(APIView):

    # Checks for token
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        content = {
            'message': 'New project!'
        }
        return Response(content)


class Signup(APIView):

    @staticmethod
    def post(request):
        form = SignupForm(request.POST)

        if form.is_valid():

            # Checking if username already exists
            if User.objects.filter(username=form.cleaned_data['username']).first() is not None:
                return Response({"message": "Username already exists"})

            # Adding user to the database
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
            )
            user.is_active = False
            user.save()

            # Generating token and sending it to user
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
            # todo: change link
            link = 'http://192.168.1.106:8000/activate/' + uid + '/' + token + '/'
            send_mail(
                'Did you signup?',
                'Thank you for signing up! Click the link below: \n' +
                link,
                'teamhariyegiyechi@gmail.com',
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return Response({"detail": "success"})

        else:
            return Response({"detail": "failure"})


class Activate(APIView):
    
    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None and account_activation_token.check_token(user, token):
            print(user.is_active)
            user.is_active = True
            # user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return HttpResponse("Activation successful.\n")
        else:
            return HttpResponse("The confirmation link was invalid, possibly because it has already been used.")


# Testing database models

class UserViewSet(viewsets.ModelViewSet):

    # Defines a 'queryset'
    queryset = User.objects.all().order_by('-date_joined')
    # Defines a 'serializer_class'
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
