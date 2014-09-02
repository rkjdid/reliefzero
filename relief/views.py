# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.template.context import RequestContext
from django.http import HttpResponse

from relief.models import Page
from zero import settings

import httpagentparser as ap
import traceback
import os.path
import re

# URLs to be treated differently, because everyone is unique
customUrls = {
  'denyIE' : "1111",      # iefailpage (<9)
}

# Set of default parameters available in all views
defaultParameters = {
  "relief_title" : settings.PAGE_TITLE,
}

def catchAgent(request, path):
  # ap.detect()['browser'] on GoogleBot UA raises KeyError
  try:
    browser = ap.detect(request.META["HTTP_USER_AGENT"])['browser']
  except:
    traceback.print_exc()
    print "returning 'None'"
    return None

  if path != customUrls['denyIE'] and "Microsoft Internet Explorer" in browser['name']:
    # remove non-numeric characters from version, MSIE 7.0b encountered
    try : version = float(re.sub("[^0-9]", "", browser['version']))
    except: version = 0.0 # if we can't read version, shit must be old.
    # disallow MSIE <= 8.0
    if version <= 8.0:
      return gothere(request, target="/%s" % customUrls['denyIE'])

def operate(request, path=""):
  pageRedirect = catchAgent(request, path)
  if pageRedirect: return pageRedirect

  try:
    p = Page.objects.get(url=path)
  except (MultipleObjectsReturned, ObjectDoesNotExist):
    return chaos(request, path)

  styles = []
  for l in p.froms.all():
    if not l.initStyle in styles: styles.append(l.initStyle)
    if not l.hoverStyle in styles: styles.append(l.hoverStyle)

  params = {
    "title" : p.page_title,
    "img" : p.image.url,
    "img_width" : p.meta_width,
    "img_height" : p.meta_height,
    "w_zoom" : p.width_zoom,
    "h_zoom" : p.height_zoom,
    "deny_robots" : p.seo_block,
    "description" : p.seo_description,
    "links" : p.froms,
    "url": path,
    "styles": styles,
    "smooth_loading" : p.smooth_loading,
    "background" : p.page_background,
  }

  params = dict(params.items() + defaultParameters.items())

  return render_to_response(
    'relief.html',
    params,
    context_instance=RequestContext(request)
  )

def chaos(request, path):
  params = {
    "url" : path
  }

  params = dict(params.items() + defaultParameters.items())

  return render_to_response(
    'chaos.html',
    params,
    context_instance=RequestContext(request)
  )

def gothere(request, target='/'):
  return redirect(target, context_instance=RequestContext(request))

# Static rendering, ok for text files and such
def staticRender(request, target, content_type):
  return render(
      request,
      target,
      content_type=content_type
  )

# Static binary serve (pdf, jpg, ..)
def staticServe(request, target, content_type):
  f = open(target, 'rb')
  content = f.read()
  f.close()
  fname = os.path.basename(os.path.normpath(target))

  response = HttpResponse(content, content_type)
  response['Content-Disposition'] = 'attachment; filename=%s' % fname
  return response


# teaz
def video(request, page_title, target_url="/", vimeo_id=None, background_color="#ffffff", skip_black=True, **kwargs):
  """
  **kwargs will be passed to clean_video_sources
  """
  params = dict()
  params['page_title'] = page_title
  params['target_url'] = target_url
  params['background_color'] = background_color
  params['skip_black'] = skip_black

  if vimeo_id:
    params['vimeo_id'] = vimeo_id

  params['sources'] = clean_video_sources(**kwargs)

  return render_to_response(
    'video.html',
    dictionary=params,
    context_instance=RequestContext(request)
  )

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
