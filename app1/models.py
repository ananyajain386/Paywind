from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class Paywind_User(AbstractUser):
    gender=models.CharField(max_length=30,null=True,blank=True)
    date_of_birth=models.DateField(blank=True,null=True)
    # UPI_id=models.CharField(max_length=50,blank=True,null=True,unique=True)
    # PIN=models.IntegerField(blank=True,null=True,unique=True)
    # age=models.IntegerField(blank=True,null=True)
    # phone_regex=RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number=models.CharField(validators=[phone_regex], max_length=17,blank=True,null=True,unique=True) 
    class Meta:
        db_table = "Paywind_User"
class SplitBill(models.Model):
    value=models.CharField(max_length=200,blank=True,null=True)
    parent=models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    admin=models.CharField(max_length=20,blank=True,null=True)
    status=models.CharField(max_length=20,blank=True,null=True)
    indiv_amount=models.IntegerField(blank=True,null=True)
    delete1=models.CharField(max_length=20,blank=True,null=True,default="false")
    class Meta:
        db_table = "Split_Bill"
class Coupons(models.Model):
    brand_name=models.CharField(max_length=200,blank=True,null=True)
    value=models.IntegerField(blank=True,null=True,default=0)
    offer=models.CharField(max_length=200,blank=True,null=True)
    # valid_till=
    coupon_code=models.CharField(max_length=200,blank=True,null=True)
    class Meta:
        db_table ="Coupons" 
class BankAccount(models.Model):
     # username=phone_no=UPI_number
     user= models.ForeignKey(Paywind_User,on_delete=models.CASCADE,null=True)
     age=models.IntegerField(blank=True,null=True)
     nominee=models.CharField(max_length=120,null=True,blank=True)
     phone_regex=RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
     nominee_phoneno=models.CharField(validators=[phone_regex], max_length=17,blank=True,null=True,unique=True) 
     aadhaar_card=models.FileField(blank=True,null=True)
     pan_card=models.FileField(blank=True,null=True)
     aadhaar_card_no=models.CharField(max_length=50,blank=True,null=True,unique=True)
     pan_card_no=models.CharField(max_length=50,blank=True,null=True,unique=True)
     marital_status=models.CharField(max_length=10,null=True,blank=True)
     photo=models.ImageField(upload_to='Pictures/',blank=True,null=True)
     address=models.CharField(max_length=120,null=True,blank=True)
     role=models.CharField(max_length=10,null=True,blank=True)
     UPI_id=models.CharField(max_length=50,blank=True,null=True,unique=True)
     UPI_number=models.CharField(max_length=50,blank=True,null=True,unique=True)
     account_number=models.CharField(max_length=15,blank=True,null=True,unique=True) 
     balance=models.IntegerField(blank=True,null=True)
     PIN=models.IntegerField(blank=True,null=True)
     class Meta:
        db_table = "BankAccount"
class LinkedAccount(models.Model):
     user= models.ForeignKey(Paywind_User,on_delete=models.CASCADE,null=True)
     UPI_number=models.CharField(max_length=50,blank=True,null=True,unique=True)
     UPI_id=models.CharField(max_length=50,blank=True,null=True,unique=True)
     branch_name=models.CharField(max_length=200,blank=True,null=True)
     bank_name=models.CharField(max_length=100,blank=True,null=True)
     account_number=models.CharField(max_length=20,blank=True,null=True,unique=True) 
     account_type=models.CharField(max_length=100,blank=True,null=True)
     IFSC_code=models.CharField(max_length=100,blank=True,null=True)
     balance=models.IntegerField(blank=True,null=True)
     PIN=models.IntegerField(blank=True,null=True)
     class Meta:
        db_table = "LinkedAccount"
class OTP(models.Model):
    user= models.ForeignKey(Paywind_User,on_delete=models.CASCADE,null=True)
    phone=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(null=True,blank=True)
    otp=models.IntegerField(blank=True,null=True)
    status=models.CharField(max_length=10,blank=True,null=True,default='active')
    # created_at = models.DateTimeField(auto_now=True)
    # expiration_time = models.DateTimeField()
    time= models.DateTimeField(null=True,auto_now=True)
    type=models.CharField(max_length=20,blank=True,default="Login")
    class Meta:
        db_table = "OTP"
class Transactions(models.Model):
    user=models.ForeignKey(Paywind_User,on_delete=models.CASCADE,null=True)
    coupon=models.ForeignKey(Coupons,on_delete=models.CASCADE,null=True)
    # type= models.CharField(max_length=10,blank=True,null=True)
    date= models.DateField(null=True,auto_now=True)
    time= models.TimeField(null=True,auto_now=True)
    amount= models.IntegerField(blank=True,null=True)
    to=models.CharField(max_length=20,blank=True,null=True) 
    status=models.CharField(max_length=10,blank=True,null=True) 
    reason=models.CharField(max_length=200,blank=True,null=True)
    cashback=models.IntegerField(blank=True,null=True,default=0)
    UPI_number=models.CharField(max_length=200,blank=True,null=True)
    class Meta:
        db_table ="Transactions"      
class Dropdowns(models.Model):
    parent=models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    value=models.CharField(max_length=200,blank=True,null=True) 
    edit=models.CharField(max_length=20,blank=True,null=True,default="False") 
    delete1=models.CharField(max_length=20,blank=True,null=True,default="False") 
    class Meta:
        db_table ="Dropdowns"
class dynamic_panel(models.Model):
    value=models.CharField(max_length=200,blank=True,null=True) 
    delete1=models.CharField(max_length=10,blank=True,null=True) 
    state=models.CharField(max_length=100,blank=True,null=True) 
    order1=models.IntegerField(blank=True,null=True)  
    state1=models.CharField(max_length=100,blank=True,null=True) 
    icon=models.FileField(blank=True)
    class Meta:
        db_table ="Dynamic_panel"
class Wallet(models.Model):
    user=models.ForeignKey(Paywind_User,on_delete=models.CASCADE,null=True)
    account1=models.ForeignKey(BankAccount,on_delete=models.CASCADE,null=True)
    account2=models.ForeignKey(LinkedAccount,on_delete=models.CASCADE,null=True)
    amount=models.IntegerField(blank=True,null=True)
    deactivate=models.CharField(max_length=20,blank=True,default="False") 
    less_than=models.IntegerField(blank=True,null=True)
    increase_by=models.IntegerField(blank=True,null=True)
    autoincrement=models.CharField(max_length=20,blank=True,default="False") 
    class Meta:
        db_table ="Wallet"
class PostPaid(models.Model):
    user=models.ForeignKey(Paywind_User,on_delete=models.CASCADE,null=True)
    account1=models.ForeignKey(BankAccount,on_delete=models.CASCADE,null=True)
    account2=models.ForeignKey(LinkedAccount,on_delete=models.CASCADE,null=True)
    deactivate=models.CharField(max_length=20,blank=True,default="False") 
    CIBIL_Score=models.IntegerField(blank=True,null=True,default=500)
    Credit_Limit=models.IntegerField(blank=True,null=True,default=6000)
    bill=models.IntegerField(blank=True,null=True)
    penality=models.IntegerField(blank=True,null=True)
    penality_no=models.IntegerField(blank=True,null=True)
    time= models.DateTimeField(null=True,auto_now=True)
    pan_card_no=models.CharField(max_length=50,blank=True,null=True,unique=True)
    date_of_birth=models.DateField(blank=True,null=True)
    aadhaar_card_no=models.CharField(max_length=50,blank=True,null=True,unique=True)
    class Meta:
        db_table ="PostPaid"