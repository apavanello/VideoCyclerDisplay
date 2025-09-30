from django.db import models

# Create your models here.
from django.db import models

class DisplayItem(models.Model):
    # Opções para o tipo de mídia
    MEDIA_TYPE_CHOICES = (
        ('video', 'Vídeo'),
        ('image', 'Imagem'),
    )

    title = models.CharField(max_length=200, help_text="O título")
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='display_media/')
    duration_in_seconds = models.PositiveIntegerField(
        default=10,
        help_text="Apenas para imagens. Define por quantos segundos a imagem será exibida."
    )
    order = models.PositiveIntegerField(default=0, help_text="Define a ordem de exibição.")
    mute = models.BooleanField(default=True, help_text="Apenas para vídeos. Define se o vídeo será reproduzido sem som.")

    def __str__(self):
        return f"{self.get_media_type_display()}: {self.title}"

    class Meta:
        ordering = ['order']