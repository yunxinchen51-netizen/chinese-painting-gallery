from django.db import models


class LayoutSettings(models.Model):
    """Shared layout offsets used by the visual layout editor."""

    key = models.CharField(max_length=100, unique=True, default='gallery-layout-positions')
    positions = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
