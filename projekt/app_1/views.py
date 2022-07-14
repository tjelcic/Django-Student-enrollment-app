from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum

# Create your views here.

def home_page(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {})
    else:
        return redirect('login')

def logout_view(request): 
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        user_form = RegistrationForm()
        return render(request, 'register.html', {'form':user_form})
    elif request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form':user_form})
    else:
        return HttpResponseNotAllowed

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def all_students(request):
    studenti = Korisnik.objects.all()
    return render(request, 'all_students.html', {'studenti':studenti})

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def insert_user(request):
    if request.method == 'GET':
        user_form = NewUserForm()
        return render(request, 'insert_user.html', {'form':user_form})
    elif request.method == 'POST':
        user_form = NewUserForm(request.POST)
        if Korisnik.objects.filter(username=request.POST['username']) or Korisnik.objects.filter(email=request.POST['email']):
            messages.info(request, 'Username ili email već postoje')
            return redirect('home')
        if user_form.is_valid():
            user_form.save()
            messages.info(request, 'Uspješno ste dodali korisnika')
            return redirect('home')
        else:
            return HttpResponseNotAllowed()

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def edit_user(request, user_id):
    user = Korisnik.objects.get(id=user_id)
    
    if request.method == 'GET':
        set_form = UserForm(instance=user)
        return render(request, 'edit_user.html', {'form':set_form})
    elif request.method == 'POST':
        set_form = UserForm(request.POST, instance=user)
        if set_form.is_valid():
            set_form.save()
            if user.role=='STUDENT':
                return redirect('all_students')
            elif user.role=='PROFESOR':
                return redirect('profesori')

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def delete_user(request, user_id):
    user = Korisnik.objects.get(id=user_id)
    user.delete()
    messages.info(request, 'Uspješno ste izbrisali korisnika')
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def user_details(request, user_id):
    user = Korisnik.objects.filter(id=user_id)
    return render(request, 'details_user.html', {'user':user})

@login_required
@user_passes_test(lambda u: u.role!='STUDENT')
def student_list(request, course_id):
    upisi = Upisi.objects.all()
    studenti = Korisnik.objects.all()
    predmet = Predmeti.objects.get(id=course_id)
    upisani = Upisi.objects.filter(predmet_id=predmet.id).values_list('student_id', flat=True)
    result = {}

    for i in studenti:
        for j in upisi:
            if i.id in upisani and i.id==j.student_id_id:
                status = Upisi.objects.get(predmet_id=predmet.id,student_id=i.id).status
                result[i.id] = {i.get_full_name(): status}

    context = {
        'studenti':result,
        'course_id':course_id,
        'predmet':predmet.name
    }
    return render(request, 'student_list.html', context)

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def profesori(request):
    profesori = Korisnik.objects.all()
    return render(request, 'profesori.html', {'profesori':profesori})

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def courses(request):
    predmeti = Predmeti.objects.all()
    return render(request, 'courses.html', {'predmeti':predmeti})

@login_required
@user_passes_test(lambda u: u.role=='PROFESOR')
def my_courses(request, user_id):
    user = Korisnik.objects.get(id=user_id)
    predmeti = Predmeti.objects.all()
    my = predmeti.filter(nositelj_id=user.id)
    return render(request, 'my_courses.html', {'predmeti':my})

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def insert_course(request):
    if request.method == 'GET':
        course_form = PredmetForm()
        return render(request, 'insert_course.html', {'form':course_form})
    elif request.method == 'POST':
        course_form = PredmetForm(request.POST)
        if Predmeti.objects.filter(name=request.POST['name']) or Predmeti.objects.filter(kod=request.POST['kod']):
            messages.info(request, 'Ime ili kod predmeta već postoji')
            return redirect('home')
        if course_form.is_valid():
            course_form.save()
            return redirect('courses')
        else:
            return HttpResponseNotAllowed()

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def delete_course(request, course_id):
    predmet = Predmeti.objects.get(id=course_id)
    predmet.delete()
    messages.info(request, 'Uspješno ste izbrisali predmet')
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.role=='ADMIN')
def edit_course(request, course_id):
    course = Predmeti.objects.get(id=course_id)

    if request.method == 'GET':
        set_form = PredmetForm(instance=course)
        return render(request, 'edit_course.html', {'form':set_form})
    elif request.method == 'POST':
        set_form = PredmetForm(request.POST, instance=course)
        if set_form.is_valid():
            set_form.save()
            return redirect('courses')

@login_required
@user_passes_test(lambda u: u.role!='STUDENT')
def course_detail(request, course_id):
    course = Predmeti.objects.filter(id=course_id)
    return render(request, 'detail_course.html', {'course':course})


@login_required
def upisni_list(request, student_id):
    predmeti = Predmeti.objects.all()
    student = Korisnik.objects.get(id=student_id)
    upisani = Upisi.objects.filter(student_id=student.id)
    predmet_id = Upisi.objects.filter(student_id=student.id).values_list('predmet_id', flat=True)
    neupisani = {}
    
    for i in predmeti:
        if i.id not in predmet_id:
            neupisani[i.id] = i.name

    context = {
        'predmeti':predmeti,
        'ime':student,
        'upisani':upisani,
        'neupisani':neupisani,
    }
    return render(request, 'upisni_list.html', context)


def ispis_predmeta(request, predmet_id, student_id):
    predmet = Upisi.objects.filter(predmet_id=predmet_id, student_id=student_id)
    predmet.delete()
    if request.user.role == 'PROFESOR':
        return redirect('my_courses', request.user.id)
    return redirect('upisni_list', student_id)


def upis_predmeta(request, predmet_id, student_id):
    predmet = Predmeti.objects.get(id=predmet_id)
    student = Korisnik.objects.get(id=student_id)

    if student.status == 'REDOVNI':
        semestar = Predmeti.objects.filter(id=predmet_id).values_list('sem_red', flat=True)
        predmeti = Predmeti.objects.filter(sem_red__lt=semestar[0]).values_list('id', flat=True)
        polozeno = Upisi.objects.filter(student_id=student_id, status='polozen').values_list('predmet_id', flat=True)
        for p in predmeti:
            if p not in polozeno:
                messages.info(request, 'Nije polozeno sve iz proslih semestara')
                return redirect('home')

    elif student.status == 'IZVANREDNI':
        semestar = Predmeti.objects.filter(id=predmet_id).values_list('sem_izv', flat=True)
        predmeti = Predmeti.objects.filter(sem_red__lt=semestar[0]).values_list('id', flat=True)
        polozeno = Upisi.objects.filter(student_id=student_id, status='polozen').values_list('predmet_id', flat=True)
        for p in predmeti:
            if p not in polozeno:
                messages.info(request, 'Nije polozeno sve iz proslih semestara')
                return redirect('home')

    Upisi.objects.create(predmet_id=predmet, student_id=student, status='upisan')

    return redirect('upisni_list', student_id)

@login_required
@user_passes_test(lambda u: u.role!='STUDENT')
def polozio_predmet(request, predmet_id, student_id):
    Upisi.objects.filter(predmet_id=predmet_id, student_id=student_id).update(status='polozen')
    if request.user.role == 'PROFESOR':
        return redirect('my_courses', request.user.id)
    return redirect('upisni_list', student_id)

@login_required
@user_passes_test(lambda u: u.role!='STUDENT')
def izgubio_potpis(request,predmet_id, student_id):
    Upisi.objects.filter(predmet_id=predmet_id, student_id=student_id).update(status='izgubio potpis')
    if request.user.role == 'PROFESOR':
        return redirect('my_courses', request.user.id)
    return redirect('upisni_list', student_id)

def zbroj_upisanih_bodova(request, student_id):
    predmeti = Upisi.objects.select_related('predmet_id').filter(student_id = student_id, status='upisan').values('predmet_id__name', 'predmet_id__ects')
    upisani = Upisi.objects.select_related('predmet_id').filter(student_id = student_id, status='upisan').aggregate(Sum('predmet_id__ects'))
    zbroj = upisani['predmet_id__ects__sum']
    student = Korisnik.objects.get(id=student_id).get_full_name()

    context = {
        'predmeti':predmeti,
        'zbroj':zbroj,
        'student':student
    }

    return render(request, 'zbroj_upisanih_bodova.html', context)

def zbroj_polozenih_bodova(request, student_id):
    predmeti = Upisi.objects.select_related('predmet_id').filter(student_id = student_id, status='polozen').values('predmet_id__name', 'predmet_id__ects')
    polozeni = Upisi.objects.select_related('predmet_id').filter(student_id = student_id, status='polozen').aggregate(Sum('predmet_id__ects'))
    zbroj = polozeni['predmet_id__ects__sum']
    student = Korisnik.objects.get(id=student_id).get_full_name()

    context = {
        'predmeti':predmeti,
        'zbroj':zbroj,
        'student':student
    }

    return render(request, 'zbroj_polozenih_bodova.html', context)




