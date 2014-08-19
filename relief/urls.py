from django.conf.urls import patterns, include, url

from zero import settings

urlpatterns = patterns(
  '',
)

# Admin custom init
from django.contrib import admin
admin.autodiscover() # admin.autodiscover() equivalent

# Admin urls
urlpatterns += patterns (
  '',
  url(r'^admin/', include(admin.site.urls)),
  url(r'^admin$', 'relief.views.gothere', { 'target' : '/admin/' }),
  url(r'^ubberkontrol/?$', 'relief.views.gothere', { 'target' : '/admin/' }),
)

if settings.DEBUG :
  # Development media sh1t
  urlpatterns += patterns (
    'django.views.static',
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.replace('/','',1), 'serve', {'document_root': settings.MEDIA_ROOT }),
  )

# SEO shit
urlpatterns += patterns(
  '',
  url(r'^robots.txt$', 'relief.views.staticRender',
      {'target' : 'seo/robots.txt',
       'content_type' : 'text/plain'}),
  url(r'^sitemap.xml$', 'relief.views.staticRender',
      {'target' : 'seo/sitemap.xml',
       'content_type' : 'application/xml'}),
)

urlpatterns += patterns(
  '',
  # Main sh1t
  url(r'^(?P<path>.*)$', 'relief.views.operate', name='operate'),
)
