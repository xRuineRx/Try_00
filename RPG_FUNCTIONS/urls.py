from django.urls import path
from .views import GamePostList, GamePostCreate, GamePostDetail, GamePostUpdate, PrivateGameCabinateList, game_message, \
    GamePost_messageCreate, PrivateGame_messageCabinateList

# Импортируем созданное нами представление

urlpatterns = [
    path('All_Posts', GamePostList.as_view(), name = 'All_Posts'),
    path('All_Posts/add_post', GamePostCreate.as_view()),
    path('All_Posts/otklick', GamePost_messageCreate.as_view()),
    path('All_Posts/detail/<int:pk>', GamePostDetail.as_view(), name= "Details"),
    path('All_Posts/update/<int:pk>', GamePostUpdate.as_view(), name= "Update_Details"),
    path('All_Posts/private_detail_posts/', PrivateGameCabinateList.as_view()),
    path('All_Posts/private_detail_posts_otklick/', PrivateGame_messageCabinateList.as_view()),
    path('All_Posts/detail/<int:pk>/game_message/', game_message, name='game_message'),
]

