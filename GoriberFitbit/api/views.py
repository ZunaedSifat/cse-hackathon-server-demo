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

from GoriberFitbit.api.serializers import *
from .forms import SignupForm
from .tokens import account_activation_token
from .models import Profile


class Home(APIView):

    # Checks for token
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        print(str(request.META))
        content = {
            'user_id': request.user.id,
            'username': request.user.username,
            'message': 'New project!'
        }
        # serializer_class =
        return Response(content)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        profile = Profile.objects.filter(user_id=request.user.id).first()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class LeaderBoardView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        profiles = Profile.objects.order_by('-score')[:5]

        context = {}
        for (i, p) in enumerate(profiles):
            context[i+1] = {
                "username": p.user.username,
                "score": p.score
            }
        return Response(context)


class SessionData(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        # print(type(request.data))
        dic = request.data
        print(request.POST)
        print(type(dic))
        print(dic['distance'])

        try:
            session = Session(
                user_id=request.user.id,
                distance=dic['distance'],
                leap_count=dic['leap_count'],
                start_time=dic['start_time'],
                end_time=dic['end_time']
            )
            session.save()
            return Response({"detail": "success"})
        except Exception as e:
            return Response({"detail": str(e)})


class HeartData(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        # print(type(request.data))
        dic = request.data

        try:
            heartdata = HeartRate(
                user_id=request.user.id,
                bpm=dic['bpm'],
                timestamp=dic['timestamp']
            )
            heartdata.save()
            return Response({"detail": "success"})
        except Exception as e:
            return Response({"detail": str(e)})


class Signup(APIView):

    @staticmethod
    def post(request):
        print(type(request.data))
        # dic = json.loads(request.data)
        dic = request.data
        form = SignupForm(dic)

        if form.is_valid():

            # Checking if username already exists
            if User.objects.filter(username=form.cleaned_data['username']).first() is not None:
                return Response({"detail": "Username already exists"})

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
            link = 'https://csehackathon.tahmeedtarek.com/activate/' + uid + '/' + token + '/'
            send_mail(
                'Did you signup?',
                'Thank you for signing up! Click the link below: \n' +
                link,
                'Goriber Fitbit <teamhariyegiyechi@gmail.com>',
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
