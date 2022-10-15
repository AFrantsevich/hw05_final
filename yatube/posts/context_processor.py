from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def get_context_data(request):
    form_aut = AuthenticationForm(request, data=request.POST)
    if form_aut.is_valid():
        auth.login(request, form_aut.get_user())
    context = {'form_aut': form_aut}
    return context
