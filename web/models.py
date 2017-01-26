# coding: utf8
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import  post_save
from PIL import Image
import os.path

class Page (models.Model):
  class Meta:
    ordering = ['url']

  url = models.CharField(
    'URL',
    help_text="this is the URL you want for your page, leading / is implied, empty string means homepage",
    max_length=300, null=True, blank=True, default="", unique=True)
  page_title = models.CharField(
    'Page title',
    help_text="title of the page, example : 'Home'",
    max_length=300, null=True, blank=True, default='relief zéro')
  page_background = models.CharField(
    'Background color',
    help_text="set custom background color",
    max_length=7, default="#ffffff")
  seo_block = models.BooleanField(
    'Block webcrawlers',
    help_text="disallow robots, like GoogleBot, for page indexing",
    default=False)
  seo_description = models.TextField(
    'Page description',
    help_text="description metatag, should be picked by crawlers for web browsers results (no guarantee, actual text content might overrule this)",
    default="", null=True, blank=True)

  image = models.ImageField(
    'Image',
    help_text='the lighter the better, 300ko or less is recommended. Submit the image to get a preview for links below',
    upload_to= 'pages/')
  height_zoom = models.FloatField(
    'Image zoom - height',
    help_text= "height (in percents) of drawing area, 100 (default) means all browser area, no scroll",
    default=100.0)
  width_zoom = models.FloatField(
    'Image zoom - width',
    help_text="width (in percents) of drawing area, 100 (default) means all browser area, no scroll",
    default=100.0)
  smooth_loading = models.BooleanField(
    'Smooth loading',
    help_text="when enabled page will fade-in only when fully loaded, this is not recommended for heavy images",
    default=False)

  # Read only meta fields
  meta_width = models.IntegerField('Image width (px)', default=0)
  meta_height = models.IntegerField('Image height (px)', default=0)
  meta_size = models.IntegerField('Image size (bytes)', default=0)

  # Update some meta fields
  def set_meta(self):
    img = Image.open(self.image.path)
    (self.meta_width, self.meta_height) = img.size
    self.meta_size = os.path.getsize(self.image.path)

    # disconnect post_save signal before updating
    post_save.disconnect(set_meta, sender=Page)
    self.save()
    post_save.connect(set_meta, sender=Page)

  def __unicode__(self):
    return "/%s" % self.url

class Link (models.Model):
  x = models.FloatField()
  y = models.FloatField()
  width = models.FloatField()
  height = models.FloatField()
  target = models.ForeignKey('Page', related_name="links", null=True, blank=True)
  page = models.ForeignKey('Page', related_name="froms")
  remote = models.CharField(max_length=600, null=True, blank=True, default='')
  newtab = models.BooleanField(default=False)

  initStyle = models.ForeignKey('Style', null=True, blank=True, default=None, related_name='init_links')
  hoverStyle = models.ForeignKey('Style', null=True, blank=True, default=None, related_name='end_links')
  transition = models.FloatField(default=0)

  def __unicode__(self):
    try: return "/%s" % self.target.url
    except:
      if self.remote != "" : return "%s" % self.remote
      else : return "[empty target]"

class Style (models.Model):
  name = models.CharField(max_length=120, unique=True, default="")
  cssString = models.TextField(default="")

  def __unicode__(self):
    return "%d#%s" % (self.id, self.name)

# post/pre_save shit
def set_meta(sender, instance, **kwargs):
  instance.set_meta()

post_save.connect(set_meta, sender=Page)
