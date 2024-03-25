from django.contrib import admin     # импорт модуля admin из django.contrib, который является встроенным приложением Django для административного сайта
from .models import Post,  Comment     # импортируем модель Post из models

class PostAdmin(admin.ModelAdmin):     # создаем класс и его аргумент это базовый класс для создания интерфейса администратора для модели
    prepopulated_fields = {'url': ['title']}     # эта штука создает url (который идет в slug) по заголовку

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)     # регистрируем Post и класс PostAdmin
admin.site.register(Comment, CommentAdmin)