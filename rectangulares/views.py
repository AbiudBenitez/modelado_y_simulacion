import math
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Proyect, Task
from django.shortcuts import get_object_or_404, render
from .forms import datos


# Create your views here.
def index(request):
    tareas = Task.objects.all()
    return render(request, "index.html", {"tareas": tareas})


def hello(request, username):
    return HttpResponse("<h1>Hola Mundo %s </h1>" % username)


def about(request):
    return HttpResponse("About")


def proyecta(request):
    proyects = list(Proyect.objects.values())
    return JsonResponse(proyects, safe=False)


def task(request, id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse("task: %s " % task.title)

def recValue(request):
    data = {
        'list': request.GET.get("list")
    }
    return render(request, "tasks/recValue.html/", data)

def rectangulares_mixto(request):
  if request.method == 'POST':
    data = request.POST
    a = int(data['a'])
    Xo = int(data['Xo'])
    C = int(data['C'])
    m = int(data['m'])
    Xl = [Xo]
    temp = None
    i = 0
    
    while temp != Xo :
        if i == 0 :
            p1 = a*Xo+C
            p2 = math.floor((p1)/m) * m
            Xn = p1-p2
            temp = Xn
    
            Xl += [Xn]
            i += 1
            print(Xl)
        else:
            p1 = a*temp+C
            p2 = math.floor((p1)/m) * m
            Xn = p1-p2
            temp = Xn
            
            if Xn in Xl :
                indice = Xl.index(Xn)
                temp = Xo
                print(len(Xl))
                request.session['list'] = Xl
                if indice == 0 and len(Xl) == m:
                    print("El periodo es completo y los numeros rectangulares se aceptan")
                else :
                    print("Los numeros rectangulares son rechazados y el periodo es incompleto")
            else :
                Xl += [Xn]
                i += 1
                print(Xl)
    # return redirect('recValue/?list=')
    return render(request, "tasks/rectangulares_mixto.html", {'form': datos()})
  else:
    return render(request, "tasks/rectangulares_mixto.html", {'form': datos()})
      