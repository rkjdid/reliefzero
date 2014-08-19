from relief import models
from django.contrib import admin

class InlineLinks(admin.StackedInline):
  model = models.Link
  fk_name = "page"
  extra = 1

class AdminPage(admin.ModelAdmin):
  # class Media:
  #   js = ('static/admin/js/',)
  #   # css = {
  #   #   'all' : settings.STATIC_ROOT + 'kontrol/css/base.css',
  #   # }
  exclude = ('meta_width', 'meta_height', 'meta_size')
  inlines = [InlineLinks]

admin.site.register(models.Page, AdminPage)
admin.site.register(models.Style)
