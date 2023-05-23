from xml.etree.ElementInclude import include
from django.urls import path
from . import views
from . import skillDetailViews
app_name = "chart"
urlpatterns = [
    # path('doughnut/',ChartView.as_view(), name='index'),
    # path('doughnut/',views.top100skills, name='doughnut'),
    path('top100Skills/',views.top100Skills, name='top100Skills'),
    path('searchResult/',views.searchResult, name='searchResult'),
    
    
    # path('skillDetailTest/<str:skill>/',views.skillDetail, name='skillDetailTest'),
    path('skillDetail/<str:skill>',skillDetailViews.skillDetail, name='skillDetail'),
    path('test/', views.test, name="test")
    
]
