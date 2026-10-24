from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render

from content.views import build_context

from .forms import ContactForm


def contact(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = ContactForm(request.POST)
    if form.is_valid():
        message = form.save()
        notify_owner(message)
        messages.success(request, "Thanks, your message was sent. I'll get back to you soon.")
        return redirect("/#contact")

    # Re-render the home page with the form errors shown next to the form.
    context = build_context(contact_form=form)
    context["contact_has_errors"] = True
    return render(request, "content/home.html", context, status=400)


def notify_owner(message):
    """Email the owner if CONTACT_NOTIFY_EMAIL is set. Never fail the request on email errors."""
    recipient = settings.CONTACT_NOTIFY_EMAIL
    if not recipient:
        return
    try:
        send_mail(
            subject=f"Portfolio message from {message.name}",
            message=f"From: {message.name} <{message.email}>\n\n{message.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=True,
        )
    except Exception:
        pass
