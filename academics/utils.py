from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import uuid


def render_to_pdf(template_src,folder_name,params:dict):
    template = get_template(template_src)
    folder_name = folder_name
    print(folder_name)
    html = template.render(params)
    result = BytesIO()
    filename= uuid.uuid4()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    try:
        with open(str(settings.BASE_DIR)+f'/media/{folder_name}/{filename}.pdf','wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")),output)
    except Exception as e:
        print(e)
            
    if pdf.err:
        return '',False
        
    return filename,True
