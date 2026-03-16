from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import logging
import traceback

logger = logging.getLogger(__name__)

class ReportingService:

    @staticmethod
    def send_report(context, template_name):
        try:
            html_message = render_to_string(template_name, context)

            email  = EmailMessage(
                subject = 'Customer request',
                body = html_message,
                from_email = settings.EMAIL_HOST_USER.strip(),
                to = [ settings.EMAIL_RECIPIENT.strip() ] ,
            )

            email.content_subtype = "html"

            email.send(fail_silently=False)
            logger.info(f"Email from '{context['user']}' sent successfully.")

            return True
        except Exception as e:
            traceback.print_exc()
            print(f"Error sending mail: {e}")
            return False
