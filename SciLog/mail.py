import json

from django.core.mail import EmailMessage


class MJEmailMessage(EmailMessage):
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, cc=None,
                 reply_to=None, template_id=None, variables=None):
        headers = headers or {}
        if 'X-MJ-TemplateLanguage' not in headers:
            headers['X-MJ-TemplateLanguage'] = '1'
        if 'X-Mailjet-TrackClick' not in headers:
            headers['X-Mailjet-TrackClick'] = '1'
        if 'X-Mailjet-TrackOpen' not in headers:
            headers['X-Mailjet-TrackOpen'] = '1'
        if template_id:
            headers['X-MJ-TemplateID'] = template_id
        if variables:
            headers['X-MJ-Vars'] = json.dumps(variables)
        super(MJEmailMessage, self).__init__(
            subject, body, from_email, to, bcc, connection, attachments,
            headers, cc, reply_to
        )
