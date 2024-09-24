import json
import math
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from .models import Proyect, Task
from django.shortcuts import get_object_or_404, render
from .forms import datos, opcionales
from scipy.stats import norm, ksone


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
    list = request.session.get("list")
    residuo = request.session.get("residuo")
    a = request.session.get("a")
    C = request.session.get("C")
    m = request.session.get("m")
    Xo = request.session.get("Xo")
    Pl = request.session.get("Pl")
    nr = request.session.get("nr")
    validate = request.session.get("validate")
    message = request.session.get("message")
    rango = range(len(list) - 1)
    data = {
        "list": list,
        "residuo": residuo,
        "a": a,
        "C": C,
        "m": m,
        "Xo": Xo,
        "rango": rango,
        "Pl": Pl,
        "nr": nr,
        "message": message,
        "validate": validate,
    }

    if validate == True:
        sumaL = sum(nr)
        tamano = len(nr)
        media = sumaL / tamano
        Zo = abs(((media - 1 / 2) * math.sqrt(tamano)) / math.sqrt(1 / 12))
        data.update(
            {
                "sumaL": sumaL,
                "tamano": tamano,
                "media": media,
                "Zo": Zo,
                "form": opcionales(),
            }
        )
    return render(request, "tasks/recValue.html/", data)


def recMultiValue(request):
    list = request.session.get("list")
    residuo = request.session.get("residuo")
    a = request.session.get("a")
    pe = request.session.get("pe")
    m = request.session.get("m")
    Xo = request.session.get("Xo")
    Pl = request.session.get("Pl")
    nr = request.session.get("nr")
    message = request.session.get("message")
    validate = request.session.get("validate")
    rango = range(len(list) - 1)
    data = {
        "list": list,
        "residuo": residuo,
        "a": a,
        "pe": pe,
        "m": m,
        "Xo": Xo,
        "Pl": Pl,
        "message": message,
        "rango": rango,
        "nr": nr,
        "validate": validate,
    }

    if validate == True:
        sumaL = sum(nr)
        tamano = len(nr)
        media = sumaL / tamano
        Zo = abs(((media - 1 / 2) * math.sqrt(tamano)) / math.sqrt(1 / 12))
        data.update(
            {
                "sumaL": sumaL,
                "tamano": tamano,
                "media": media,
                "Zo": Zo,
                "form": opcionales(),
            }
        )

    return render(request, "tasks/recMultiValue.html/", data)


def rectangulares_mixto(request):
    return render(request, "tasks/rectangulares_mixto.html", {"form": datos()})


def rectangulares_multi(request):
    return render(request, "tasks/rectangulares_multi.html", {"form": datos()})


def mixtos_datos(request):
    if request.method == "POST":
        data = request.POST
        a = int(data["a"])
        Xo = int(data["Xo"])
        C = int(data["C"])
        m = int(data["m"])
        Xl = [Xo]
        Rl = []
        Pl = []
        nr = []
        temp = None

        while temp != Xo:
            if temp == None:
                p1 = a * Xo + C
            else:
                p1 = a * temp + C

            floor = math.floor((p1) / m)
            Pl += [p1]
            Rl += [floor]
            p2 = floor * m
            Xn = p1 - p2
            temp = Xn

            if Xn in Xl or len(Xl) == m + 1:
                Xl += [Xn]
                nr += [Xn / m]
                indice = Xl.index(Xn)
                temp = Xo
                if indice == 0 and len(Xl) == m + 1:
                    message = "Como n = m y Xn = Xn+1. El periodo es completo y los numeros rectangulares se aceptan"
                    validate = True
                else:
                    message = "Como n != m y Xn = Xn+1. Los numeros rectangulares son rechazados y el periodo es incompleto"
                    validate = False
            else:
                nr += [Xn / m]
                Xl += [Xn]
        request.session["list"] = Xl
        request.session["residuo"] = Rl
        request.session["Pl"] = Pl
        request.session["Xo"] = Xo
        request.session["nr"] = nr
        request.session["a"] = a
        request.session["C"] = C
        request.session["m"] = m
        request.session["validate"] = validate
        request.session["message"] = message
        return redirect("recValue")
        # url = reverse("recValue") + f'?list={Xl}'
        # return redirect(url)


def multi_datos(request):
    if request.method == "POST":
        data = request.POST
        a = int(data["a"])
        Xo = int(data["Xo"])
        m = int(data["m"])
        pe = int(m / 4)
        Xl = [Xo]
        Rl = []
        Pl = []
        nr = []
        temp = None

        while temp != Xo:
            if temp == None:
                p1 = a * Xo
            else:
                p1 = a * temp

            floor = math.floor(p1 / m)
            Pl += [p1]
            Rl += [floor]
            p2 = floor * m
            Xn = p1 - p2
            temp = Xn

            if Xn in Xl or len(Xl) == pe + 1:
                Xl += [Xn]
                nr += [Xn / m]
                indice = Xl.index(Xn)
                temp = Xo
                if indice == 0 and len(Xl) == pe + 1:
                    message = "Como n = PE y Xn = Xn+1. El periodo es completo y los numeros rectangulares son aceptados."
                    validate = True
                else:
                    message = "Como n != PE o Xn = Xn+1. Los numeros rectangulares son rechazados y el perido es incompleto"
                    validate = False
            else:
                nr += [Xn / m]
                Xl += [Xn]
        request.session["list"] = Xl
        request.session["residuo"] = Rl
        request.session["nr"] = nr
        request.session["Pl"] = Pl
        request.session["Xo"] = Xo
        request.session["a"] = a
        request.session["m"] = m
        request.session["pe"] = pe
        request.session["validate"] = validate
        request.session["message"] = message
        return redirect("recMultiValue")


def calcular_alpha(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            alpha_dato = int(data.get("alpha_dato"))
            alpha_real = 1 - (alpha_dato / 100)
            Zar = alpha_real / 2
            Z = norm.ppf(1 - (alpha_dato / 100) / 2)

            response_data = {"alpha_real": alpha_real, "Zar": Zar, "Z": Z}
            return JsonResponse(response_data)
        except json.JSONDecoderError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def calcular_alpha_dn(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            alpha_dato = int(data.get("alpha_dato"))
            alpha_real = alpha_dato / 100
            n = int(data.get("n"))
            datos = data.get("promedios")
            if(alpha_dato == 5) :
                c = 1.36
            elif (alpha_dato == 1) :
                c = 1.63
            else :
                c = 1.22
            
            D_alpha_n = c / math.sqrt(n)
            
            # D_alpha_n = ksone.ppf(1 - alpha_real, n)

            response_data = {"alpha_real": alpha_real, "n": n, "Dan": D_alpha_n}
            return JsonResponse(response_data)
        except json.JSONDecoderError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def promedios(request):
    data = {
        "form": opcionales()
    }
    return render(request, "tasks/promedios.html", data)

def promedio_value(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lista = data.get("lista")
            # print(lista)
            suma = sum(lista)
            n = len(lista)
            promedio = suma/n
            Zo = abs(((promedio - 1 / 2) * math.sqrt(n)) / math.sqrt(1 / 12))
            
            request_data = {"promedio": promedio, 
                            "suma": suma, 
                            "n": n, 
                            "lista": lista, 
                            "Zo": Zo}
            return JsonResponse(request_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=405)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def ks_value(request):
    if request.method == "POST":
        try:
            Fxi = []
            Dn = []
            
            data = json.loads(request.body)
            lista = data.get("lista")
            print(lista)
            n = len(lista)
            listaOrd = sorted(lista)
            print(listaOrd)
            for i in listaOrd :
                xi = (int(listaOrd.index(i)) + 1) / n
                Fxi += [xi]
                Dn += [xi - i]
                Dnm = max(Dn)
                
            repeat = Dn.count(Dnm)
            
            request_data = {"n": n, 
                            "lista": lista,
                            "listaOrd": listaOrd,
                            "Fxi": Fxi,
                            "Dn": Dn,
                            "Dnm": Dnm,
                            "repeat": repeat}
            
            return JsonResponse(request_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=405)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def f_value(request) :
    if request.method == "POST" :
        try :
            data = json.loads(request.body)
            lista = data.get("lista")
            N = int(data.get("N"))
            alfa = data.get("alfa")
            newList = []
            contador = 0
            n = len(lista)
            i = 0
            FEi = n/N
            
            while i < N :
                j = 0
                temp = []
                print("salto")
                while j < N :
                    if(contador == n) :
                        temp += []
                    else :
                        temp += [lista[contador]]
                        contador += 1
                    j += 1
                    print(temp)
                    
                i += 1
                newList += [temp]
                    
            request_data = {
                "newList": newList,
                "FEi": FEi,
                "n": N,
                "N": n
            }
            
            return JsonResponse(request_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=405)
    
    return JsonResponse({"error": "Invalid JSON"}, status=405)