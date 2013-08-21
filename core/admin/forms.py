# coding=utf-8
from django.contrib.auth.models import User, Group
from django.forms import ModelForm, TextInput, forms, fields
from guardian.models import UserObjectPermission
from suit.widgets import EnclosedInput, AutosizedTextarea
from core.models import LegalEntity

__author__ = 'sergio'


class InfoForm(ModelForm):
    class Meta:
        widgets = {
            'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
        }


class HealingObjectForm(ModelForm):
    class Meta:
        widgets = {
            'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'full_name': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xxlarge'}),
            'name': TextInput(attrs={'class': 'input-xxlarge'}),
            'chief_original_name': TextInput(attrs={'class':'input-xxlarge'})
        }


class ServiceForm(InfoForm):
    class Meta:
        widgets = {
            'phone': EnclosedInput(prepend='icon-headphones'),
            'fax': EnclosedInput(prepend='icon-print'),
            'site_url': EnclosedInput(prepend='icon-globe'),
            'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'specialization': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'departments': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'chief_original_name': TextInput(attrs={'class':'input-xxlarge'})
        }


class NamedModelForm(ModelForm):
    class Meta:
        widgets = {
            'name': TextInput(attrs={'class': 'input-xxlarge'})
        }


user_manager_fieldset = (
    u"Управляющий пользователь", {
        'classes': ('suit-tab suit-tab-general',),
        'fields': (
            ('manager_user', 'user_password', 'send_email')
        )
    }
)


def get_user_manager_form(model_type, permission, group_name):
    class ManagerUserForm(ModelForm):
        user_password = fields.CharField(widget=fields.PasswordInput, required=False, label=u"Пароль")
        send_email = fields.BooleanField(label=u"Отправить письмо с реквизитами", required=False, help_text=u"После создания аккаунта пользователя, ему будет отправлено письмо с реквизитами (логином и паролем)")

        def _get_user(self, email=None):
            email = email or self.cleaned_data['manager_user']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return None

        def clean(self):
            cleaned_data = super(ManagerUserForm, self).clean()
            if not 'manager_user' in cleaned_data:
                return cleaned_data
            pwd = cleaned_data['user_password']
            u = self._get_user(cleaned_data['manager_user'])
            if not u and not pwd:
                raise forms.ValidationError(u"Вы пытаетесь создать нового пользователя (%s), для этого необходимо задать ему пароль" % cleaned_data['manager_user'])
            return cleaned_data

        def save(self, commit=True):
            e = super(ManagerUserForm, self).save(commit)
            # create user if not exists
            email = self.cleaned_data['manager_user']
            pwd = self.cleaned_data['user_password']
            send_email = self.cleaned_data['send_email']
            u = self._get_user()
            if not u:
                u = User.objects.create_user(email, email, pwd)
                u.is_staff = True
                u.is_active = True
                u.save()
                g = Group.objects.get(name=group_name)
                g.user_set.add(u)
                UserObjectPermission.objects.assign_perm(permission, u, e)
                if send_email:
                    # TODO Send email
                    pass
            return e

        class Meta:
            model = model_type

            widgets = {
                'chief_original_name': TextInput(attrs={'class': 'input-xxlarge'})
            }

    return ManagerUserForm
#
#
# class LegalEntityForm(ManagerUserForm):
#     #user_password = fields.CharField(widget=fields.PasswordInput, required=False, label=u"Пароль")
#     #send_email = fields.BooleanField(label=u"Отправить письмо с реквизитами", required=False, help_text=u"После создания аккаунта пользователя, ему будет отправлено письмо с реквизитами (логином и паролем)")
#
#     def _get_permission(self):
#         return 'change_legalentity'
#
#     class Meta:
#         model = LegalEntity
#         widgets = {
#             'chief_original_name': TextInput(attrs={'class':'input-xxlarge'})
#         }