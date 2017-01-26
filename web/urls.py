from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.http import HttpResponse

import web.views

# admin urls
urlpatterns = (
  url(r'^admin/', include(admin.site.urls)),
  url(r'^admin$', RedirectView.as_view(url='admin/', permanent=True)),

  # seo shit
  url(r'^robots.txt', lambda r: HttpResponse("User-agent: *\nAllow: /",
                                             mimetype="text/plain")),
  url(r'^sitemap.xml', lambda r: HttpResponse("http://reliefzero.com/",
                                              mimetype="text/plain"
  )),

  # sample call to video view
  # url(r'^$', 'relief.views.video',
  #     {
  #       'target_url': '/home',
  #       'page_title': 'Matabase',
  #       'vimeo_id': 104282882,
  #       'background_color': '#ffffff',
  #       'video/mp4': 'other/teazer.mp4',
  #     }
  # ),

  # Main page
  url(r'^(?P<path>.*)$', web.views.operate, name='operate'),
)
