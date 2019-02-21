from django.forms import ModelForm

from core.models import ConfigurationModel


class ConfigurationForm(ModelForm):
    class Meta:
        model = ConfigurationModel
        fields = ['wait_time', 'scroll_count', 'scroll_delay']
