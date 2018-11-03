from django.conf.urls import url
from . import views   

urlpatterns = [
    url(r'^$', views.signin),
    url(r'^reg_process$', views.reg_process),
    url(r'^log_process$', views.log_process),
    url(r'^clear$', views.clear),
    url(r'^books$', views.home),
    url(r'^add$', views.add), # Page to add new books 
    url(r'^add_process$', views.add_process),
    url(r'^books/(?P<num>\d+)$', views.show), # Shows book, author, and reviews
    url(r'^books/(?P<num>\d+)/add_review$', views.add_review),
    url(r'^books/(?P<num>\d+)/(?P<num2>\d+)/delete_review$', views.delete_review),
    url(r'^users/(?P<num>\d+)$', views.profile), # User profile 
]