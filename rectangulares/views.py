import math
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
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
    list = request.session.get('list')
    residuo = request.session.get('residuo')
    a = request.session.get('a')
    C = request.session.get('C')
    m = request.session.get('m')
    Xo = request.session.get('Xo')
    Pl = request.session.get('Pl')
    rango = range(len(list) - 1)  
    data = {
      'list': list,
      'residuo': residuo,
      'a': a,
      'C': C,
      'm': m,
      'Xo': Xo,
      'rango': rango,
      'Pl': Pl
    }
    return render(request, "tasks/recValue.html/", data)

def rectangulares_mixto(request):
    return render(request, "tasks/rectangulares_mixto.html", {'form': datos()})
      
def mixtos_datos(request): 
  if request.method == 'POST':
    data = request.POST
    a = int(data['a'])
    Xo = int(data['Xo'])
    C = int(data['C'])
    m = int(data['m'])
    Xl = [Xo]
    Rl = []
    Pl = []
    temp = None
    
    while temp != Xo :
        if temp == None :
            p1 = a*Xo+C
        else:
            p1 = a*temp+C
        
        floor = math.floor((p1)/m)
        Pl += [p1]
        Rl += [floor]
        p2 = floor * m
        Xn = p1-p2
        temp = Xn
        print(p1)
        if Xn in Xl :
            Xl += [Xn]
            indice = Xl.index(Xn)
            temp = Xo
            request.session['list'] = Xl
            if indice == 0 and len(Xl) == m:
                message = "Como n = m y Xn = Xn+1. El periodo es completo y los numeros rectangulares se aceptan"
            else :
                message = "Como n != m y Xn = Xn+1. Los numeros rectangulares son rechazados y el periodo es incompleto"
        else :
            Xl += [Xn]
    request.session['list'] = Xl
    request.session['residuo'] = Rl
    request.session['Pl'] = Pl
    request.session['Xo'] = Xo
    request.session['a'] = a
    request.session['C'] = C
    request.session['m'] = m
    request.session['mensaje'] = message
    return redirect("recValue")
    # url = reverse("recValue") + f'?list={Xl}'
    # return redirect(url)
  
    