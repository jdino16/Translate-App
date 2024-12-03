from django.urls import path
from .views import TranslationView, translate_text

urlpatterns = [
    # For class-based view:
    path("translate/", TranslationView.as_view(), name="translate"),

    # Or, if you prefer function-based view:
    # path("translate/", translate_text, name="translate"),
]
