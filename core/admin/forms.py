# coding=utf-8
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.forms import ModelForm, TextInput, forms, fields
from django.template import Context
from django.template.loader import get_template
from guardian.models import UserObjectPermission
from selectable.forms import AutoCompleteSelectWidget
from core.admin.lookups import LegalEntityLookup, AddressObjectLookup, HealingObjectLookup, StreetLookup

__author__ = 'sergio'


class InfoForm(ModelForm):
    class Meta:
        widgets = {
            #'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
        }


class HealingObjectForm(ModelForm):
    class Meta:
        widgets = {
            #'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            #'full_name': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xxlarge'}),
            'name': TextInput(attrs={'class': 'vLargeTextField'}),
            'chief_original_name': TextInput(attrs={'class': 'vLargeTextField'})
        }


class ServiceForm(InfoForm):
    class Meta:
        widgets = {
            # 'phone': EnclosedInput(prepend='icon-headphones'),
            # 'fax': EnclosedInput(prepend='icon-print'),
            # 'site_url': EnclosedInput(prepend='icon-globe'),
            # 'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            # 'specialization': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            # 'departments': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'chief_original_name': TextInput(attrs={'rows': 1, 'class': 'vLargeTextField'}),
            'healing_object': AutoCompleteSelectWidget(lookup_class=HealingObjectLookup)
        }


class NamedModelForm(ModelForm):
    class Meta:
        widgets = {
            'name': TextInput(attrs={'class': 'vLargeTextField'})
        }


class AddressObjectForm(ModelForm):
    class Meta:
        widgets = {
            'street': AutoCompleteSelectWidget(lookup_class=StreetLookup)
        }

user_manager_fields = ('manager_user', 'user_password', 'send_email')
user_manager_fieldset = (
    u"Управляющий пользователь", {
        'classes': ('suit-tab suit-tab-general', 'grp-collapse grp-closed'),
        'fields': (user_manager_fields,)
    }
)


def get_user_manager_form(model_type, permission, group_name, email_subject, email_template_name):
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
            manager_user = cleaned_data['manager_user']
            if manager_user:
                u = self._get_user(manager_user)
                if not u and not pwd:
                    raise forms.ValidationError(u"Вы пытаетесь создать нового пользователя (%s), для этого необходимо задать ему пароль" % cleaned_data['manager_user'])
            return cleaned_data

        def save(self, commit=True):
            e = super(ManagerUserForm, self).save(commit)
            # create user if not exists
            email = self.cleaned_data.get('manager_user')
            pwd = self.cleaned_data.get('user_password')
            should_send_email = self.cleaned_data.get('send_email')
            if email:
                u = self._get_user()
                if not u:
                    u = User.objects.create_user(email, email, pwd)
                    u.is_staff = True
                    u.is_active = True
                    u.save()
                    if should_send_email:
                        body = get_template(email_template_name).render(Context({
                            'user': u,
                            'password': pwd,
                            'entity': e,
                            'base_url': Site.objects.get_current().domain
                        }))
                        email = EmailMessage(
                            subject=email_subject,
                            body=body,
                            from_email=DEFAULT_FROM_EMAIL,
                            to=[u.email])
                        email.content_subtype = "html"
                        email.send(fail_silently=True)

                try:
                    g = Group.objects.get(name=group_name)
                    g.user_set.add(u)
                    UserObjectPermission.objects.assign_perm(permission, u, e)
                except:
                    pass
            return e

        class Meta:
            model = model_type

            widgets = {
                'chief_original_name': TextInput(attrs={'class': 'vLargeTextField'}),
                'legal_entity': AutoCompleteSelectWidget(lookup_class=LegalEntityLookup),
                'address': AutoCompleteSelectWidget(lookup_class=AddressObjectLookup),
                'jur_address': AutoCompleteSelectWidget(lookup_class=AddressObjectLookup),
                'fact_address': AutoCompleteSelectWidget(lookup_class=AddressObjectLookup),
                'parent': AutoCompleteSelectWidget(lookup_class=HealingObjectLookup)
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