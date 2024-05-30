from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .forms import UserBioForm, UploadFileForm


# Create your views here.

def process_get_view(request: HttpRequest):
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        'a': a,
        'b': b,
       'result': result,
    }
    return render(request, 'requestapp/request-query-params.html', context=context)

def user_form(request: HttpRequest):
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestapp/user-bio-form.html', context=context)

def handle_file_upload(request: HttpRequest):
    # result = ''
    form = UploadFileForm()
    if request.method == "POST":                # and request.FILES.get('myfile'):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
          # myfile = request.FILES["myfile"]
          myfile = form.cleaned_data["file"]
          fs = FileSystemStorage()
          if myfile.size <= 1048576:
            filename = fs.save(myfile.name, myfile)
            print("saved file", filename)
            # result = f"Successfully saved file {myfile.name}"
          else:
            print("Error, file is too big")
            # result = f"Error, file is too big {myfile.name}"
    else:
        form = UploadFileForm()
    context = {
       #'result': result,
        "form": form
    }
    return render(request, 'requestapp/file-upload.html', context=context)