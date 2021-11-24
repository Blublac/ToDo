from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
 


@receiver(post_save,sender=User)

def send_activation_email(sender,instance,created,**kwargs):

    if created:
        message = f"""Hello, {instance.first_name}. thank you for signing up on our platform.we are very glad
        
        
    
        
        """
    

        send_mail(subject="Activation mail", message=message,recipient_list=[instance.email],from_email = 'admin@reportly.com')

   