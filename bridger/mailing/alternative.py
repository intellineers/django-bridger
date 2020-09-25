from django.core.mail import EmailMultiAlternatives

class MailingModuleEmailMultiAlternatives(EmailMultiAlternatives):
    """ This class extend the default EmailMultiAternative and override the constructor with four attributes:
        * mass_mail
        * previous_mail
        * create_mailobj
        * permission
    """
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, cc=None,
                 reply_to=None, mass_mail=None, previous_mail=None, create_mailobj=False, permission=None):
        super().__init__(
            subject, body, from_email, to, bcc, connection, attachments,
            headers, cc, reply_to
        )
        self.mass_mail = mass_mail
        self.previous_mail = previous_mail
        self.create_mailobj = create_mailobj
        self.permission = permission

    def message(self):
        msg = super().message()
        if self.mass_mail:
            msg.mass_mail = self.mass_mail
        if self.previous_mail:
            msg.previous_mail = self.previous_mail
        if self.permission:
            msg.permission = self.permission
        msg.create_mailobj = self.create_mailobj
        return msg
