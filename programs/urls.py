from django.urls    import path
from programs.views import ReserveView, ProgramView


urlpatterns = [
    path('', ProgramView.as_view()),
    path('/reserve', ReserveView.as_view()),
]