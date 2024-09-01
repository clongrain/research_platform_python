import io
import json
from PyPDF2 import PdfReader, PdfWriter
from supabase import create_client
import os
from dotenv import load_dotenv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

BUCKET_NAME = 'scientific-management-platform'


class SupabaseClientSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if SupabaseClientSingleton._instance is None:
            # Supabase 项目 URL 和匿名用户公钥
            load_dotenv()
            SUPABASE_URL = os.getenv("SUPABASE_URL")
            SUPABASE_KEY = os.getenv("SUPABASE_KEY")
            # 创建 Supabase 客户端
            SupabaseClientSingleton._instance = create_client(SUPABASE_URL, SUPABASE_KEY)
        return SupabaseClientSingleton._instance



# Create your views here.
def generateMaterial(request):
    data = json.loads(request.body)
    order = data['order']

    writer = PdfWriter()
    pdfTemplate = select_pdf_template(data['materialType'])
    if not pdfTemplate:
        return HttpResponse("Invalid material type", status=400)
    reader = PdfReader(pdfTemplate)
    for page in reader.pages:
        writer.add_page(page)

    supabase = SupabaseClientSingleton.get_instance()
    supabase.auth.sign_in_with_password(
        {"email": "ChangyuYun@outlook.com", "password": "123456"})
    for item in order:
        mergePDF(writer, item, supabase, data)
    with open('merged_file.pdf', 'wb') as f:
        writer.write(f)
    with open('merged_file.pdf', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="merged_file.pdf"'
        return response


def mergePDF(writer, type: str, supabase, data):
    table = ''
    if type.__eq__('conferencePaper'):
        table = 'conference_paper'
    elif type.__eq__('journalPaper'):
        table = 'journal_paper'
    elif type.__eq__('award'):
        table = 'award'
    elif type.__eq__('patent'):
        table = 'patent'
    elif type.__eq__('monograph'):
        table = 'monograph'
    elif type.__eq__('softwareCopyright'):
        table = 'software_copyright'
    else:
        return

    response = (supabase.table(table).select("storage_path").
                in_('id', data[type]).execute())
    if response.data and len(response.data) > 0:
        for storage in response.data:
            path: str = storage['storage_path']
            res = supabase.storage.from_(BUCKET_NAME).download(path)
            filename = path.split('/')[-1]
            with open(filename, 'wb+') as f:
                f.write(res)
            print(f'文件：{filename}已下载')
            reader = PdfReader(filename)
            for page in reader.pages:
                writer.add_page(page)

            os.remove(filename)

def select_pdf_template(material_type):
    templates = {
        '成果报奖': '成果报奖.pdf',
        '年度总结': '年度总结.pdf',
        '职称评定': '职称评定.pdf',
        '项目结题': '项目结题.pdf'
    }
    return templates.get(material_type, None)
