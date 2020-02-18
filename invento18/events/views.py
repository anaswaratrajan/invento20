from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.base import ContextMixin
from .models import Event, Event_register, Ambassador
from .forms import EventRegisterForm,AmbassadorForm, Loginform

from django.http import HttpResponseRedirect
from django.shortcuts import render



def ambassador_register_view(request):
    last_registration = Ambassador.objects.latest('referal_code')
    ref_code = last_registration.referal_code
    form = AmbassadorForm(request.POST)
    if request.method == 'POST':
        a = Ambassador()
        a.first_name = request.POST.get('first_name')
        a.last_name = request.POST.get('last_name')
        a.email = request.POST.get('email')
        a.phone = request.POST.get('phone')
        a.college = request.POST.get('college')
        a.department = request.POST.get('department')
        print(Ambassador.objects.filter(email=a.email).count())

        if Ambassador.objects.filter(email=a.email).count()==0:
            ref=int(ref_code[3:])
            ref +=1
            a.referal_code = 'INV'+str(ref)
            ref_code = 'INV'+str(ref)
            a.points = 0
            a.save()
            return redirect('/ambassador-login')
        else:
            message = "Email already registered!!"
            return render(request, 'pages/ambassador_register.html', {'form': form,
                                                                            'message':message})

    else:
        form = AmbassadorForm()

    return render(request, 'pages/ambassador_register.html', {'form': form})

def ambassador_login_view(request):
    form = Loginform(request.POST)
    if request.method == 'POST':
        try:
            post_email = request.POST.get('email')
            post_referal_code = request.POST.get('referal_code')
            current_ambassador = Ambassador.objects.get(pk=post_referal_code, email=post_email)
            request.session['referal_code'] = current_ambassador.referal_code

            return redirect('/leaderboard')
        except:
            message = 'INVALID LOGIN!'
            return render(request, 'pages/login_ambassador.html', {'form': form,
                                                                       'message':message} )
    else:
        form = AmbassadorForm()

    return render(request, 'pages/login_ambassador.html', {'form': form})


def profile(request):
    if request.session.has_key('referal_code'):
        ref_code = request.session['referal_code']
        current_ambassador = Ambassador.objects.get(referal_code=ref_code)
        return render(request, 'pages/profile.html', {"current_ambassador":current_ambassador})
    else:
        return render(request, 'pages/login_ambassador.html', {})

def leaderboard(request):
    if request.session.has_key('referal_code'):
        ref_code = request.session['referal_code']
        current_ambassador = Ambassador.objects.get(referal_code=ref_code)
        Ambassadors = Ambassador.objects.all().order_by('-points').exclude(pk='INV2020')
        return render(request, 'pages/points.html', {"ambassadors":Ambassadors,
                                                "current_ambassador":current_ambassador})

def logout(request):
    try:
        del request.session['referal_code']
        print("\n\n\nlogged out\n\n\n")
        return redirect('/')
    except:
        pass
    return redirect('/')

class EventDetailView(DetailView):
    model = Event
    template_name = 'pages/event_detail.html'

def departmentview(request):

    if request.path == '/general/':
        template_name = 'pages/general.html'
        events = Event.objects.filter(category='gen')
        return render(request, template_name,
            {'events' : events }
        )

    else:
        if request.path == '/cse/':
            dept = 'cse'
        elif request.path == '/ece/':
            dept = 'ece'
        elif request.path == '/eee/':
            dept = 'eee'
        elif request.path == '/it/':
            dept = 'it'
        elif request.path == '/me/':
            dept = 'me'
        elif request.path == '/saptha/':
            dept = 'sta'

        template_name = 'pages/' + dept + '_dept.html'

        workshops = Event.objects.filter(category=dept, _type='wor')
        competitions = Event.objects.filter(category=dept, _type='com')
        shows = Event.objects.filter(category=dept, _type='sho')
        talks = Event.objects.filter(category=dept, _type='tal')


        return render(request, template_name, {
        'workshops' : workshops,
        'competitions' : competitions,
        'shows' : shows,
        'talks' : talks,
        })

def event_register_view(request):
    # form = EventRegisterForm(request.POST or None)
    # if form.is_valid():
    #     form.save()
    #     return redirect('home')
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        mobile = request.POST["phone"]
        referal_code = request.POST["referal_code"]
        event = request.POST["event"]
        event_register = Event_register(first_name=first_name, last_name=last_name, email=email, phone=mobile, referal_code=referal_code, event=event)
        event_register.save()


        ambassador = Ambassador.objects.get(referal_code = referal_code)
        ev = Event.objects.get(title = event)
        ambassador.points += ev.fee /10
        ambassador.save()

        return redirect('home')
    else:
        events = Event.objects.all().order_by('title')
        return render(request, 'pages/event_register.html', {'events': events})

def event_register(request):
    events = Event.objects.all().order_by('title')
    return render(request, 'pages/event_register.html', {'events': events})


def campus_ambassador(request):
    return render(request, 'pages/ambassador.html')
