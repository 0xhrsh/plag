from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import FileForm
import os
import requests

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/943193187332280360/5vICFUEYbl-nLmCO50ra3uyzbMPilqbexmUOR_gBkG7Dju_oI5JZpb6w3Skd5YIKgMs4"

def IndexView(request):

    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f1 = request.FILES['file1']
            f2 = request.FILES['file2']

            fs = FileSystemStorage()
            f1n = fs.save(f1.name, f1)
            f2n = fs.save(f2.name, f2)

            lans = {
                'c': 'c',
                'cpp': 'cc',
                'py': 'python',
                'cs': 'csharp',
                'js': 'javascript',
                'm': 'matlab',
                'tcl': 'tcl'
            }

            if f1n.split('.')[-1] != f2n.split('.')[-1]:
                return HttpResponse("Files of different languages!")

            ext = f2n.split('.')[-1]
            if ext not in lans:
                return HttpResponse(".{} files are not yet supported!\n You can only check plagiarism for the following files: {}".format(ext, ", ".join(list(lans.keys()))))

            ls_fd = os.popen(
                "cd media;chmod 0755 mossnet.pl;./mossnet.pl -l {} {} {} ".format(lans[ext], f1n, f2n))
            output = ls_fd.read()
            requests.post(DISCORD_WEBHOOK, json={
                      "content": "cc: <@!745343708936798319>\nplag checked for: " + str(output)})
            print(output)
            ls_fd.close()
            ls_fd = os.popen("cd media;rm {};rm {}".format(f1n, f2n))
            ls_fd.close()
            output = str(output).split()
            return HttpResponseRedirect(output[0])

    return render(request, 'plagapp/index.html', {"form": FileForm()})
