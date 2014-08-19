import os.path
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

# Static shit
urlpatterns += patterns(
  '',
  url(r'^ddpresse$', 'relief.views.staticServe',
      {'target': os.path.join(settings.STATIC_ROOT, 'other/appendice-Operandi_Collection_1.pdf'),
       'content_type' : 'application/pdf'}),
  url(r'^collection_zero.pdf$', 'relief.views.staticServe',
      {'target': os.path.join(settings.STATIC_ROOT, 'other/appendice-Operandi_Collection_0.pdf'),
       'content_type' : 'application/pdf'}),
  url(r'^collection_une.pdf$', 'relief.views.staticServe',
      {'target': os.path.join(settings.STATIC_ROOT, 'other/appendice-Operandi_Collection_1.pdf'),
       'content_type' : 'application/pdf'}),
  # url(r'^collection_deux.pdf$', 'relief.views.staticServe',
  #     {'target': os.path.join(settings.STATIC_ROOT, 'other/appendice-Operandi_Collection_2.pdf'),
  #      'content_type' : 'application/pdf'}),
  url(r'^collection_trois.pdf$', 'relief.views.staticServe',
      {'target': os.path.join(settings.STATIC_ROOT, 'other/appendice-Operandi_Collection_3.pdf'),
       'content_type' : 'application/pdf'}),
  # url(r'^collection_une.pdf')

)

urlpatterns += patterns(
  '',
  # MUSCLE
  url(r'^$', 'relief.views.muscle'),

  # Main sh1t
  url(r'^(?P<path>.*)$', 'relief.views.operate', name='operate'),
)
