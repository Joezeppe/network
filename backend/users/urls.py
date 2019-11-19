from django.conf.urls import url
from users.views import RegisterUserView, UserDetail


app_name = 'users'
urlpatterns = [
    url(r'^user-register$', RegisterUserView.as_view(), name="user-register"),
    url(r'^user/(?P<pk>\d+)$', UserDetail.as_view(), name="user-detail")
]
