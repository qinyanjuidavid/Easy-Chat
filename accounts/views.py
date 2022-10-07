from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def registration_view(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account was successfully created for "
                + form.cleaned_data.get("username"),
            )
            # redirect to login page
            return redirect("accounts:login")
    else:
        form = UserCreationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)
