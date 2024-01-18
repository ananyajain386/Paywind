from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.http import JsonResponse 
from app1.models import Paywind_User,BankAccount,OTP,LinkedAccount,Transactions,Coupons,SplitBill,Dropdowns,dynamic_panel,Wallet,PostPaid
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json
import random
from django.db.models.functions import Now
from django.utils import timezone  
import re
# from app1.tasks import add 

# def expire_otp(request):
#    if request.method=='GET': 
#      result = add.apply_async((2, 3), countdown=5) 
#      print(result) 
#      return JsonResponse({"message":"hi"},status=200)

def register(request):
   if request.method=='POST': 
      db=json.loads(request.body)
      # username=db['phonenumber']
      # email=db['email']
      # first_name=db['firstname']
      # last_name=db['lastname']
      # date_of_birth=db['dob']
      # gender=db['gender']
      # password=db['password']
      # confirmpassword=db['confirmpassword']
      # print(type(request.post))
      # username=db['phonenumber']
      # print(request.POST)
      print(db.keys())
      print(type(db.keys()))
      # if 'phonenumber' in db.keys():
      #    username=db['phonenumber']
      # else:
      #    return JsonResponse({"message":"Fill the username"},status=400)
      # print(db)
      # print(username)
      username=db.get('phonenumber')
      email=db.get('email')
      first_name=db.get('firstname')
      last_name=db.get('lastname')
      date_of_birth=db.get('dob')
      gender=db.get('gender')
      password=db.get('password')
      confirmpassword=db.get('confirmpassword')
      print(type(db))
      if username is None:
           print('hi')
           return JsonResponse({"message":"Fill the username"},status=400)
      if first_name is None:
           return JsonResponse({"message":"Fill the first_name"},status=400)
      if last_name is None:
           return JsonResponse({"message":"Fill the last_name"},status=400)
      if email is None:
           return JsonResponse({"message":"Fill the email"},status=400)
      if date_of_birth is None:
           return JsonResponse({"message":"Fill the date_of_birth"},status=400)
      if gender is None:
           return JsonResponse({"message":"Fill the gender"},status=400)
      if password is None:
           return JsonResponse({"message":"Fill the password"},status=400)
      if confirmpassword is None:
           return JsonResponse({"message":"Fill the confirmpassword"},status=400)
      if password!=confirmpassword:
            return JsonResponse({'message':'Password does not match'},status=400) 
      if Paywind_User.objects.filter(username=username).exists():
          return JsonResponse({'message':'User already registered'},status=400) 
      elif Paywind_User.objects.filter(email=email).exists():
          return JsonResponse({'message':'Email already registered'},status=400) 
      else:  
            Paywind_User.objects.create_user(username=username,email=email,password=password,first_name =first_name,last_name=last_name,gender=gender,date_of_birth=date_of_birth)
          #   id=str(username)+"@paytm"
          #   user.UPI_id=id
          #   user.save()
            return JsonResponse({'message':'New user has been registered successfully.'},status=200)
   else:
      return JsonResponse({'message':'Incorrect request method'},status=400)   
def create_account(request):
   if request.method=='POST': 
      nominee=request.POST.get('nominee')
      nominee_phoneno=request.POST.get('nominee_phoneno')
      print(nominee_phoneno)  
      aadhaar_card=request.FILES.get('aadhaar_card')
      pan_card=request.FILES.get('pan_card')
      aadhaar_card_no=request.POST.get('aadhaar_card_no')
      pan_card_no=request.POST.get('pan_card_no')
      marital_status=request.POST.get('marital_status')
      photo=request.FILES.get('photo')
      address=request.POST.get('address')
      UPI_number=request.POST.get('phonenumber')
      # print(type(request.post.get))
      if not nominee:
           return JsonResponse({"message":"Fill the nominee"},status=400)
      if not nominee_phoneno:
           return JsonResponse({"message":"Fill the nominee's phone number"},status=400)
      if not aadhaar_card:
           return JsonResponse({"message":"Add aadhaar_card"},status=400)
      if not pan_card:
           return JsonResponse({"message":"Add pan_card"},status=400)
      if not aadhaar_card_no:
           return JsonResponse({"message":"Fill the aadhaar card number"},status=400)
      if not pan_card_no:
           return JsonResponse({"message":"Fill the aadhaar card number"},status=400)
      if not marital_status:
           return JsonResponse({"message":"Fill marital_status"},status=400)
      if not photo:
           return JsonResponse({"message":"Add photo"},status=400)
      if not address:
           return JsonResponse({"message":"Fill the address"},status=400)
      if not UPI_number:
           return JsonResponse({"message":"Enter the phone number"},status=400)
      elif BankAccount.objects.filter(aadhaar_card_no=aadhaar_card_no).exists():
           return JsonResponse({"message":"Account already exists with same aadhar card number"},status=400)
      elif BankAccount.objects.filter(pan_card_no=pan_card_no).exists():
           return JsonResponse({"message":"Account already exists with same pan card number"},status=400)
      elif BankAccount.objects.filter(nominee_phoneno=nominee_phoneno).exists():
           return JsonResponse({"message":"Account already exists with same nominee phone number"},status=400)
      elif BankAccount.objects.filter(UPI_number=UPI_number).exists():
           return JsonResponse({"message":"Account already exist"},status=400)
      else:
         if Paywind_User.objects.filter(username=UPI_number).exists():
           user=Paywind_User.objects.get(username=UPI_number).pk
           acc=BankAccount.objects.create(user_id=user,nominee=nominee,nominee_phoneno=nominee_phoneno,aadhaar_card=aadhaar_card,pan_card=pan_card,aadhaar_card_no=aadhaar_card_no,pan_card_no=pan_card_no,marital_status=marital_status,photo=photo,address=address,UPI_number=UPI_number)
           id=str(UPI_number)+"@paytm"
           a=1
           while a>0:
             x=random.sample(range(9999999999,99999999999),1)
             print(x)
             if not BankAccount.objects.filter(account_number=x).exists(): 
                break
           print(x[0])
           acc.account_number=x[0]
           acc.balance=1000
           acc.UPI_id=id
           acc.save()
           return JsonResponse({'message':'New account has been created successfully.'},status=200)
         else: 
          return JsonResponse({'message':'Kindly regiater first'},status=400)
    
def link_account(request):
   if request.user.is_authenticated: 
    if request.method=='POST': 
     id=request.user.id
     user=Paywind_User.objects.get(id=id)
     db=json.loads(request.body)
     UPI_number=db['UPI_number']
     print(UPI_number)
     bank_name=db['bank_name']
     branch_name=db['branch_name']
     account_number=db['account_number']
     account_type=db['account_type'] 
     IFSC_code=db['IFSC_code']
     if BankAccount.objects.filter(UPI_number=UPI_number).exists(): 
         return JsonResponse({"message":"Bank account already exists"},status=400)
     elif LinkedAccount.objects.filter(UPI_number=UPI_number).exists(): 
         return JsonResponse({"message":"An account has been already linked to this number"},status=400)
     elif UPI_number!=user.username:
        return JsonResponse({"message":"Enter correct phone number"},status=400)
     else:
      if not UPI_number:
           return JsonResponse({"message":"Fill the phone number"},status=400)
      if not bank_name:
           return JsonResponse({"message":"Fill the phone number"},status=400)
      if not branch_name:
           return JsonResponse({"message":"Fill the branch name"},status=400)
      if not account_number:
           return JsonResponse({"message":"Add account number"},status=400)
      if not account_type:
           return JsonResponse({"message":"Add account type"},status=400)
      if not IFSC_code:
           return JsonResponse({"message":"Fill the IFSC code"},status=400)
      elif LinkedAccount.objects.filter(account_number=account_number).exists():
           return JsonResponse({"message":"Account already exists"},status=400)
      elif BankAccount.objects.filter(account_number=account_number).exists():
           return JsonResponse({"message":"Account already exists"},status=400)
      else:
           user=Paywind_User.objects.get(username=UPI_number).pk
           user1=LinkedAccount.objects.create(user_id=user,UPI_number=UPI_number,bank_name=bank_name,branch_name=branch_name,account_number=account_number,account_type=account_type,IFSC_code=IFSC_code)
           id=str(UPI_number)+"@paytm"
           user1.UPI_id=id
           user1.balance=10000
           user1.save()
      return JsonResponse({'message':'Your account has been linked successfully.'},status=200)
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)
     
def otp(request):
    if request.method=='POST': 
      f=json.loads(request.body)
      phone=f['phone']
      print(phone)
      if Paywind_User.objects.filter(username=phone).exists():
       user=Paywind_User.objects.get(username=phone)
       id=user.id
       inst=OTP.objects.create(user_id=id,phone=user.username,email=user.email)
       x=random.sample(range(999,9999),1)
       inst.otp=x[0]
       inst.save()
    #    five_minutes_ago = django.utils.timezone.now() + datetime.timedelta(minutes=-5)
    #    fil = OTP.objects.filter(req_time__gte=five_minutes_ago)
    #    for x in fil:
    #        x.status='active'
    #        x.save()
       ctx ={'otp':x,
             'UPI_id':user.username,
             'UPI_number':user.username,
             'email':user.email
            }
       email_content = render_to_string('email.html',ctx) 
       subject = 'OTP'
       from_email = 'ananyajain386@gmail.com'
       recipient_list = [user.email]
       send_mail(subject, 'OTP Verification', from_email, recipient_list, html_message=email_content)
       return JsonResponse({'message':'OTP sent successfully.'},status=200)
      else:
       return JsonResponse({'message':'User not registered.'},status=400)
        
def confirm_otp(request):
    if request.method=='POST': 
       time_for_now =  timezone.now()
       print(time_for_now)
     #   Time_difference= 
       f=json.loads(request.body)
       phone=f['phone']
       otp=f['otp']
       user=OTP.objects.filter(phone=phone,status='active',type='Login').last()
       time=user.time
       Time_difference=time_for_now-time
       td=Time_difference.seconds
       print(Time_difference.seconds)
       a=user.otp
       if td<120:
        if otp==str(a):
           user1=Paywind_User.objects.get(username=phone)
           user.status='expired'
           user.save()
           login(request,user1)
           return JsonResponse({'message':'OTP matched and logged in successfully.'},status=200)
        else:
         print('pen')
         return JsonResponse({'message':'OTP not matched.'},status=400)
       else:
         user.status='expired'
         user.save() 
         return JsonResponse({'message':'OTP not matched.'},status=400)
       
def login_page(request):
   if request.method=='GET': 
      if request.user.is_authenticated: 
          return JsonResponse({'message':'Alredy logged in'},status=400)
      else:
        return JsonResponse({'message':'Login yoursekf'},status=200) 
   else:
      return JsonResponse({'message':'Invalid request method'},status=400)
   
def logout1(request):
   if request.method=='GET': 
      if request.user.is_authenticated: 
          request.session.flush()
          logout(request)
          return JsonResponse({'message':'Logged out successfully.'},status=200)
      else:
        return JsonResponse({'message':'Already logged out.'},status=400) 
   else:
      return JsonResponse({'message':'Invalid request method'},status=400)

def pin(request):
   if request.user.is_authenticated: 
    if request.method=='POST': 
       id=request.user.id
       user=Paywind_User.objects.get(id=id)
       phone=user.username
       db=json.loads(request.body)
       pin=db['pin']
       if LinkedAccount.objects.filter(UPI_number=phone).exists():
           a=LinkedAccount.objects.get(UPI_number=phone)
           a.PIN=int(pin)
           a.save()
           return JsonResponse({'message':'Pin saved.'},status=200)  
       elif BankAccount.objects.filter(UPI_number=phone).exists():
           a=BankAccount.objects.get(UPI_number=phone)
           a.PIN=int(pin)
           a.save()
           return JsonResponse({'message':'Pin saved.'},status=200)
       else:
           return JsonResponse({'message':'Not registered'},status=200)  
    else:
     return JsonResponse({'message':'Invalid request method'},status=400)    
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)    
     
# def valid_amount(request):
#     if request.user.is_authenticated: 
#      if request.method=='POST': 
#         id=request.user.id
#         db=json.loads(request.body)
#         to=db['to']
#         amount=db['amount']
#         if LinkedAccount.objects.filter(user_id=id).exists():
#             u=LinkedAccount.objects.get(user_id=id)
#             amnt=int(amount)
#             if amnt<u.balance:
#                 return JsonResponse({'message':'Sufficient balance'},status=200)  
#             else:
#                 t=Transactions.objects.create(amount=amount,to=to)
#                 t.status='FAILED'
#                 t.reason='Your payment is unsuccessful as you do not have sufficient balance in your Bank account. Do not worrry, your money has NOT been deducted from the account.'
#                 t.save()
#                 return JsonResponse({'message':'Insufficient balance'},status=400)    
#         elif BankAccount.objects.filter(user_id=id).exists():
#             amount=db['amount']
#             u=BankAccount.objects.get(user_id=id)
#             amnt=int(amount)
#             if amnt<u.balance:
#                 return JsonResponse({'message':'Sufficient balance'},status=200)  
#             else:
#                 return JsonResponse({'message':'Insufficient balance'},status=400)
#         else:
#           return JsonResponse(status=400) 

# def check_pin(request):
#     if request.user.is_authenticated: 
#      if request.method=='POST': 
#         id=request.user.id
#         db=json.loads(request.body)
#         pin1=db['pin']
#         pin=int(pin1)
#         if LinkedAccount.objects.filter(user_id=id).exists():
#             u=LinkedAccount.objects.get(user_id=id)
#             if pin==u.PIN:
#                 return JsonResponse({'message':'CORRECT Pin'},status=200)  
#             else:
#                 return JsonResponse({'message':'INCORRECT Pin'},status=400)  
#         elif BankAccount.objects.filter(user_id=id).exists():
#             u=BankAccount.objects.get(user_id=id)
#             if pin==u.PIN:
#                 return JsonResponse({'message':'CORRECT Pin'},status=200)  
#             else:
#                 return JsonResponse({'message':'INCORRECT Pin'},status=400)
#         else:
#           return JsonResponse({'message':'Bad request'},status=400)

# def transaction(request):
#     if request.user.is_authenticated: 
#      if request.method=='POST': 
#         id=request.user.id
#         db=json.loads(request.body)
#         amount=db['amount']
#         date=db['date']
#         time=db['time']
#         to=db['to']
#         Transactions.objects.create(amount=amount,date=date,time=time,to=to)
#         if LinkedAccount.objects.filter(user_id=id).exists():
#            u=LinkedAccount.objects.get(user_id=id)
#            u.balance-=amount
#            u.save()
#         if BankAccount.objects.filter(user_id=id).exists():
#            u=BankAccount.objects.get(user_id=id)
#            u.balance-=amount
#            u.save()
#         if LinkedAccount.objects.filter(UPI_number=to).exists():
#            a=LinkedAccount.objects.get(UPI_number=to)
#            a.balance+=amount
#            a.save()
#         if BankAccount.objects.filter(UPI_number=to).exists():
#            a=BankAccount.objects.get(UPI_number=to)
#            a.balance+=amount
#            a.save()
#         return JsonResponse({'message':'Tranaction successfully done'},status=200) 

def transaction(request):
   if request.user.is_authenticated: 
      if request.method=='GET': 
        id=request.user.id
        print(id)
        phone1=Paywind_User.objects.get(id=id)
        phone=phone1.username
        amount=request.GET.get('amount')
        pin=request.GET.get('pin')
        to=request.GET.get('to')
        method=request.GET.get('method')
     #    id=6
     #    amount=100
     #    pin=1234
     #    to=9569673877
        amnt=int(amount)
        pin1=int(pin)
      #   print(amount)
      #   print(pin)
      #   print(to)
      #   print(method)
      #   print(type(method))
        if amnt<=100000:
         if LinkedAccount.objects.filter(user_id=id).exists():
            u=LinkedAccount.objects.get(user_id=id)
            print(u,"hello")
            # print(u.id)
            # print(u.balance)
            if int(method)==2:
              w=Wallet.objects.get(user_id=id)
              if amnt<=w.amount: 
               if pin1==u.PIN:    
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to,status="success",UPI_number=phone)
                  id1=t.id
                  cb=Transactions.objects.get(id=id1)  
                  print('mariou')
                  w.amount-=amnt 
                  w.save()
                  if amnt<=100:
                   x=random.sample(range(5,20),1)
                   print(x[0])
                   cb.cashback=x[0]
                   cb.save()
                   w.amount+=x[0]
                   w.save()
                  if amnt<=500 and amnt>100:
                     x=random.sample(range(50,100),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt<=1000 and amnt>500:
                     x=random.sample(range(100,200),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt<=5000 and amnt>1000:
                     x=random.sample(range(200,500),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt<=10000 and amnt>5000:
                     x=random.sample(range(500,1000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt>10000:
                     x=random.sample(range(1000,3000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if LinkedAccount.objects.filter(UPI_number=to).exists():
                    a=LinkedAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  if BankAccount.objects.filter(UPI_number=to).exists():
                    a=BankAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  data1=[{'cashback':cb.cashback}]
                  k=random.sample(range(1,101),1)
                  print(k[0])
                  if k[0]%2==0 and k[0]>50:
                      l=random.sample(range(1,6),1)
                      print(l[0])
                      coupon1=Coupons.objects.get(value=l[0])
                      i=coupon1.id
                      cb.coupon_id=i
                      cb.save()
                      data2=[{'brand_name':coupon1.brand_name,'offer':coupon1.offer,'coupon_code':coupon1.coupon_code}]
                  else:
                      data2=[{'coupons':'No coupon applicable'}]
                  data=[]
                  data=data1+data2
                  return JsonResponse(data,safe=False) 
               else:
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                  t.status='FAILED'
                  t.reason='You have entered an inorrect UPI Pin for your account.Please retry your payment to proceed.'
                  t.save()
                  return JsonResponse({'message':'INCORRECT Pin'},status=400)
              else:
                t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                t.status='FAILED'
                t.reason='Your payment is unsuccessful as you do not have sufficient balance in your Bank account. Dont worrry, your money has NOT been deducted from the account.'
                t.save()
                return JsonResponse({'message':'Insufficient balance'},status=400)
            else:
             if amnt<=u.balance:
                if pin1==u.PIN:
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to,status="success",UPI_number=phone)
                  id1=t.id
                  cb=Transactions.objects.get(id=id1)
                  print('paul')
                  u.balance-=amnt 
                  u.save()
                  print('mario')
                  # w=Wallet.objects.get(user_id=id)
                  # w.amount-=amnt 
                  # w.save()
                  if amnt<=100:
                     x=random.sample(range(5,20),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=500 and amnt>100:
                     x=random.sample(range(50,100),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=1000 and amnt>500:
                     x=random.sample(range(100,200),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=5000 and amnt>1000:
                     x=random.sample(range(200,500),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=10000 and amnt>5000:
                     x=random.sample(range(500,1000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt>10000:
                     x=random.sample(range(1000,3000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if LinkedAccount.objects.filter(UPI_number=to).exists():
                    a=LinkedAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  if BankAccount.objects.filter(UPI_number=to).exists():
                    a=BankAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  data1=[{'cashback':cb.cashback}]
                  k=random.sample(range(1,101),1)
                  print(k[0])
                  if k[0]%2==0 and k[0]>50:
                      l=random.sample(range(1,6),1)
                      print(l[0])
                      coupon1=Coupons.objects.get(value=l[0])
                      i=coupon1.id
                      cb.coupon_id=i
                      cb.save()
                      data2=[{'brand_name':coupon1.brand_name,'offer':coupon1.offer,'coupon_code':coupon1.coupon_code}]
                  else:
                      data2=[{'coupons':'No coupon applicable'}]
                  data=[]
                  data=data1+data2
                  return JsonResponse(data,safe=False) 
                else:
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                  t.status='FAILED'
                  t.reason='You have entered an inorrect UPI Pin for your account.Please retry your payment to proceed.'
                  t.save()
                  return JsonResponse({'message':'INCORRECT Pin'},status=400)
             else:
                t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                t.status='FAILED'
                t.reason='Your payment is unsuccessful as you do not have sufficient balance in your Bank account. Dont worrry, your money has NOT been deducted from the account.'
                t.save()
                return JsonResponse({'message':'Insufficient balance'},status=400)
         elif BankAccount.objects.filter(user_id=id).exists():
           u=BankAccount.objects.get(user_id=id)
           if int(method)==2:
            w=Wallet.objects.get(user_id=id)
            if amnt<=w.amount: 
               if pin1==u.PIN:   
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to,status="success",UPI_number=phone)
                  id1=t.id
                  cb=Transactions.objects.get(id=id1)  
                  print('mario')
                  w.amount-=amnt 
                  w.save()
                  if amnt<=100:
                   x=random.sample(range(5,20),1)
                   print(x[0])
                   cb.cashback=x[0]
                   cb.save()
                   w.amount+=x[0]
                   w.save()
                  if amnt<=500 and amnt>100:
                     x=random.sample(range(50,100),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt<=1000 and amnt>500:
                     x=random.sample(range(100,200),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt<=5000 and amnt>1000:
                     x=random.sample(range(200,500),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt<=10000 and amnt>5000:
                     x=random.sample(range(500,1000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if amnt>10000:
                     x=random.sample(range(1000,3000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     w.amount+=x[0]
                     w.save()
                  if LinkedAccount.objects.filter(UPI_number=to).exists():
                    a=LinkedAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  if BankAccount.objects.filter(UPI_number=to).exists():
                    a=BankAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  data1=[{'cashback':cb.cashback}]
                  k=random.sample(range(1,101),1)
                  print(k[0])
                  if k[0]%2==0 and k[0]>50:
                      l=random.sample(range(1,6),1)
                      print(l[0])
                      coupon1=Coupons.objects.get(value=l[0])
                      i=coupon1.id
                      cb.coupon_id=i
                      cb.save()
                      data2=[{'brand_name':coupon1.brand_name,'offer':coupon1.offer,'coupon_code':coupon1.coupon_code}]
                  else:
                      data2=[{'coupons':'No coupon applicable'}]
                  data=[]
                  data=data1+data2
                  return JsonResponse(data,safe=False) 
               else:
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                  t.status='FAILED'
                  t.reason='You have entered an inorrect UPI Pin for your account.Please retry your payment to proceed.'
                  t.save()
                  return JsonResponse({'message':'INCORRECT Pin'},status=400)
            else:
                t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                t.status='FAILED'
                t.reason='Your payment is unsuccessful as you do not have sufficient balance in your Bank account. Dont worrry, your money has NOT been deducted from the account.'
                t.save()
                return JsonResponse({'message':'Insufficient balance'},status=400)
           else:
             if amnt<=u.balance:
                if pin1==u.PIN:
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to,status="success",UPI_number=phone)
                  id1=t.id
                  cb=Transactions.objects.get(id=id1)
                  print('paul')
                  u.balance-=amnt 
                  u.save()
                  print('mario')
                  # w=Wallet.objects.get(user_id=id)
                  # w.amount-=amnt 
                  # w.save()
                  if amnt<=100:
                     x=random.sample(range(5,20),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=500 and amnt>100:
                     x=random.sample(range(50,100),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=1000 and amnt>500:
                     x=random.sample(range(100,200),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=5000 and amnt>1000:
                     x=random.sample(range(200,500),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt<=10000 and amnt>5000:
                     x=random.sample(range(500,1000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if amnt>10000:
                     x=random.sample(range(1000,3000),1)
                     print(x[0])
                     cb.cashback=x[0]
                     cb.save()
                     u.balance+=x[0]
                     u.save()
                  if LinkedAccount.objects.filter(UPI_number=to).exists():
                    a=LinkedAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  if BankAccount.objects.filter(UPI_number=to).exists():
                    a=BankAccount.objects.get(UPI_number=to)
                    a.balance+=amnt
                    a.save()
                  data1=[{'cashback':cb.cashback}]
                  k=random.sample(range(1,101),1)
                  print(k[0])
                  if k[0]%2==0 and k[0]>50:
                      l=random.sample(range(1,6),1)
                      print(l[0])
                      coupon1=Coupons.objects.get(value=l[0])
                      i=coupon1.id
                      cb.coupon_id=i
                      cb.save()
                      data2=[{'brand_name':coupon1.brand_name,'offer':coupon1.offer,'coupon_code':coupon1.coupon_code}]
                  else:
                      data2=[{'coupons':'No coupon applicable'}]
                  data=[]
                  data=data1+data2
                  return JsonResponse(data,safe=False) 
                else:
                  t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                  t.status='FAILED'
                  t.reason='You have entered an inorrect UPI Pin for your account.Please retry your payment to proceed.'
                  t.save()
                  return JsonResponse({'message':'INCORRECT Pin'},status=400)
             else:
                t=Transactions.objects.create(user_id=id,amount=amount,to=to)
                t.status='FAILED'
                t.reason='Your payment is unsuccessful as you do not have sufficient balance in your Bank account. Dont worrry, your money has NOT been deducted from the account.'
                t.save()
                return JsonResponse({'message':'Insufficient balance'},status=400)
         else:
           return JsonResponse({'message':'Create account first.'},status=400)
        else:
           return JsonResponse({'message':'Cannot send more than one lakh'},status=400)
      else:
        return JsonResponse({'message':'Invalid request method'},status=400) 
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)       
    
def show_coupons(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
          id=request.user.id 
          #id=6
          list1=[]
          data=[]
          t=Transactions.objects.filter(user_id=id)
          #if t.coupon_id is not None:
          for x in t:
            if x.coupon_id is None:
              continue
            else:
          #     print(type(x.coupon_id))
          #     print(type(list(x.coupon_id)))
              list1+=list(str(x.coupon_id))
          print(list1)
          for i in list1:
              coup=Coupons.objects.get(id=int(i))
              print(int(i))
              print(coup.brand_name)
              data+=[{'brand_name':coup.brand_name,'offer':coup.offer,'coupon_code':coup.coupon_code,'id':i}]
          # data=[{'brand_name':x.brand_name,'offer':coupon1.offer,'coupon_code':coupon1.coupon_code}]
          print(data)
          return JsonResponse(data,status=200,safe=False)  
      else:
        return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},status=400)  

def view_coupon(request):
   if request.user.is_authenticated: 
      if request.method=='GET':
          id=request.GET.get('id') 
          if Coupons.objects.filter(id=id):
             c=Coupons.objects.filter(id=id).values('brand_name','offer','coupon_code')
             data=list(c)
             return JsonResponse(data,status=200,safe=False)   
          else:
             return JsonResponse({'message':'No coupon'},safe=False,status=400)  
      else:
         return JsonResponse({'message':'Invalid request method'},status=400) 
   else:
     return JsonResponse({'message':'Kindly log in first'},status=400) 
    
def Payment_history(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
       print('hit')
       id=request.user.id
     #    id=6    
      #   user1=Paywind_User.objects.filter(id=id).values("first_name","last_name").first()
     #    print(user1)
     #    a=user1['first_name']
     #    print(type(user1))
     #    print(a)
     #    print(type(a))
       user=Paywind_User.objects.get(id=id)
       phone=user.username
       if Transactions.objects.filter(user_id=id).exists():
        transaction=Transactions.objects.filter(user_id=id)
        list1=[]
        for t in transaction:
          if t.status=='success':
            # print('fg')
            # dict1={'amount':t.amount,'status':t.status,'time':t.time,'date':t.date,'to':t.to}
            list2=[{'status1':"-",'amount':t.amount,'status':t.status,'time':t.time,'date':t.date,'to':t.to,'id':t.id}]
          #  to1=t.to
            list1+=list2
          else:
             list2=[{'status1':"!",'amount':t.amount,'status':t.status,'time':t.time,'date':t.date,'to':t.to,'id':t.id}]
             list1+=list2
        if Transactions.objects.filter(to=phone).exists:
           print('hmss')
           transaction1=Transactions.objects.filter(to=phone)
          #  .order_by("time", "date")
           for x in transaction1:
             list3=[{'status1':"+",'amount':x.amount,'status':x.status,'time':x.time,'date':x.date,'to':x.UPI_number,'id':t.id}]
             print(x.UPI_number)
             id3=t.user_id
             list1+=list3
           print(list1)
        return JsonResponse(list1,status=200,safe=False) 
       else:
          return JsonResponse({'message':'No history'},status=200) 
      else:
        return JsonResponse({'message':'Invalid request method'},status=400) 
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)    

def individual_paymenthist(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
          id=request.user.id 
          user=Paywind_User.objects.get(id=id)
          firstname=user.first_name
          lastname=user.last_name
          phone=user.username 
          pers=request.GET.get('pers')
          id1=request.GET.get('id')
          print(pers)
          list1=[]   
          if Transactions.objects.filter(id=id1,user_id=id,to=pers,status='success').exists():
             t=Transactions.objects.filter(user_id=id,to=pers,status='success')
             for x in t:
              list2=[{'to':pers,'from':phone,'from_name':firstname+' '+lastname,'amount':x.amount,'status':x.status,'time':x.time,'date':x.date,'id':x.id}]
              list1=list2
          if Transactions.objects.filter(id=id1,user_id=id,to=pers,status='FAILED').exists():
             t=Transactions.objects.filter(user_id=id,to=pers,status='FAILED')
             for x in t:
              list3=[{'to':pers,'from':phone,'from_name':firstname+' '+lastname,'amount':x.amount,'status':x.status,'reason':x.reason,'time':x.time,'date':x.date,'id':x.id}]
              list1=list3
          if Transactions.objects.filter(id=id1,UPI_number=pers,to=phone,status='success').exists():
             t=Transactions.objects.filter(UPI_number=pers,to=phone,status='success')
             for x in t:
              list4=[{'from':pers,'to':phone,'to_name':firstname+' '+lastname,'amount':x.amount,'status':"+",'time':x.time,'date':x.date,'id':x.id}]
              list1=list4
          print(list1)
          return JsonResponse(list1,status=200,safe=False)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)   
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
        
def dropdown(request):
      if request.method=='GET':  
          val=request.GET.get('value') 
          print(val)
          d=Dropdowns.objects.get(value=val).pk
          e=Dropdowns.objects.filter(parent_id=d)
          list1=[]
          for x in e:
             a=x.value
             list1.append(a)
          print(list1)
          return JsonResponse(list1,status=200,safe=False)
      else:
        return JsonResponse({'message':'Invalid request method'},status=400)   
       
def branch_name(request):
   if request.method=='GET':  
      val=request.GET.get('value') 
      bank=request.GET.get('value1') 
      print(val)
      print(bank)
      d=Dropdowns.objects.get(value=val).pk
      e=Dropdowns.objects.filter(parent_id=d)
      list1=[]
      for x in e:
         a=x.value
         if a==bank:
            id1=x.id
            print(bank)
            print(id1)
            break
      f=Dropdowns.objects.filter(parent_id=id1)
      for x in f:
             g=x.value
             list1.append(g)
      print(list1)
      return JsonResponse(list1,status=200,safe=False)
   else:
     return JsonResponse({'message':'Invalid request method'},status=400)
    
# def check_balance(request):
#     if request.method=='GET':
#        pin=str(request.GET.get('pin'))
#        if LinkedAccount.objects.filter(PIN=pin).exists():
#           a=LinkedAccount.objects.filter(PIN=pin).values("balance")
#           return JsonResponse(list(a),status=200,safe=False)
#        elif BankAccount.objects.filter(PIN=pin).exists():
#           a=LinkedAccount.objects.filter(PIN=pin).values("balance")   
#           return JsonResponse(list(a),status=200,safe=False)          
#        else:
#           return JsonResponse({'message':'Incorrect PIN'},status=400)

def check_balance(request):
   if request.user.is_authenticated: 
      if request.method=='GET':
        pin=int(request.GET.get('pin'))
        id= request.user.id
        user=Paywind_User.objects.get(id=id)
        phone=user.username
        if LinkedAccount.objects.filter(UPI_number=phone).exists():
           a=LinkedAccount.objects.get(UPI_number=phone)
           p=a.PIN
           balance=str(a.balance)
           if pin==p:
              return JsonResponse(balance,status=200,safe=False)  
           else:
              return JsonResponse({'message':'Incorrect PIN'},status=400)
        elif BankAccount.objects.filter(UPI_number=phone).exists():
           a=BankAccount.objects.get(UPI_number=phone)
           p=a.PIN
           balance=str(a.balance)
           balance1=list(balance)
           if pin==p:
              return JsonResponse(balance1,status=200,safe=False)  
           else:
              return JsonResponse({'message':'Incorrect PIN'},status=400)
        else:
          return JsonResponse({'message':'Not registered.'},status=400) 
      else:
        return JsonResponse({'message':'Invalid request method'},status=400) 
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
   
def edit_pin(request):
   if request.user.is_authenticated: 
      if request.method=='GET':
       pin=request.GET.get('pin')
       id= request.user.id
      #  id=6
       user=Paywind_User.objects.get(id=id)
       phone=user.username
      #  if LinkedAccount.objects.filter(PIN=pin).exists():
      #     return JsonResponse({'message':'Correct PIN'},status=200)
      #  elif BankAccount.objects.filter(PIN=pin).exists():
      #     return JsonResponse({'message':'Correct PIN'},status=200)          
      #  else:
      #     return JsonResponse({'message':'Incorrect PIN'},status=400)
       g=LinkedAccount.objects.filter(UPI_number=phone).exists()
      #  print(g)
      #  print(type(g))
       if g==True:
           a=LinkedAccount.objects.get(UPI_number=phone)
           p=a.PIN
           if pin==str(p):
              return JsonResponse({'message':'Correct PIN'},status=200)  
           else:
              return JsonResponse({'message':'Incorrect PIN'},status=400)
       elif BankAccount.objects.filter(UPI_number=phone).exists():
           a=BankAccount.objects.get(UPI_number=phone)
           p=a.PIN
           if pin==str(p):
              return JsonResponse({'message':'Correct PIN'},status=200)  
           else:
              return JsonResponse({'message':'Incorrect PIN'},status=400)
       else:
          return JsonResponse({'message':'Not registered.'},status=400)  
      else:
        return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
      
def show_data(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
          id=request.user.id
         #  id=6
          user= Paywind_User.objects.get(id=id)
          UPI_no=user.username
          amount=request.GET.get('amount')
          if amount is None:
            return JsonResponse({"message":"Enter amount"},status=400) 
          else:
           amount1=int(amount)
           list1=[{'amount':amount1,'ADMIN':int(UPI_no)}]
           print(list1)
           return JsonResponse(list1,status=200,safe=False)
      else:
        return JsonResponse({'message':'Invalid request method'},status=400)    
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
      
def split_bill(request):
   if request.user.is_authenticated: 
      if request.method=='POST':  
          id=request.user.id
          user= Paywind_User.objects.get(id=id)
          UPI_no=user.username
          db=json.loads(request.body)
          amount=db['amount1']
          # no=db['no']
          # no1=int(no)
          # indi_amount=int(amount)/no1
          UPI_number=db.get('UPI')
          if amount is None:
           return JsonResponse({"message":"Fill the amount"},status=400)
          elif UPI_number is None:
           return JsonResponse({"message":"Fill the UPI number"},status=400)
          else:
           print(UPI_number)
           print(type(UPI_number))
           t=SplitBill.objects.create(value=amount)
           id1=t.id
           s=SplitBill.objects.create(value=UPI_no,parent_id=id1,admin="TRUE")
           s.status="paid"
           s.save()
           for x in UPI_number:
            number = x["numbers"]
            amnt= x["amount"]
            st=SplitBill.objects.create(value=number,parent_id=id1,indiv_amount=amnt)
            st.status="yet to be paid"
            st.save() 
            return JsonResponse({'message':'Success'},status=200)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
   
def splitbill_groups(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
          id=request.user.id  
          user=Paywind_User.objects.get(id=id)
          phone=user.username 
         #  phone='9524485485'
          data3=[]
          if SplitBill.objects.filter(value=phone,status='yet to be paid',delete1='false').exists():
           print('hi')
           s=SplitBill.objects.filter(value=phone,status='yet to be paid',delete1='false')
           print(s)
           for x in s:
             print('hi1') 
             id1=x.parent_id
             print(id1)
             data1=[]
             b=SplitBill.objects.filter(parent_id=id1,delete1='false')
             print(b)
             for i in b:
                print('hi2')
                if phone==i.value:
                 continue
                else:
                 print("jjk")
                 data1.append(int(i.value))
             data3+=[{'key':data1,'id':x.id}]
             print(data3)
           return JsonResponse(data3,status=200,safe=False)
         #  if SplitBill.objects.filter(value=phone,admin='TRUE').exists():
         #   print('hi')
         #   s=SplitBill.objects.filter(value=phone)
         #   print(s)
         #   for x in s:
         #     print('hi1') 
         #     id1=x.parent_id
         #     print(id1)
         #     data1=[]
         #     b=SplitBill.objects.filter(parent_id=id1)
         #     print(b)
         #     for i in b:
         #        print('hi2')
         #        if phone==i.value:
         #         continue
         #        else:
         #         print("jjk")
         #         data1.append(int(i.value))
         #     data3+=[{'key':data1,'id':x.id}]
         #     print(data3)
         #   return JsonResponse(data3,status=200,safe=False) 
          else:
            return JsonResponse({'message':'No split bill'},status=200) 
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
   
# def notification(request):
#  if request.user.is_authenticated: 
#        if request.method=='GET':  
#           id=request.user.id  
#           user=Paywind_User.objects.get(id=id)
#           phone=user.username
#           if SplitBill.objects.filter(value=phone).exists():
#             a=SplitBill.objects.filter(value=phone).first()
#             id1=a.parent_id
#             b=SplitBill.objects.get(id=id1)
#             amount=b.value
#             ide=b.id
#             amnt=int(amount)
#             c=SplitBill.objects.get(parent_id=id1,admin="TRUE")
#             to=c.value
#             count=0
#             d=SplitBill.objects.filter(value=phone)
#             for x in d:
#                count+=1
#             final_amount=amnt/count
#             data=[{'ye mujhe bhej':ide,'to':to,'amount':final_amount}]
#             return JsonResponse(data,safe=False)
#        else:
#            return JsonResponse({'message':'No split bill'},status=400) 

def individual_notification(request): 
   if request.user.is_authenticated: 
      if request.method=='GET':  
          id=request.user.id 
          user=Paywind_User.objects.get(id=id)  
          phone=user.username 
          id1=request.GET.get('id1')
          print(id1)
          s=SplitBill.objects.get(id=id1,delete1='false') 
          id2=s.parent_id
          ad=SplitBill.objects.get(parent_id=id2,admin="TRUE",delete1='false') 
          to=ad.value
         #  a=SplitBill.objects.get(id=id2)
          amount=s.indiv_amount
          data=[{'to':to,'amount':amount,'id':id1}]
          print(data)
          return JsonResponse(data,status=200,safe=False)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
   
# def pay_splitbill(request):
#    if request.user.is_authenticated: 
#       if request.method=='GET':  
#           id1=request.user.id 
#           user=Paywind_User.objects.get(id=id1)
#           phone=user.username
#           id=request.GET.get('ide')
#           b=SplitBill.objects.filter(parent_id=id)
#           for x in b:
#              if x.value==phone:
#                 x.status='paid'
#                 x.save()
#           return JsonResponse({'message':'Done'},status=200)  
#       else:
#          return JsonResponse({'message':'Invalid request method'},status=400)  
#    else:
#         return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
         
def pay_splitbill(request):
   if request.user.is_authenticated: 
      if request.method=='POST':  
         id1=request.user.id 
         user=Paywind_User.objects.get(id=id1)
         phone=user.username
         db=json.loads(request.body)
         id=db['id']
         pin1=db['pin']
         if LinkedAccount.objects.filter(UPI_number=phone).exists():
               a=LinkedAccount.objects.get(UPI_number=phone)
               pin=a.PIN
         elif BankAccount.objects.filter(UPI_number=phone).exists():
               a=BankAccount.objects.get(UPI_number=phone)
               pin=a.PIN
         else:
           return JsonResponse({'message':'Invalid pin'},status=400)   
         if int(pin1)==pin:
            b=SplitBill.objects.get(id=id,delete1='false')
            amnt=b.indiv_amount
            b.status="paid"
            b.save()
            p_id=b.parent_id
            c=SplitBill.objects.get(parent_id=p_id,admin="TRUE",delete1='false')
            to=c.value
            # d=SplitBill.objects.get(id=p_id)
            # amnt=int(d.value)
            Transactions.objects.create(user_id=id1,amount=amnt,to=to,status="success",UPI_number=phone)
            if LinkedAccount.objects.filter(UPI_number=phone).exists():
               u=LinkedAccount.objects.get(UPI_number=phone)
               u.balance-=amnt
               u.save()
            if BankAccount.objects.filter(UPI_number=phone).exists():
               u=BankAccount.objects.get(UPI_number=phone)
               u.balance-=amnt
               u.save()
            if LinkedAccount.objects.filter(UPI_number=to).exists():
               v=LinkedAccount.objects.get(UPI_number=to)
               v.balance+=amnt
               v.save()
            if BankAccount.objects.filter(UPI_number=to).exists():
               v=BankAccount.objects.get(UPI_number=to)
               v.balance+=amnt
               v.save()
            return JsonResponse({'message':'Done'},status=200)  
         else:
            return JsonResponse({'message':'Wrong pin'},status=400)  
      else:
        return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
    return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)       

def messages(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
          print('hit')
          id=request.user.id 
          user=Paywind_User.objects.get(id=id)
          phone=user.username 
          # pers=request.GET.get('pers')
          list1=[]     
          #sent 
          print('')
          if Transactions.objects.filter(user_id=id).exists():
             t=Transactions.objects.filter(user_id=id)
             for x in t:
               # print('hi')
               count=0
               for i in list1:
                  if i==x.to:
                     # print('go')
                     break
                  else:
                     count+=1
                     continue
               if count==len(list1):
                list1.append(x.to)
          print(list1)
          if Transactions.objects.filter(to=phone).exists():
             b=Transactions.objects.filter(user_id=id)
             for x in b:
               print('hi')
               count=0
               for i in list1:
                  if i==x.to:
                     break
                  else:
                     count+=1
                     continue
               if count==len(list1):
                list1.append(x.to)
          print(list1)
          return JsonResponse(list1,status=200,safe=False)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
   
def individual_messages(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
          id=request.user.id 
          user=Paywind_User.objects.get(id=id)
          phone=user.username 
          pers=request.GET.get('pers')
          print(pers)
          list1=[]     
          if Transactions.objects.filter(user_id=id,to=pers,status='success').exists():
             t=Transactions.objects.filter(user_id=id,to=pers,status='success')
             for x in t:
              list2=[{'amount':x.amount,'status':"-"}]
              list1+=list2
          if Transactions.objects.filter(user_id=id,to=pers,status='FAILED').exists():
             t=Transactions.objects.filter(user_id=id,to=pers,status='FAILED')
             for x in t:
              list3=[{'amount':x.amount,'status':'!'}]
              list1+=list3
          if Transactions.objects.filter(UPI_number=pers,to=phone,status='success').exists():
             t=Transactions.objects.filter(UPI_number=pers,to=phone,status='success')
             for x in t:
              list4=[{'amount':x.amount,'status':"+"}]
              list1+=list4
          print(list1)
          return JsonResponse(list1,status=200,safe=False) 
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
       
def profile(request):
   if request.user.is_authenticated: 
      if request.method=='GET':  
          id=request.user.id 
         #  id =6
          user=Paywind_User.objects.get(id=id)
          phone_no=user.username 
          UPI_number=phone_no
          email=user.email
          first_name=user.first_name
          last_name=user.last_name
          name=first_name+' '+last_name
          gender=user.gender
          dict1={'phone_no':phone_no,'UPI_number':UPI_number,'email':email,'name':name,'gender':gender}
          print(dict1)
          if BankAccount.objects.filter(user_id=id).exists():
             user1=BankAccount.objects.get(user_id=id)
             account_number=user1.account_number
             nominee=user1.nominee
             UPI_id=user1.UPI_id
             address=user1.address
             dict2={'account_number':account_number,'nominee':nominee,'UPI_id':UPI_id,'address':address}
             dict3 = dict1.copy()
             for key, value in dict2.items():  # use for loop to iterate dict2 into the dict3 dictionary  
              dict3[key] = value  
             data=[dict3]
            #  print(dict3)
          if LinkedAccount.objects.filter(user_id=id).exists():
             user1=LinkedAccount.objects.get(user_id=id)
             bank_name=user1.bank_name
             branch_name=user1.branch_name
             account_number=user1.account_number
             UPI_id=user1.UPI_id
             dict2={'account_number':account_number,'bank_name':bank_name,'UPI_id':UPI_id,'branch_name':branch_name}
             dict3 = dict1.copy()
             for key, value in dict2.items():  # use for loop to iterate dict2 into the dict3 dictionary  
              dict3[key] = value 
             data=[dict3]
          print(dict3)
          return JsonResponse(data,status=200,safe=False)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)  
   # else:
      #   return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
      
def dynamicpanel(request):
   if request.user.is_authenticated:
      if request.method=='GET':  
          id=request.user.id
          user=Paywind_User.objects.get(id=id)
          phone_no=user.username
          first_name=user.first_name
          last_name=user.last_name
          name=first_name+' '+last_name
          dp=dynamic_panel.objects.filter(delete1='false')
          data0=[{'user':[{'name':name,'phone_no':phone_no}]}]
          data=[]
          for x in dp:
             data1= [{'value': x.value,'state': x.state,'order1':x.order1,'pop_up':x.state1,'icon':str(x.icon)}]
             data+=data1
          data2=[{'dashboard':data}]
          data3=data0+data2
          print(data)   
          return JsonResponse(data3,status=200,safe=False)
      else:
       return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
   
def otp_wallet(request):
 if request.user.is_authenticated:  
  id1=request.user.id
  if Wallet.objects.filter(user_id=id1,deactivate='False').exists():
        return JsonResponse({'message':'Already activated'},status=400) 
  else: 
   if request.method=='POST': 
   # id1=request.user.id
    user=Paywind_User.objects.get(id=id1)
    f=json.loads(request.body)
    phone=f['phone']
    print(phone)
    if phone==user.username:
      if Paywind_User.objects.filter(username=phone).exists():
       user=Paywind_User.objects.get(username=phone)
       id=user.id
       inst=OTP.objects.create(user_id=id,phone=user.username,email=user.email,type='Wallet')
       x=random.sample(range(999,9999),1)
       inst.otp=x[0]
       inst.save()
    #    five_minutes_ago = django.utils.timezone.now() + datetime.timedelta(minutes=-5)
    #    fil = OTP.objects.filter(req_time__gte=five_minutes_ago)
    #    for x in fil:
    #        x.status='active'
    #        x.save()
       ctx ={'otp':x,
             'UPI_id':user.username,
             'UPI_number':user.username,
             'email':user.email
             }
       email_content = render_to_string('email.html',ctx)
       subject = 'OTP'
       from_email = 'ananyajain386@gmail.com'
       recipient_list = [user.email]
       send_mail(subject, 'OTP Verification', from_email, recipient_list, html_message=email_content)
       return JsonResponse({'message':'OTP sent successfully.'},status=200)
      else:
       return JsonResponse({'message':'User not registered.'},status=400)
    else:
      return JsonResponse({'message':'Enter correct number'},status=400) 
   else:
     return JsonResponse({'message':'Invalid request method'},status=400)  
 else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  
    
def confirmotp_wallet(request):
   if request.user.is_authenticated: 
      if request.method=='POST': 
       time_for_now =  timezone.now()
       print(time_for_now)
     #  Time_difference=
       f=json.loads(request.body)
       phone=f['phone']
       otp=f['otp']
       if OTP.objects.filter(phone=phone,status='active',type='Wallet').exists():
        user=OTP.objects.filter(phone=phone,status='active',type='Wallet').last()
        print(user)
        time=user.time
        Time_difference=time_for_now -time
        td=Time_difference.seconds
        print(Time_difference.seconds)
        a=user.otp
        print(a)
        if td<120:
         if otp==str(a):
         #   user1=Paywind_User.objects.get(username=phone)
           user.status='expired'
           user.save()
           return JsonResponse({'message':'OTP matched.'},status=200)
         else:
          print('pen')
          return JsonResponse({'message':'OTP not matched.'},status=400)
        else:
         user.status='expired'
         user.save()
       else:
        return JsonResponse({'message':'Set OTP first'},status=400)   
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)   
   else:
        return JsonResponse({'message':'Kindly log in first'},safe=False,status=400)  

def activate_wallet(request):
   if request.user.is_authenticated: 
    if request.method=='POST': 
       id=request.user.id
       print(id)
       f=json.loads(request.body)
       amount1=f['amount1']
       if BankAccount.objects.filter(user_id=id).exists():
          print('hi')  
          m=BankAccount.objects.get(user_id=id)
          id1=m.id
          bal=m.balance
          if bal<int(amount1):
             return JsonResponse({'message':'Insufficient Balance'},status=400)
          else:
             Wallet.objects.create(user_id=id,account1_id=id1,amount=amount1)
             m.balance-=int(amount1)
             m.save()
             return JsonResponse({'message':'Wallet activated.'},status=200)
       if LinkedAccount.objects.filter(user_id=id).exists():
          m=LinkedAccount.objects.get(user_id=id)
          id1=m.id
          bal=m.balance
          if bal<int(amount1):
             return JsonResponse({'message':'Insufficient Balance'},status=400)
          else:
             Wallet.objects.create(user_id=id,account2_id=id1,amount=amount1)
             m.balance-=int(amount1)
             m.save()
             return JsonResponse({'message':'Wallet activated.'},status=200)
    else:
       return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
        return JsonResponse({'message':'Kindly log in first'},status=400)   

# transaction ke continue button pe hit
def continue1(request):
   if request.user.is_authenticated: 
      if request.method=='GET': 
       id=request.user.id
       if Wallet.objects.filter(user_id=id,deactivate='False').exists():
          print('hi')
          method=2
       else:
          method=1
      #  data={'method':method}
       data=str(method)
       return JsonResponse(data,status=200,safe=False)
      else:
       return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
    return JsonResponse({'message':'Kindly log in first'},status=400)  
   
def autoincrement_wallet(request):
   if request.user.is_authenticated: 
     if request.method=='POST': 
       id=request.user.id
       f=json.loads(request.body)
       less_than1=f['amount1']
       increase_by1=f['amount2']
       w=Wallet.objects.get(user_id=id,deactivate='False')
       w.less_than=less_than1
       w.increase_by=increase_by1
       w.autoincrement="True"
       w.save()
       return JsonResponse({'message':'Changed made'},status=200)
     else:
        return JsonResponse({'message':'Invalid request method'},status=400)  
   else:
     return JsonResponse({'message':'Kindly log in first'},status=400)  

# transaction pe hit
def increment_wallet(request):
   if request.user.is_authenticated: 
      if request.method=='GET': 
       id=request.user.id
       if Wallet.objects.filter(user_id=id,deactivate='False').exists():
          w=Wallet.objects.get(user_id=id)
          if w.autoincrement=="True":
           if w.amount<w.less_than:
             w.amount+=w.increase_by 
             w.save()
             if LinkedAccount.objects.filter(user_id=id).exists():
               v=LinkedAccount.objects.get(user_id=id)
               v.balance-=w.increase_by 
               v.save()
             if BankAccount.objects.filter(user_id=id).exists():
               v=BankAccount.objects.get(user_id=id)
               v.balance-=w.increase_by 
               v.save()
             return JsonResponse({'message':'Ok'},status=200)
           else:
             return JsonResponse({'message':'Ok'},status=200)
          else:
             return JsonResponse({'message':'Ok'},status=200)
       else:
           return JsonResponse({'message':'Ok'},status=200)
      else:
        return JsonResponse({'message':'Invalid request method'},status=400)
   else:
      return JsonResponse({'message':'Kindly log in first'},status=400)  
   
def deactivate(request):
   if request.user.is_authenticated: 
      if request.method=='GET': 
         id=request.user.id
         if Wallet.objects.filter(user_id=id,deactivate='False').exists():
          w=Wallet.objects.get(user_id=id)
          w.deactivate='True'
          w.save()
          if w.amount!=0:
             amnt=w.amount
             if BankAccount.objects.filter(id=w.account1).exists():
                a=BankAccount.objects.get(id=w.account1)
                a.balance+=amnt
                a.save()
             if LinkedAccount.objects.filter(id=w.account2).exists():
                a=BankAccount.objects.get(id=w.account1)
                a.balance+=amnt
                a.save()
             return JsonResponse({'message':'Activated successfully'},status=200)  
          else:
            return JsonResponse({'message':'Activated successfully'},status=200)  
         else:
            return JsonResponse({'message':'No wallet account'},status=400)  
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)
   else:
       return JsonResponse({'message':'Kindly log in first'},status=400)      
       
def activate_postpaid(request):
   if request.user.is_authenticated: 
      if request.method=='POST': 
         id=request.user.id
         db=json.loads(request.body)
         pan_number=db['pan']
         dob=db['dob']
         print(type(dob))
         aadhar_number=db['aadhar']
         email=db['email']
         user=Paywind_User.objects.get(id=id)
         print(type(str(user.date_of_birth)))
         if BankAccount.objects.filter(user_id=id).exists(): 
          print('dfgh')
          la=BankAccount.objects.get(user_id=id)
          if str(user.date_of_birth)==dob:  
           if str(user.email)==email:
            if str(la.aadhaar_card_no)==aadhar_number:
              if str(la.pan_card_no)==pan_number:
               inst=OTP.objects.create(user_id=id,phone=user.username,email=user.email,type='Postpaid')
               x=random.sample(range(999,9999),1)
               inst.otp=x[0]
               inst.save()
               ctx ={'otp':x,
                'UPI_id':user.username,
                'UPI_number':user.username,
                'email':user.email}
               email_content = render_to_string('email.html',ctx)
               subject = 'OTP'
               from_email = 'ananyajain386@gmail.com'
               recipient_list = [user.email]
               send_mail(subject, 'OTP Verification', from_email, recipient_list, html_message=email_content)
               return JsonResponse({'message':'OTP sent successfully.'},status=200)
              else:
                return JsonResponse({'message':'Enter correct pan number'},status=400)   
            else:
              return JsonResponse({'message':'Enter correct aadhar number'},status=400)  
           else:
            return JsonResponse({'message':'Enter correct email'},status=400) 
          else:
             return JsonResponse({'message':'Enter correct date of birth'},status=400)    
         elif LinkedAccount.objects.filter(user_id=id).exists():  
          if str(user.date_of_birth)==dob:  
           if str(user.email)==email:
            inst=OTP.objects.create(user_id=id,phone=user.username,email=user.email,type='Postpaid')
            x=random.sample(range(999,9999),1)
            inst.otp=x[0]
            inst.save()
            ctx ={'otp':x,
             'UPI_id':user.username,
             'UPI_number':user.username,
             'email':user.email
             }
            email_content = render_to_string('email.html',ctx)
            subject = 'OTP'
            from_email = 'ananyajain386@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, 'OTP Verification', from_email, recipient_list, html_message=email_content)
            return JsonResponse({'message':'OTP sent successfully.'},status=200)
           else:
            return JsonResponse({'message':'Enter correct email'},status=400)  
          else:
             return JsonResponse({'message':'Enter correct date of birth'},status=400)
         else:
            return JsonResponse({'message':'Create account first'},status=400)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)   
   else:
     return JsonResponse({'message':'Kindly log in first'},status=400)       
   
def confirmotp_postpaid(request):
   if request.user.is_authenticated: 
      if request.method=='POST': 
         id=request.user.id
         db=json.loads(request.body)
         pan_number=db['pan']
         aadhar_number=db['aadhar']
         dob=db['dob']
         email=db['email'] 
         otp=db['otp']
         o=OTP.objects.filter(user_id=id,type="Postpaid").last()
         if o.otp==int(otp):
          if BankAccount.objects.filter(user_id=id).exists():
             a=BankAccount.objects.get(user_id=id)
             PostPaid.objects.create(user_id=id,account1_id=a.id,pan_card_no=pan_number,date_of_birth=dob,aadhaar_card_no=aadhar_number)
             return JsonResponse({'message':'Postpaid activated successfully'},status=200)
          if LinkedAccount.objects.filter(user_id=id).exists():
             a=LinkedAccount.objects.get(user_id=id) 
             PostPaid.objects.create(user_id=id,account2_id=a.id,pan_card_no=pan_number,date_of_birth=dob,aadhaar_card_no=aadhar_number)
             return JsonResponse({'message':'Postpaid activated successfully'},status=200)
         else:
            return JsonResponse({'message':'Wrong otp'},status=400)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400)   
   else:
      return JsonResponse({'message':'Kindly log in first'},status=400)    
   
def cibil_score(request):
   if request.user.is_authenticated: 
      if request.method=='GET': 
         id=request.user.id
         if PostPaid.objects.filter(user_id=id,deactivate="False").exists():
          c=PostPaid.objects.get(user_id=id)
          cibil_score=c.CIBIL_Score
          Credit_Limit=c.Credit_Limit
         # cibil_score=2
         # Credit_Limit=2
          data="Your CIBIL Score is "+str(cibil_score)+" and Credit Limit is Rs."+str(Credit_Limit)
          return JsonResponse(data,status=200,safe=False)
         else:
           data='Postpaid not activated'
           return JsonResponse(data,status=200,safe=False)
      else:
         return JsonResponse({'message':'Invalid request method'},status=400) 
   else:
    return JsonResponse({'message':'Kindly log in first'},status=400)   

def paybypostpaid(request):
    if request.user.is_authenticated: 
      if request.method=='POST': 
         id=request.user.id
