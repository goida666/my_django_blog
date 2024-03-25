from django.db import models                          # models нужен чтобы преобразовывать данные в таблицу базы данных
from django.contrib.auth.models import User           # user для авторизации и регистрации 
from taggit.managers import TaggableManager
from django.utils import timezone


class Post(models.Model):                           # создаем класс Post в котором описываем свойства данных поста
    # везде где ниже написан models - модуль который содержит базовые классы для определения моделей данных
    h1 = models.CharField(max_length=200)                        # название (Строковое поле для хранения коротких или длинных строк)
    title = models.CharField(max_length=200)                           # заголовок с макс длиной 200 символов
    url = models.SlugField()                                      # url адрес который добавляется к основному url когда переходишь на страницу отдельного поста
    description = models.TextField()                               # описание - текстовое поле
    content = models.TextField()               # контент, сама статья
    image = models.ImageField()                                         # картинка вначале (для отображения нужно pip install pillow)
    created_at = models.DateTimeField(auto_now_add=True)               # указывает, что это поле будет хранить дату и время. Параметр auto_now_add=True означает, что при создании новой записи в базе данных, поле created_at будет автоматически заполнено текущим временем (временем создания записи)
    author = models.ForeignKey(User, on_delete=models.CASCADE)            # внешний ключ который связывает с моделью User
    # on_delete=models.CASCADE - при удалении модели User которая связана с полем author все его записи будут удалены каскадно
    tag = TaggableManager()                                  # хранит целочисленное значение, null=True - можно оставить пустым 


    def __str__(self):        # определяет метод __str__ для модели данных
        return self.title      # возвращает значение поля title объекта (хз что это)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text
