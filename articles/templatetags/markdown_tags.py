import markdown
import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

VIEWPORT_SIZES = {
    'small' :  None,
    'medium':  None,
    'large' :  None,
}

# formats youtube link for embed and creates iframe tag
def to_iframe(link: str, size: str):
    size = size.split("*")
    width = size[0]
    height = size[1]

    link = re.sub("/watch\?v=", "/embed/", link)
    link = re.sub("&ab_channel=(.*)", "", link)

    return f"<iframe src='{link}' width='{width}' height='{height}'>"

# 1. finds entries of special %md_vid={url}|size=width*height% sequence
# 2. for each such entry creates <iframe src={url} width={width} height={height}> tag
# 3. replaces according special sequences with their iframe tag representation
def process_embed_vids(md_text: str):
    vid_links = re.findall("%md_vid=(.*)\|size=([0-9]*[*][0-9]*)|(?:small|medium|large)%", md_text)

    for vid_link in vid_links:
        iframe_tag = to_iframe(vid_link[0], vid_link[1])
        template_md = f"%md_vid={vid_link[0]}|size={vid_link[1]}%"
        md_text = md_text.replace(template_md, iframe_tag)

    return md_text


# markdown filter that transforms markdown to html for further display in html template
# allows us to store text in markdown syntax while working with models and employ different extensions embeds/tables/code 
# without creation of extra fields and relations
@register.filter(name='markdown')
@stringfilter
def markdown_to_html(string: str):
    md_extensions = ['fenced_code', 'abbr', 'def_list', 'footnotes', 'tables']

    if "%md_vid" in string:
        processed_string = process_embed_vids(string)

        return markdown.markdown(processed_string, extensions=md_extensions)
    
    return markdown.markdown(string, extensions=md_extensions)
    
    
