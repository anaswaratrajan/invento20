from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from invento18.events.views import EventDetailView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^elements/$', TemplateView.as_view(template_name='pages/elements.html'), name='elements'),
    url(r'^generic/$', TemplateView.as_view(template_name='pages/generic.html'), name='generic'),
    url(r'^generic1/$', TemplateView.as_view(template_name='pages/generic1.html'), name='generic1'),
    url(r'^generic2/$', TemplateView.as_view(template_name='pages/generic2.html'), name='generic2'),
    
    url(r'^parallax/$', TemplateView.as_view(template_name='pages/parallax.html'), name='parallax'),
    url(r'^cse/$', TemplateView.as_view(template_name='pages/cs_dept.html'), name='cse'),
    url(r'^ec/$', TemplateView.as_view(template_name='pages/ec_dept.html'), name='ec'),
    url(r'^it/$', TemplateView.as_view(template_name='pages/it_dept.html'), name='it'),
    

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('invento18.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^events/(?P<pk>\d+)/$', EventDetailView.as_view(), name='event-view')


    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
