# accounts/views.py

from django.shortcuts       import render, redirect
from django.contrib.auth    import login
from django.contrib.auth.forms import UserCreationForm
from django.urls            import reverse_lazy
from django.conf            import settings
from allauth.account.views  import PasswordChangeView

from orders.emails import send_account_update_notification  # ← import the helper

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class NotifyPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url   = reverse_lazy('account_password_change_done')

    def form_valid(self, form):
        # Let allauth perform the password change
        response = super().form_valid(form)

        # ─── send notification email ─────────────────────────────
        send_account_update_notification(self.request.user)
        # ─────────────────────────────────────────────────────────

        return response

