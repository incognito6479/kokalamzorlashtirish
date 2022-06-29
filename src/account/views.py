from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import (
    AuthenticationUserForm,
    SetPasswordForm,
    UserCreationForm,
    UserUpdateForm,
)
from .models import Organization, User


class LoginUserView(LoginView):
    template_name = "account/login.html"
    redirect_authenticated_user = True
    form_class = AuthenticationUserForm


class LogoutUserView(LogoutView):
    template_name = "account/login.html"


class OrganizationViewList(PermissionRequiredMixin, ListView):
    permission_required = "account.view_organization_admin"
    paginate_by = settings.ORGANIZATION_PAGE_SIZE
    template_name = "account/organization-list.html"
    queryset = Organization.objects.get_organizations()


class CreateUserView(PermissionRequiredMixin, CreateView):
    permission_required = "account.add_user"
    template_name = "account/user-create.html"
    model = User
    success_url = reverse_lazy("account:list")
    form_class = UserCreationForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


class UpdateUserView(PermissionRequiredMixin, UpdateView):
    permission_required = "account.change_user"
    template_name = "account/change.html"
    model = User
    success_url = reverse_lazy("account:list")
    form_class = UserUpdateForm


class ListUserView(PermissionRequiredMixin, ListView):
    permission_required = "account.change_user"
    template_name = "account/list.html"
    paginate_by = settings.USER_PAGE_SIZE

    def get_queryset(self):
        return User.objects.get_all_users_by_organization(
            user=self.request.user
        )


class UpdateUserPassword(PermissionRequiredMixin, UpdateView):
    permission_required = "account.change_user"
    model = User
    template_name = "account/user-password-update.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("account:list")
