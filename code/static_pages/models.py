from django.core.validators import RegexValidator
from django.db import models

import markdown
from django.utils.translation import ugettext_lazy as _


class StaticPage(models.Model):
    SHORT_NAME_REGEX = "[a-zA-Z0-9\_\-]+"
    short_name = models.CharField(
        verbose_name=_("short name"),
        unique=True,
        max_length=255,
        validators=[RegexValidator('^{}$'.format(SHORT_NAME_REGEX))]
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    is_visible = models.BooleanField(
        verbose_name=_("visible"),
        default=True,
        help_text=_("Designate whether this type of requests can be created.")
    )
    text = models.TextField(
        verbose_name=_("text"),
        blank=True
    )

    @property
    def description_html(self):
        return markdown.markdown(self.text)

    def __str__(self):
        return self.name
