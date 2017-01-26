# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.template.context import RequestContext
from django.template.response import TemplateResponse

from web.models import Page
from rzero import settings

import os.path

# Main view rendering all valid paths
def operate(request, path=""):
  try:
    p = Page.objects.get(url=path)
  except (MultipleObjectsReturned, ObjectDoesNotExist):
    return chaos(request, path)

  styles = []
  for l in p.froms.all():
    if not l.initStyle in styles: styles.append(l.initStyle)
    if not l.hoverStyle in styles: styles.append(l.hoverStyle)

  ctx= {
    "title": p.page_title,
    "img": p.image.url,
    "img_width": p.meta_width,
    "img_height": p.meta_height,
    "w_zoom": p.width_zoom,
    "h_zoom": p.height_zoom,
    "deny_robots": p.seo_block,
    "description": p.seo_description,
    "links": p.froms,
    "url": path,
    "styles": styles,
    "smooth_loading": p.smooth_loading,
    "background": p.page_background,

    "relief_title": "TODO"
  }
  return TemplateResponse(request, 'web/relief.html', context=ctx)

def chaos(request, path):
  ctx = {
    "url": path,
    "relief_title": "TODO"
  }
  return TemplateResponse(request, 'web/chaos.html', context=ctx)

# teaz
def video(request, page_title, target_url="/", vimeo_id=None, background_color="#ffffff", skip_black=True, **kwargs):
  """
  **kwargs will be passed to clean_video_sources
  """
  ctx = dict()
  ctx['page_title'] = page_title
  ctx['target_url'] = target_url
  ctx['background_color'] = background_color
  ctx['skip_black'] = skip_black

  if vimeo_id:
    ctx['vimeo_id'] = vimeo_id

  ctx['sources'] = clean_video_sources(**kwargs)

  return TemplateResponse(request, 'web/video.html', context=ctx)

def clean_video_sources(**kwargs):
  """
  Example for kwargs:
  kwargs = {
    'video/mp4': 'path/to/example.mp4'
    'video/ogg': 'path/to/example.ogg'
  }
  see __supported_video_types for valid key values,
  any other key value for kwargs will be ignored
  """
  __supported_video_types = ["video/mp4", "video/ogg"]
  sources = dict()
  for k, v in kwargs.iteritems():
    if k in __supported_video_types:
      p = os.path.join(settings.STATIC_ROOT, v)
      try:
        open(p)
      except:
        continue # file not found

      sources[k] = os.path.join(settings.STATIC_URL, v)

  return sources
