from django.urls    import path
from programs.views import ProgramView


urlpatterns = [
    path('', ProgramView.as_view()),
]