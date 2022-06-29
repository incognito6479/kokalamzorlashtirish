from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import UserModel
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.template.defaultfilters import capfirst
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

from account.models import User

excluded_options = ["Маҳаллий админ", "Бош Aдмин"]


class AuthenticationUserForm(forms.Form):
    phone_number = PhoneNumberField()
    password = forms.CharField()

    error_messages = {
        "invalid_login": _("Телефон номер ёки Парол нотўғри киритилган"),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD
        )
        username_max_length = self.username_field.max_length or 254
        self.fields["phone_number"].max_length = username_max_length
        self.fields["phone_number"].widget.attrs[
            "maxlength"
        ] = username_max_length
        if self.fields["phone_number"].label is None:
            self.fields["phone_number"].label = capfirst(
                self.username_field.verbose_name
            )

    def clean(self):
        phone_number = self.cleaned_data.get("phone_number")
        password = self.cleaned_data.get("password")

        if phone_number is not None and password:
            self.user_cache = authenticate(
                self.request, phone_number=phone_number, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"phone_number": self.username_field.verbose_name},
        )


class UserUpdateForm(forms.ModelForm):
    old_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_("old_groups"),
            is_stacked=False,
            attrs={
                "id": "multiselect",
                "class": "form-control",
                "size": 9,
                "style": "height:200px",
                "multiple": True,
            },
        ),
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_("groups"),
            is_stacked=False,
            attrs={
                "id": "multiselect_to",
                "class": "form-control",
                "size": 9,
                "style": "height:200px",
                "multiple": True,
            },
        ),
    )

    class Meta:
        model = User
        fields = [
            "phone_number",
            "first_name",
            "last_name",
        ]
        labels = {
            "phone_number": _("Телефон рақами(логин)"),
            "first_name": _("Исми"),
            "last_name": _("Фамилияси"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "groups" in self.data:
            self.fields["groups"].queryset = Group.objects.filter(
                id__in=self.data.getlist("groups")
            )

        else:
            self.fields["groups"].queryset = self.instance.groups.all()
        if "old_groups" in self.data:
            self.fields["old_groups"].queryset = Group.objects.filter(
                id__in=self.data.getlist("old_groups")
            )
        else:
            self.fields["old_groups"].queryset = Group.objects.exclude(
                Q(user=self.instance) | Q(name__in=excluded_options)
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        with transaction.atomic():
            user.groups.set(self.cleaned_data["groups"])
            user.save()
            self.save_m2m()
        return user


class UserCreationForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": _("Иккита парол бир бирига мос келмади"),
    }
    password1 = forms.CharField(
        label=_("Парол"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label=_("Паролни тасдиқланг"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.exclude(name__in=excluded_options),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_("groups"),
            is_stacked=False,
            attrs={
                "id": "multiselect_to",
                "class": "form-control",
                "size": 9,
                "style": "height:200px",
                "multiple": True,
            },
        ),
    )

    class Meta:
        model = User
        fields = (
            "groups",
            "phone_number",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )
        field_classes = {"phone_number": PhoneNumberField}
        labels = {
            "groups": _("Гуруҳлар"),
            "phone_number": _("Телефон рақами(логин)"),
            "first_name": _("Исми"),
            "last_name": _("Фамилияси"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password2")

        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        with transaction.atomic():
            user.set_password(self.cleaned_data["password1"])
            user.save()
            self.save_m2m()
        return user


class SetPasswordForm(forms.ModelForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_("Янги Парол"), widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label=_("Янги паролни тасдиқланг"), widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        return password2

    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.instance.save()
        return self.instance
