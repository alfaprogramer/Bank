from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User,Transaction,BankAccount, UserProfile,Notification
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponse,HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from django.contrib import messages
from .forms import formedu, formhome
from django.db.models import Max






# Create your views here.
@login_required
def index(request):
   

     
    user_profile = UserProfile.objects.get(user=request.user)
     # Get unread notifications for the user
    unread_notifications = Notification.objects.filter(user=request.user, read=False)

    return render(request, "money/index.html", {
        "user": request.user,
        "user_profile": user_profile,
        "unread_notifications": unread_notifications,
    })    
    



@login_required
def mark_notification_as_read(request):
    if request.method == "POST":
        notification_id = request.POST.get("notification_id")
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.read = True
            notification.save()
            return JsonResponse({"success": True})
        except Notification.DoesNotExist:
            return JsonResponse({"success": False, "message": "Notification not found."})

    return JsonResponse({"success": False, "message": "Invalid request method."})

@login_required
def mark_all_notifications_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, read=False).update(read=True)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "message": "Invalid request method."})

   

 



def loanform(request):
    return render(request,"money/loanform.html")

def formEdu(request):
    form1 = formedu()
    

    context = {
        'form1': form1,
        
    }

    return render(request, 'money/loanform.html', context)


def formHome(request):
    form2 = formhome()
    context={
        'form2': form2,
    }
    return render(request, 'money/loanform.html',context)



def submit_form1(request):
    if request.method == 'POST':
        form = formedu(request.POST)
        if form.is_valid():
            # Process form data if needed
            # Redirect to another page or render a success message
            return redirect('balance')  # Change 'success_page' to your actual success page

    return render(request, 'money/loanform.html', {'form1': formedu()})

def submit_form2(request):
    if request.method == 'POST':
        form = formhome(request.POST)
        if form.is_valid():
            # Process form data if needed
            # Redirect to another page or render a success message
            return redirect('balance')  # Change 'success_page' to your actual success page

    return render(request, 'money/loanfrom.html', {'form2': formhome()})

def balance(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        bank_account = BankAccount.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
        bank_account = None

    # Check balance and add a notification if it's under 20
    if bank_account and bank_account.balance < 20:
        create_notification(request.user, "Low Balance: Your account balance is below 20.")

   

    return render(request, "money/balance.html", {"user": request.user, "user_profile": user_profile})



def create_notification(user, message):
    Notification.objects.create(
        user=user,
        message=message,
    )
    

def send(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,"money/sendmoney.html", { "user": request.user,"user_profile": user_profile })

def history(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,"money/history.html", { "user": request.user,"user_profile": user_profile })

def loan(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,"money/loan.html", { "user": request.user,"user_profile": user_profile })







def send_money_api(request):
    if request.method =="POST":
        amount = request.POST.get("amount")
        to_whom_mcode = request.POST.get("towhom")
        


        recieveruser= User.objects.get(userprofile__mcode = to_whom_mcode)

        recieveracc=BankAccount.objects.get(user=recieveruser)
        try:
            senderacc = BankAccount.objects.get(user=request.user) 

            # Check if sender is trying to send money to themselves
            if senderacc.user == recieveruser:
                return JsonResponse({"success": False, "message": "Invalid recipient MCODE."})

          

            # Convert amount to Decimal before performing subtraction
            amount_decimal = Decimal(amount)

            if senderacc.balance >= amount_decimal > 0:

                senderacc.balance -= amount_decimal
                recieveracc.balance += amount_decimal

                senderacc.save()
                recieveracc.save()

                # Create a single Transaction record for the transaction
                Transaction.objects.create(sender=request.user, receiver=recieveruser, amount=float(amount))
                

                return JsonResponse({"success" : True})
            else:
                return JsonResponse({"success": False, "message": "Insufficient balance."})
        except (User.DoesNotExist, BankAccount.DoesNotExist):
            return JsonResponse({"success": False, "message": "Invalid recipient mcode."})
     
    return JsonResponse({"success": False, "message": "Invalid request method."})   



def history(request):
    # Retrieve the user's sent and received transactions
    # Get transactions where the user is either the sender or the receiver
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)

    return render(request, 'money/history.html', {
        'transactions': transactions, 
        "user": request.user,
       "user_profile": user_profile})


def login_in(request):
    if request.method =="POST":

     name = request.POST['name']
     password = request.POST['password']

     user = authenticate(request,username=name, password=password)

     if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
     else:
        return render(request,"money/login.html",{
           "message":"Invalid Name or Password"
        })
     
    else:
       return render(request, "money/login.html")
    


def register(request):
    if request.method == "POST":
        print(request.FILES)  # Add this line to print request.FILES
        name = request.POST['name']
        email = request.POST['email']
        date = request.POST['date']
        mobile = request.POST['mobile']
        address = request.POST['address']
        tcode = request.POST['tcode']
        
        # Use request.FILES for file uploads (like images)
        image = request.FILES['image']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            return render(request, "money/register.html", {
                "message": "Please select an image."
            })
       
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        # Check if passwords match
        if password != cpassword:
            return render(request, "money/register.html", {
                "message": "Password must match."
            })
        

         
      
        try:
            # Create a user instance
            user = User.objects.create_user(name, email, password)
            user.save()

            # Authenticate the user
            auth_user = authenticate(request, username=name, password=password)

            # Log in the user
            login(request, auth_user)

            # Create a BankAccount instance for the user
            bank_account = BankAccount(user=request.user, balance=100.00)
            bank_account.save()

            # Create a user profile instance
            profile = UserProfile(
                user=request.user,  # Associate with the authenticated user
                date_of_birth=date,
                mobile_number=mobile,
                address=address,
                mcode=tcode,
                image=image,
            )
            profile.save()

            # Redirect to the index page
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            # Handle duplicate user creation
            return render(request, "money/register.html", {
                "message": "User with this email already exists."
            })
        except ValidationError:
            return render(request, "money/register.html", {
                "message": "Invalid data submitted."
            })
    else:
        return render(request, "money/register.html")