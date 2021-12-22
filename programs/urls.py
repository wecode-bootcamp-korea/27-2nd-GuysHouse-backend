from django.urls    import path
from programs.views import ProgramDetailView, ProgramView, ReserveView,ProgramListView


urlpatterns = [
    path('', ProgramListView.as_view()),
    path('/hosting', ProgramView.as_view()),
    path('/detail/<int:program_id>', ProgramDetailView.as_view()),
    path('/detail/<int:program_id>/reserve', ReserveView.as_view()),
]