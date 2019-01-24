from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from GoriberFitbit.api.serializers import UserSerializer, GroupSerializer
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse

from .forms import SignUpForm
from .tokens import account_activation_token


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        content = {
            'message': 'New project!'
        }
        return Response(content)


# Testing database models

class UserViewSet(viewsets.ModelViewSet):

    # Defines a 'queryset'
    queryset = User.objects.all().order_by('-date_joined')
    # Defines a 'serializer_class'
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            a = account_activation_token.make_token(user)
            b = urlsafe_base64_encode(force_bytes(user.pk)).decode()
            print(a, b)

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('email_auth/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': b,
                'token': a,
            })
            user.email_user(subject, message)

            return HttpResponse('Account activation link sent.')
    else:
        form = SignUpForm()
    return render(request, 'email_auth/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(uidb64, token)

    if user is not None and account_activation_token.check_token(user, token):
        print(user.is_active)
        user.is_active = True
        # user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return HttpResponse("Activation successful\n")
    else:
        return HttpResponse("The confirmation link was invalid, possibly because it has already been used.")

