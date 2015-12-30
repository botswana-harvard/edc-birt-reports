from django.core.exceptions import ValidationError
from django.db import models

from edc_base.model.models import BaseModel

from ..choices import PARAM_TYPES
from ..models import BaseReport
from ..validators import start_with_model


class ReportParameter(BaseModel):

    report = models.ForeignKey(BaseReport)

    is_active = models.BooleanField(default=False)

    parameter_name = models.CharField(
        verbose_name=("parameter name"),
        max_length=25)

    parameter_type = models.CharField(
        verbose_name=("parameter type"),
        max_length=25,
        choices=PARAM_TYPES)

    is_selectfield = models.BooleanField(
        verbose_name=("is selectfield"),
        default=False,
        help_text='Allows multiple selects')

    app_name = models.CharField(
        verbose_name=("application"),
        max_length=35,
        blank=True,
        null=True,
        help_text='App that parameter exists in')

    model_name = models.CharField(
        verbose_name=("model"),
        max_length=35,
        blank=True,
        null=True,
        help_text='Model that parameter exists in')

    query_string = models.CharField(
        verbose_name=("query string"),
        max_length=200,
        validators=[start_with_model, ],
        blank=True,
        null=True,
        help_text='Always start query set with \'Model.\'')

    def save(self, *args, **kwargs):
        if self.is_selectfield:
            if not self.app_name:
                raise ValidationError('Application must be filled if is_selectfield=True')
            if not self.model_name:
                raise ValidationError('Model must be filled if is_selectfield=True')
            if not self.query_string:
                raise ValidationError('Query string must be filled if is_selectfield=True')
        super(ReportParameter, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{0} of {1}'.format(
            self.report.report_name,
            self.parameter_name)

    class Meta:
        app_label = 'bhp_birt_reports'
        unique_together = ('report', 'parameter_name')
