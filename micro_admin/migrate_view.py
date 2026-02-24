from django.http import HttpResponse
from django.core.management import call_command
from io import StringIO

def run_migrations(request):
    if request.GET.get('secret') != 'migrate-now-2024':
        return HttpResponse('Unauthorized', status=401)
    
    output = StringIO()
    try:
        call_command('migrate', '--noinput', stdout=output)
        call_command('create_default_superuser', stdout=output)
        return HttpResponse(f'<pre>{output.getvalue()}</pre>')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
