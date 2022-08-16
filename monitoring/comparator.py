from datetime import datetime
from django.forms.models import model_to_dict
from companies.models import Company
from monitoring.sender import send_email
from users.models import CustomUser
from .models import Monitoring


def compare(quotes):

    #quotes = model_to_dict(quotes)
    monitoring = Monitoring.objects.all()

    for moni in monitoring:
        quote = list(
            filter(lambda q: q.parent_company == moni.company, quotes))[0]
        print(quote)

        company = Company.objects.get(code=moni.company.code)

        notification_user(moni)

        if quote.value < company.min_quote:
            # Cotação menor
            company.min_quote = quote.value
            company.save()
            notification_user(moni)

        elif quote.value > company.max_quote:
            # Cotação maior
            company.max_quote = quote.value
            company.save()
            notification_user(moni)


def notification_user(moni):

    last_notification = datetime(moni.last_notification)
    delta = datetime.now() - last_notification

    if delta >= moni.frequency:
        send_email(moni.user.uid, moni.id)
