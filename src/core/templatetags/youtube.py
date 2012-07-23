# encoding: utf-8
from django import template
from django.template import Context, Template, Node

TEMPLATE = """"
<object width="480" height="385">
       <param name="movie"
           value="http://www.youtube.com/v/{{ id }}" />
       <param name="allowFullScreen" value="true" />
       <param name="allowscriptaccess" value="always" />
       <embed src="http://www.youtube.com/v/{{ id }}"
           type="application/x-shockwave-flash"
           allowscriptaccess="always"
           allowfullscreen="true"
           width="480"
           height="385">
       </embed>
   </object>
"""

def do_youtube(parser, token):
    try:
        tag_name, id_ = token.split_contents()
    except ValueError:
        msg = "%r tag requires 1 argument" % token.contents.split()[0]
        raise template.TemplateSyntaxError, msg

    return YoutubeNode(id_)


class YoutubeNode(Node):
    def __init__(self, id_):
        self.id = template.Variable(id_)

    def render(self, context):
        try:
            actual_id = self.id.resolve(context)
        except template.VariableDoesNotExist:
            actual_id = self.id

        t = Template(TEMPLATE)
        c = Context({'id': actual_id}, autoescape=context.autoescape)
        return t.render(c)

register = template.Library()
register.tag('youtube', do_youtube)
