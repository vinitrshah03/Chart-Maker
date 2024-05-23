from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render,HttpResponse
from .models import *
from .utils import *
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import UserProfile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def home(request):
    return render(request, 'home.html')
def home2(request):
    return render(request, 'home2.html')
def about(request):
    return render(request, 'about.html')


def Login(request):
    if request.method == 'POST':
        Username = request.POST['username']
        Password = request.POST['password']

        try:
            # Try to retrieve a user by the provided username
            user = UserProfile.objects.get(username=Username)

            global u_name
            u_name = Username

            # Check if the provided password is correct for the user
            if check_password(Password, user.password):
                # Redirect the user to the home page or any other desired page
                return render(request, 'home2.html',{'message': 'Loged in successfully'})
            else:
                # Display an error message to the user.
                return render(request, 'Login.html', {'error_message': 'Passwords do not match.Please Re-enter'})
        except UserProfile.DoesNotExist:
            # If the user does not exist, display an error message.
            return render(request, 'Login.html', {'error_message': 'User does not exist.Please Register and Login'})

    # Handle GET requests (render the login page)
    return render(request, 'Login.html')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = UserProfile.objects.get(email=email)
            if user:
                subject = 'Password Reset Request'
                message = 'Please click on the link below to reset your password:\n\n'
                message += request.build_absolute_uri(reverse('password_reset_confirm', args=[user.pk, 'token'])) + '\n\n'
                message += 'If you did not request a password reset, please ignore this email.'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                messages.success(request, 'Password reset email sent. Please check your email.')
                return redirect('password_reset_done')
            else:
                messages.error(request, 'No user found with this email address.')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, pk, token):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            # Retrieve the UserProfile object
            user = get_object_or_404(UserProfile, pk=pk)

            # Hash the password
            hashed_password = make_password(password)

            # Update the password field and save the object
            user.password = hashed_password
            user.save()

            messages.success(request, 'Password reset successful. You can now login with your new password.')
            return redirect('Login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'password_reset_confirm.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')

import re

def register(request):
    if request.method == 'POST':
        full_name = request.POST['full-name']
        email = request.POST['email']
        occupation = request.POST['occupation']
        username = request.POST['username']
        password = request.POST['password']

        # Check if username or email already exists
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        elif UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        # Enforce password policy
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('register')
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Password must contain at least one special character.Register again')
            return redirect('register')
        
        # Maximum password length
        if len(password) > 12:
            messages.error(request, 'Password too long. Register Again')
            return redirect('register')

        # Hash the password before saving
        hashed_password = make_password(password)

        try:
            # Create the user
            user = UserProfile.objects.create(
                full_name=full_name,
                email=email,
                occupation=occupation,
                username=username,
                password=hashed_password
            )
            user.password=password
            # Redirect to a success page or login page
            return redirect('Login')
        except Exception as e:
            # Display error message if user creation fails
            messages.error(request, 'Failed to create user: ' + str(e))
            return redirect('register')

    return render(request, 'Login.html')


@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, username=request.user.username)
    return render(request, 'profile.html', {'user_profile': user_profile})

def contract(request):
    return render(request, 'contract.html')
def set_session(request):
    request.session['username'] = 'john'
    return render(request, 'set_session.html')
def get_session(request):
    username = request.session.get('username')
    return render(request, 'get_session.html', {'username': username})

def Line(request):
    return render(request,"Line.html")
def bar(request):
    return render(request,"bar.html")
def pie(request):
    return render(request,"pie.html")
def insertview2(request):
    try:
        z=line_details.delete_all_records()
        z=objects_line.delete_all_records()
        a=request.GET["n1"]
        b=request.GET["n2"]
        c=request.GET["n3"]
        d=request.GET["n4"]
        z=line_details(obj1=a,obj2=b,obj3=c,obj4=d)
        z.save()
        return render(request,"Line.html",{"msg1":"Chart Details Saved"})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})

def insertview(request):
    try:
        a=int(request.GET["n2"])
        b=request.GET["n1"]
        z=objects_line(obj1=b,obj2=a)
        z.save()
        return render(request,"Line.html",{"msg":"Record Inserted"})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})

def plot_view(request):
    try:
        qs = objects_line.objects.all()
        qs1 = line_details.objects.all()
        x = [i.obj1 for i in qs]
        y = [j.obj2 for j in qs]
        a = [i.obj1 for i in qs1][0]
        b = [i.obj2 for i in qs1][0]
        c = [i.obj3 for i in qs1][0]
        d = [i.obj4 for i in qs1][0]
        e = line_details.obj1
        chart = get_plot(x,y,a,b,c,d,u_name)
        return render(request,"Line.html",{"chart":chart})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})

def bar_insert1(request):
    try:
        z=bar_details.delete_all_records()
        z=objects_bar.delete_all_records()
        a=request.GET["n1"]
        b=request.GET["n2"]
        c=request.GET["n3"]
        z=bar_details(obj1=a,obj2=b,obj3=c)
        z.save()
        return render(request,"bar.html",{"msg1":"Chart Details Saved"})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})

def bar_insert2(request):
    try:
        a=int(request.GET["n2"])
        b=request.GET["n1"]
        c=request.GET["n3"]
        z=objects_bar(obj1=b,obj2=a,obj3=c)
        z.save()
        return render(request,"bar.html",{"msg":"Record Inserted"})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})



def bar_plot_view(request):
    try:
        qs = objects_bar.objects.all()
        qs1 = bar_details.objects.all()
        x = [i.obj1 for i in qs]
        y = [j.obj2 for j in qs]
        z = [k.obj3 for k in qs]
        a = [i.obj1 for i in qs1][0]
        b = [i.obj2 for i in qs1][0]
        c = [i.obj3 for i in qs1][0]
        e = line_details.obj1
        chart = bar_plot(x,y,z,a,b,c,u_name)
        return render(request,"bar.html",{"chart":chart})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})



def pie_insert1(request):
    try:
        z=pie_details.delete_all_records()
        z=objects_pie.delete_all_records()
        a=int(request.GET["n2"])
        b=request.GET["n1"]
        z=pie_details(obj1=b,obj2=a)
        z.save()
        return render(request,"pie.html",{"msg":"Chart Details Saved.Click on next"})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})


def pie_insert2(request):
    try:
        a=int(request.GET["n2"])
        b=request.GET["n1"]
        c=request.GET["n3"]
        z=objects_pie(obj1=b,obj2=a,obj3=c)
        z.save()
        return render(request,"pie.html",{"msg":"Record Inserted.Click on next"})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})

def pie_plot_view(request):
    try:
        qs = objects_pie.objects.all()
        qs1 = pie_details.objects.all()
        x = [i.obj1 for i in qs]
        y = [j.obj2 for j in qs]
        z = [k.obj3 for k in qs]
        a = [i.obj1 for i in qs1][0]
        b = [i.obj2 for i in qs1][0]
        chart = pie_plot(x,y,z,a,b,u_name)
        return render(request,"pie.html",{"chart":chart})
    except:
        return render(request,"error.html",{"msg":"An Error Occured"})


def download_view(request):

    # e=ImageModel.delete_all_except_latest()

    # image_model = get_object_or_404(ImageModel)
    
    # image_model = ImageModel.objects.latest('timestamp')

    image_model = AllImageModel.objects.filter(uname=u_name).latest('timestamp')

    image_content = default_storage.open(image_model.image_field.name).read()
    response = HttpResponse(image_content, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename={slugify(image_model.image_field.name)}.png'

    return response

def randgentr(request):
    output = None
    if 'chart_type' in request.GET:
        chart_type = request.GET['chart_type']
        if chart_type == 'none':
            output = None
        elif chart_type == 'rand_line':
            output = rand_line(u_name)
        elif chart_type == 'rand_bar':
            output = rand_bar(u_name)
        elif chart_type == 'rand_barh':
            output = rand_barh(u_name)
        elif chart_type == 'rand_pie':
            labels = request.GET.get("labels")
            output = rand_pie(labels,u_name)
    return render(request,"charts.html",{"rand_chart":output})

#CSV to graph
def csv(request):
    try:
        if ('csv' in request.FILES) and (request.method == "POST"):
            csv_file = request.FILES['csv']
            if (request.POST.get("index")):
                data = pd.read_csv(csv_file, sep = ",",index_col = (request.POST.get("index")).strip())
                graph = csvgraph(request,data,u_name)
                return render(request, "csv.html", {"msg": "Index Column value not specified!","csv_chart":graph})
            else:
                # if (request.POST.get("chart_type2") in ["hist","h_hist"]):
                #     graph = ""
                #     return render(request, "csv.html", {"msg": "Index Column value not specified!","csv_chart":graph})
                # else:
                data = pd.read_csv(csv_file, sep = ",")
                graph = csvgraph(request,data,u_name)
                return render(request, "csv.html", {"msg": "CSV file uploaded successfully.","csv_chart":graph})
    except pd.errors.EmptyDataError:
        return render(request, "csv.html", {"msg": "The uploaded CSV file is empty."})
    except pd.errors.ParserError:
        return render(request, "csv.html", {"msg": "Invalid CSV file format."})

def charts(request):
    return render(request,"charts.html")

def csvchart(request):
    return render(request,"csv.html")

def all_images(request):
    allimages = AllImageModel.objects.filter(uname=u_name)
    return render(request,'all_chart.html',{'images': allimages})

#adding previous and next buttons to allow user to navigate through his graphs form the database
def buttons(request):
    previous = False
    next = False
    graph = False

    if (request.GET.get("previous")):
        previous = True
    elif(request.GET.get("next")):
        next = True

    cur_id = (request.GET.get("cur_id")).strip()    
    print("Type of cur_id: ",type(cur_id))
    print("Current ID from request:", cur_id)
    
    if not cur_id:
        if ImageModel.objects.exists():
            cur_id = int(((ImageModel.objects.order_by("id")).last()).id )
        else:
            1
    else:
        cur_id = int(cur_id)
        if(previous):
            cur_id = cur_id - 1
        elif(next):
            cur_id = cur_id + 1
    
        if int(cur_id) <= 1:
            cur_id = 1
        elif int(cur_id) >= ImageModel.objects.count():
            cur_id = int(ImageModel.objects.last().id)
            print("Count: ",cur_id)
        else:
            cur_id = int(cur_id)
        print("Updated cur_id 1:", cur_id)
    print("Type of cur_id: ",type(cur_id))

    try:
        graph = ImageModel.objects.get(id=cur_id)
        print("Fetching graph with cur_id:", cur_id)
        print("Type of cur_id: ",type(cur_id))

    except ImageModel.DoesNotExist:
        raise NoneException(request, "ImageModel with id {} does not exist.".format(cur_id), "charts.html")

    return render(request, "charts.html", {"chart": graph, "id": cur_id,"prev":previous,"next":next})

def a_c(request):
    return render(request,"all_chart.html")