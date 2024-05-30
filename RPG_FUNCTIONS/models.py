from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# для загрузки фото и видео
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.


#Для индификации юзера при отправке откликов
class GameUser(models.Model):
    user_link = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.user_link})'
# class GameCategory(models.Model):
#     text = models.CharField(max_length=100)

class GamePost(models.Model):
    header = models.CharField(max_length=100, unique= True)
    text = models.TextField()
    text_picture = models.TextField(blank=True)
    body = RichTextUploadingField(blank=True, config_name='default')

    #Опишем ограниченный выбор категорий
    class GameCategory(models.TextChoices):
        Cat_1 ='TANK', 'Танки'
        Cat_2 ='HEAL', 'Хилы'
        Cat_3 ='DD', 'ДД'
        Cat_4 ='TRADE', 'Торговцы'
        Cat_5 ='GUILDM', 'Гилдмастеры'
        Cat_6 ='QUESTGV', 'Квестгиверы'
        Cat_7 ='KZ', 'Кузнецы'
        Cat_8 ='LETHER', 'Кожевники'
        Cat_9 ='Alch', 'Зельевары'
        Cat_10 ='MAGIC', 'Мастера заклинаний'

    CategoryCheck = models.CharField(blank=True, choices=GameCategory.choices, max_length = 100)

    #связи MtM
    link_GameUser = models.ForeignKey(GameUser, on_delete=models.CASCADE)

    #Функция для отправки отклика на объявление
    game_message_senders = models.ManyToManyField(User, blank=True, null=True)

    #Чтобы отклики отображались в ЛК не queryset а красиво!
    def written_by(self):
        return "\n,\n".join([str(p) for p in self.game_message_senders.all()])

    # def __str__(self):
    #     return f'({self.CategoryCheck})'

class GamePost_message(models.Model):
    link_GameUser_Sender = models.ForeignKey(GameUser, on_delete=models.CASCADE)
    #Текст для отправки отклика на объявление
    text_message = models.TextField(blank=True)
    text_message_senders = models.ManyToManyField(GamePost, blank=True, null=True)



    def __str__(self):
        return f'({self.link_GameUser_Sender})'


