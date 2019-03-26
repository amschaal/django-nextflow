from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import NxfRun, NxfLogMessage
from .tasks import add
# from .forms import NextflowStartForm
import logging
import subprocess as sp

logger = logging.getLogger()
logger.info("loading views")

# Create your views here.
def index(request):
    """
    Return the main page
    """
    logger.info("processing index request")
    template = "dashboard/index.html"
    context = {}
    return render(request, template, context)

def start_pipeline(request):
    """
    """
    if request.method == 'POST':
        # form = NextflowStartForm(request.POST)
        # print(form)
        command = ['nextflow', 'help']
        process = sp.Popen(command,
            stdout = sp.PIPE,
            stderr = sp.PIPE,
            shell = False,
            universal_newlines = True)
        proc_stdout, proc_stderr = process.communicate()
        print(proc_stdout, proc_stderr, process.returncode)
        return HttpResponse("")
    # else:
    #     return render(request, 'name.html', {'form': form})

@csrf_exempt
def listen(request):
    """
    """
    if request.method == 'POST':
        message_json = request.body
        message_data = json.loads(message_json)
        print(message_data)
        # {'runId': 'ab3882b5-bc08-45a1-aff0-45c0173e5b17', 'event': 'started', 'runName': 'distraught_shaw', 'runStatus': 'started', 'utcTime': '2019-03-25T16:47:59Z'}
        # {'runId': 'ab3882b5-bc08-45a1-aff0-45c0173e5b17', 'event': 'completed', 'runName': 'distraught_shaw', 'runStatus': 'completed', 'utcTime': '2019-03-25T16:47:59Z'}
        runId = message_data['runId']
        runName = message_data['runName']
        event = message_data['event']
        runStatus = message_data['runStatus']
        utcTime = message_data['utcTime']
        runId_instance, runId_created = NxfRun.objects.get_or_create(
            runId = runId,
            runName = runName
            )
        logMessage_instance, logMessage_created = NxfLogMessage.objects.get_or_create(
            runId = runId_instance,
            event = event,
            runName = runName,
            runStatus = runStatus,
            utcTime = utcTime,
            body_json = message_json)
        return HttpResponse("")
