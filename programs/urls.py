from django.urls    import path

from programs.views import ProgramListView


urlpatterns = [
    path('', ProgramListView.as_view())
]