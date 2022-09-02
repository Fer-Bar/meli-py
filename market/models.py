from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.core.mail import send_mail


class Seller(models.Model):
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor')
    nickname = models.CharField(max_length=45, unique=True)
    phone = PhoneNumberField()
    email = models.EmailField(max_length=30, unique=True)
    

    def __str__(self):
        return self.nickname

class Product(models.Model):
    seller_fk = models.ForeignKey(Seller, on_delete=models.CASCADE, 
                                  related_name="seller_fk")
    title = models.CharField(max_length=80)
    product_id = models.CharField(max_length=30)
    sellerid = models.CharField(max_length=30, null=True)
    brand = models.CharField(max_length=30)
    ppv = models.IntegerField()
    brand_discount_allow = models.FloatField(default=0)
    base_price = models.IntegerField(null=True)
    original_price = models.IntegerField(null=True)
    discount_ammount = models.IntegerField(null=True)
    discount_percent = models.FloatField(null=True)
    fault_date = models.DateTimeField(null=True)    
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    
    
    def raise_alert(self):
        return self.discount_percent > self.brand_discount_allow or self.ppv > self.base_price 
    
    def email_notify(self):
        if self.raise_alert() and self.fault_date is None:
            self.fault_date = timezone.now()
            self.save()
            seller_email = self.seller_fk.email
            supervisor_email = self.seller_fk.supervisor.email
            subject = f'Precio fuera del rango permitido - Artículo {self.product_id}'
            message = f"El artículo: '{self.title}', cuyo PVP es ${self.ppv}, posee un precio publicado de ${self.base_price}. Favor de corregir."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [seller_email, supervisor_email, ]
            if send_mail( subject, message, email_from, recipient_list ):
                print(f'Mail was Send to {seller_email} and {supervisor_email}')
            else:
                print('Error with the send of the mail')
        print('The user was notified or is not necessarily.')
    
    def __str__(self):
        return self.title
