#!/Users/alex/tassl/mailer/venv/bin/python3
"""This script is an api call to Mandrill to send an email template populated with the params identified in the 'dispatch' function """
import mandrill, config
api_key = config.API_KEY


def dispatch(template_identifier, \
    recipient_name, \
    recipient_email, \
    recipient_alma_mater, \
    sender_name='Melissa Schipke', \
    sender_email='melissa@tassl.com', \
    email_subject='Welcome to Tassl!'):
    try:
        mandrill_client = mandrill.Mandrill(api_key)
        template_content = [] 
        message = {'attachments': [],
         'auto_html': None,
         'auto_text': None,
         'bcc_address': None, 
         'from_email': sender_email,
         'from_name': sender_name,
         'global_merge_vars': [],
         #'google_analytics_campaign': 'message.from_email@example.com',
         #'google_analytics_domains': ['example.com'],
         'headers': {'Reply-To': sender_email},
         'html': None, 
         'images': [], 
         'important': False,
         'inline_css': None,
         'merge': True,
         'merge_language': 'mailchimp',
         'merge_vars': [{'rcpt': recipient_email,
                         'vars': [{'content': recipient_alma_mater, 'name': 'ALMAMATER'}]}],
         'metadata': {'website': 'www.tasslapp.com'},
         'preserve_recipients': None,
         'recipient_metadata': [{'rcpt': recipient_email,
                                 'values': {}}],
         'return_path_domain': None,
         'signing_domain': None,
         'subaccount': None, #'cust-123'
         'subject': email_subject,
         'tags': [],
         'text': None, 
         'to': [{'email': recipient_email,
                 'name': recipient_name,
                 'type': 'to'}],
         'track_clicks': None,
         'track_opens': None,
         'tracking_domain': None,
         'url_strip_qs': None,
         'view_content_link': None}
        result = mandrill_client.messages.send_template(template_name=template_identifier, template_content=template_content, message=message, async=False, ip_pool='Main Pool')#, send_at='example send_at')
        print(result)

    except mandrill.Error as e:
        # Mandrill errors are thrown as exceptions
        print('A mandrill error occurred: %s - %s' % (e.__class__, e))
        raise