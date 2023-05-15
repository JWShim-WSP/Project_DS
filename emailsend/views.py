from django.views.generic import FormView, TemplateView
from .forms import ContactForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

# Here, we are going to use ClassView to execute a form and send email with contents directly. Rather than using function-based form with model to save into db
class ContactView(FormView):
    form_class = ContactForm
    template_name = 'emailsend/main.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            #from_email = form.cleaned_data['your_email_Address']
            #name = form.cleaned_data['your_first_Name'] + ' ' + form.cleaned_data['your_last_Name']
            to_emails = form.cleaned_data['to'].split(",")
            cc_emails = form.cleaned_data['cc'].split(",")
            bcc_emails = form.cleaned_data['bcc'].split(",")

            subject = form.cleaned_data['subject']

            #this is for when you send email for the sender
            #message = f'{name} with email address of {from_email} contacted you:'
            #message += f'\n"{subject}"\n\n'
            message = f'{subject}\n'
            message += form.cleaned_data['message']

            files = request.FILES.getlist('attach')

            try:

                mail = EmailMessage(subject, message, from_email=settings.EMAIL_HOST_USER, to=to_emails, cc=cc_emails, bcc=bcc_emails)

                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)

                mail.send()

                error_message = f'Success: sent email to {to_emails}'
                # reset the form for another email
                form = self.form_class()

            except:
                error_message = 'Failure'

        else:
            error_message = 'Form-Error'

        return render(request, self.template_name, {'form': form, 'message': error_message })

"""
def bstContactUs(request):
    # Check if method is POST
    if request.method == "POST":
        #Take in the data the user submitted and save it
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Instead of form saving in db, it's time to send email to Admin
            #form.save()
            send(request.POST)
            
            message = "Success"
        else:
            message = form.errors
    else:
        message = "Pass"
        form = ContactUsForm()

    return render(request, 'contactus/bstcontactus.html',{
        "message": message,
        "form": form
    })
"""

