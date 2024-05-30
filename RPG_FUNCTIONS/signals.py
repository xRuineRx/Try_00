# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from django.template.loader import render_to_string
#
# from RPG_GAMEDESK.RPG_FUNCTIONS.models import GamePost
#
#
# def send_notifications(preview, pk, title, sub_otklick):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body="",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=sub_otklick,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender= GamePost)
#
# def notify_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.game_message_senders.all()
#         sub_otklick_emails = []
#
#         for cat in categories:
#             sub_otklick = cat.subscribers.all()
#             sub_otklick_emails += [s.email for s in sub_otklick]
#
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)