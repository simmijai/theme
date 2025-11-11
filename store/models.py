from django.db import models

class HomeSlider(models.Model):
    title = models.CharField(max_length=150, default="Shop Our New Collection")
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='sliders/')
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower number = higher priority")

    class Meta:
        ordering = ['order']
        verbose_name = "Home Slider"
        verbose_name_plural = "Home Sliders"

    def __str__(self):
        return self.title
