from django import template
import string

register = template.Library()

@register.simple_tag
def randomStr(size=12, chars=string.ascii_letters + string.digits + string.punctuation):
  import random
  return ''.join(random.choice(chars) for i in range(size))
