

from django.core.files.storage import FileSystemStorage, Storage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,

    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/user-bio-form.html')


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    response_error = ''
    context = {
        "response_error": response_error
    }
    if request.method == 'POST' and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        print(fs.size(myfile.name))
        if fs.size(myfile.name) > 1024:
            context["response_error"] = 'Not allowed size of the file. File must be less 1 kB. Submit another file.'
            return render(request, 'requestdataapp/file-upload.html', context=context)
        filename = fs.save(myfile.name, myfile)

        print('Saved file', filename)
    return render(request, 'requestdataapp/file-upload.html', context=context)