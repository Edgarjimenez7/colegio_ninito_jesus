from django.shortcuts import render

def admisiones(request):
    return render(request, 'admisiones.html')

def area_matematicas(request):
    return render(request, 'areas/matematicas.html')

def area_ciencias(request):
    return render(request, 'areas/ciencias.html')

def area_espanol(request):
    return render(request, 'areas/espanol.html')

def area_sociales(request):
    return render(request, 'areas/sociales.html')

def area_tecnologia(request):
    return render(request, 'areas/tecnologia.html')

def area_pastoral(request):
    return render(request, 'areas/pastoral.html')

def area_idiomas(request):
    return render(request, 'areas/idiomas.html')

def area_psicologia(request):
    return render(request, 'areas/psicologia.html')

def area_artes(request):
    return render(request, 'areas/artes.html')

def area_deportes(request):
    return render(request, 'areas/deportes.html')
