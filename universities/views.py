from django.shortcuts import render, redirect
from .models import *
from .forms import *
from users.access_checking import *


def view_university(request, university_id):
    check_1 = check_access_type_1(request)
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)

    university = University.objects.get(pk = university_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            university.delete()
            return redirect('view_universities')
    

    return render(request, 'University.html', {'university':university})


def add_university(request):
    check_1 = check_access_type_2(request, 'add_university')
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    university_form = UniversityForm()
    if request.method == 'POST':
        university_form = UniversityForm(request.POST or None)
        university_form.save()
        return redirect('view_universities')

    return render(request, 'add_university.html', {'university_form':university_form})
    

def edit_university(request, university_id):
    

    check_1 = check_access_type_2(request, 'add_university')
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    university = University.objects.get(pk = university_id)
    university_form = UniversityForm(instance=university)
    if request.method == 'POST':
        university_form = UniversityForm(request.POST or None, instance=university)
        university_form.save()
        return redirect('view_university', university.pk)

    return render(request, 'edit_university.html', {'university_form':university_form, 'university': university})
    



def view_universities(request):
    check_1 = check_access_type_1(request)
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)

    universities = University.objects.all()

    return render(request, 'Universities.html', {'universities':universities})





def view_scholarship(request, scholarship_id):
    scholarship = Scholarship.objects.get(pk = scholarship_id)
    followed = bool(len(list(ScholarshipFollower.objects.filter(user =request.user , scholarship = scholarship))))

    if request.method == 'POST':
        if 'Follow' in request.POST:
            if followed:
                ScholarshipFollower.objects.get(user =request.user , scholarship = scholarship).delete()
                followed = 0
            else:
                ScholarshipFollower.objects.create(user =request.user , scholarship = scholarship)
                followed = 1

        elif 'delete' in request.POST:
            scholarship.delete()
            return redirect('view_university', scholarship.university.pk)

    return render(request, 'scholarship.html', {'scholarship':scholarship, 'followed':followed})



def add_scholarship(request, university_id):
    uni = University.objects.get(pk = university_id)
    check_1 = check_access_type_2(request, 'add_university')
    
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    scholarship_form = ScholarshipForm(initial={"university": uni})
    if request.method == 'POST':
        scholarship_form = ScholarshipForm(request.POST or None)
        scholarship_form.save()
        return redirect('view_university', uni.pk)

    return render(request, 'add_scholarship.html', {'scholarship_form':scholarship_form, 'university': uni})
    




def edit_scholarship(request, scholarship_id):
    
    check_1 = check_access_type_2(request, 'add_university')
    
    
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    scholarship = Scholarship.objects.get(pk = scholarship_id)
    uni = scholarship.university

    scholarship_form = ScholarshipForm(instance=scholarship)
    if request.method == 'POST':
        scholarship_form = ScholarshipForm(request.POST or None, instance=scholarship)
        if scholarship_form.is_valid():
            scholarship_form.save()
            return redirect('view_scholarship', scholarship.pk)

    return render(request, 'edit_scholarship.html', {'scholarship_form':scholarship_form, 'university': uni, 'scholarship':scholarship})
    




def add_scholarship_session(request, scholarship_id):
    scholarship = Scholarship.objects.get(pk = scholarship_id)
    check_1 = check_access_type_2(request, 'add_university')
    print(check_1)
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    scholarship_form = ScholarshipSessionForm(initial={"scholarship": scholarship})
    if request.method == 'POST':
        scholarship_form = ScholarshipSessionForm(request.POST or None)
        scholarship_form.save()
        return redirect('view_universities')

    return render(request, 'add_scholarship_session.html', {'scholarship_form':scholarship_form, 'scholarship':scholarship})
    


def edit_scholarship_session(request, session_id):
    session = ScholarshipSession.objects.get(pk = session_id)
    check_1 = check_access_type_2(request, 'add_university')
    
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    scholarship_form = ScholarshipSessionForm(instance=session)
    if request.method == 'POST':
        scholarship_form = ScholarshipSessionForm(request.POST or None, instance=session)
        if scholarship_form.is_valid():
            scholarship_form.save()
            return redirect('view_scholarship', session.scholarship.pk)

    return render(request, 'edit_scholarship_session.html', {'scholarship_form':scholarship_form, 'session':session})
    

