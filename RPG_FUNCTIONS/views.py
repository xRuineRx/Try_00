from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import GamePostForm, GamePostOtklickForm
from .models import GamePost, GameUser, GamePost_message

from django.shortcuts import get_object_or_404

# Create your views here.


class GamePostList(ListView):
    model = GamePost
    template_name ='Gameposts.html'
    context_object_name = 'GamePosts'


class GamePostDetail(DetailView):
    model = GamePost
    template_name = 'Post_Detail.html'
    context_object_name = "post"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.header = get_object_or_404(GamePost, id=self.kwargs['pk'])
        context['gameheader'] = self.header
        return context


class GamePostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = GamePostForm
    model = GamePost
    template_name = 'GamePost_Create.html'
    success_url = reverse_lazy('All_Posts')

    def test_func(self):
        obj = self.get_object()
        return obj.link_GameUser == self.request.user.gameuser

#Для создания поста
class GamePostCreate(LoginRequiredMixin, CreateView):
    model = GamePost
    form_class = GamePostForm
    template_name = 'GamePost_Create.html'
    success_url = reverse_lazy('All_Posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        GameUser.objects.get_or_create(user_link=self.request.user)
        post.link_GameUser = self.request.user.gameuser
        post.save()
        return super().form_valid(form)


#Для создания коменнтария к посту
class GamePost_messageCreate(LoginRequiredMixin, CreateView):
    model = GamePost_message
    form_class = GamePostOtklickForm
    template_name = 'GamePost_messageCreate.html'
    success_url = reverse_lazy('All_Posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        GameUser.objects.get_or_create(user_link=self.request.user)
        post.link_GameUser_Sender = self.request.user.gameuser
        post.save()
        return super().form_valid(form)

#Приватная страница пользователя с его объявлениями и  откликами на его объявления
class PrivateGameCabinateList(ListView):
    model = GamePost
    template_name ='PrivateGameCabinate.html'
    context_object_name = 'GamePosts_Private'

    def get_queryset(self):
        ask_2= list(GameUser.objects.filter(user_link=self.request.user).values_list('user_link', flat=True))[0]
        queryset = GamePost.objects.filter(link_GameUser=ask_2)
        return queryset

#Дополнительный класс для показа откликов
class PrivateGame_messageCabinateList(ListView):
    model = GamePost_message
    template_name ='PrivateGame_messageCabinate.html'
    context_object_name = 'GamePosts_messagePrivate'

    def get_queryset_otklick(self):
        ask_2= list(GameUser.objects.filter(user_link=self.request.user).values_list('user_link', flat=True))[0]

        list_1= list(GamePost.objects.filter(link_GameUser = ask_2).values_list('id', flat=True))
        author_otklick = []
        text_otklick = []
        for x in list_1:

           # Возвращает отправителя сообщения:
            a_1 = GamePost_message.objects.filter(text_message_senders__id=x)
            author_otklick += a_1
           # Возвращается текст отправителя сообщения
            t_1 = GamePost_message.objects.filter(text_message_senders__id=x).values_list('text_message', flat=True)
            text_otklick += t_1
        return f"{author_otklick} and {text_otklick}"

    # def get(self, request, *args, **kwargs):
    #     self.get_queryset_otklick()
    #     return super().get(request, *args, **kwargs)
        # print(f"{author_otklick} and {text_otklick}")

#Для того чтобы использовать условия != в фильтре, импортирую и использую from django.db.models import Q

# #Получу все объявления где текущий пользователь НЕ автор объявления.
# GamePost.objects.filter(~Q(link_GameUser = self.request.user)).values_list('header', flat=True)
#
# #Все объявления текущего пользователя
# GamePost.objects.filter(link_GameUser = self.request.user).values_list('header', flat=True)
#
# #Текущий пользователь как владелец своих объявлений
# GamePost.objects.filter(link_GameUser = self.request.user).values_list('link_GameUser', flat=True)[0]
# пример* list(GamePost.objects.filter(link_GameUser = 1).values_list('id', flat=True))

# #Все отклики НЕ принадлежащие текущему пользователю
# GamePost_message.objects.filter(~Q(link_GameUser_Sender=self.request.user)).values_list('link_GameUser_Sender',  flat=True)

# #Сообщения принадлежащие конкретному посту по id (кто написал)
# GamePost_message.objects.filter(text_message_senders__id=4)

# Цикл который позволяет вернуть всех пользователей оставивших  к каждому посту текущего пользователя
# list_1= list(GamePost.objects.filter(link_GameUser = self.request.user).values_list('id', flat=True))
# for x in list_1:
#    # Возвращает отправителя сообщения:
#     GamePost_message.objects.filter(text_message_senders__id=x)
#    # Возвращается текст отправителя сообщения
#     GamePost_message.objects.filter(text_message_senders__id=x).values_list('text_message', flat=True)

# Для теста
# list_1= list(GamePost.objects.filter(link_GameUser = 1).values_list('id', flat=True))
# for x in list_1:
#     GamePost_message.objects.filter(text_message_senders__id=x)
#     GamePost_message.objects.filter(text_message_senders__id=x).values_list('text_message', flat=True)

# Возвращает столбик gamepost_message id из связи m2m (по факту id сообщения оставленное пользователем)
#GamePost.objects.filter(gamepost_message__id=1).values_list('gamepost_message', flat=True)

# Возвращает текст сообщений по отношению к конкретному посту
#GamePost_message.objects.filter(text_message_senders__id=1).values_list('text_message', flat=True)


# Для отправки отклика
@login_required
def game_message(request, pk):
    user = request.user
    gamepost = GamePost.objects.get(id=pk)
    gamepost.game_message_senders.add(user)

    message = 'Вы успешно отправили отклик на объявление, ждите ответа от владельца объявления'
    return render(request, 'game_message.html', {'message': message})
