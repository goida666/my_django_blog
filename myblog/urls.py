from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import MainView, PostDetailView, SignInView, SignUpView, sign_out, FeedBackView, SuccessView, SearchResultsView, \
    TagView

urlpatterns = [
    path('', MainView.as_view(), name='index'),                 
    # обьявляем путь url адреса (тут дефолтный), обьявлем класс MainView и превращаем его в функцию чтобы он мог возвращать представление и имя index чтобы ссылаться на него в других частях кода
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    # обьявляем путь url адреса (тут дефолтный + blog + url отдельного поста), делаем с PostDetailViews тоже что и выше и даем имя post_detail чтобы ссылаться на него в других частях кода
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', sign_out, name='signout'),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('contact/success/', SuccessView.as_view(), name='success'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('tag/<slug:slug>/', TagView.as_view(), name="tag"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    # определяет маршрут для обслуживания файлов медиа (например, изображений, видео, аудио),
    # static это функция Django, которая используется для определения маршрутов обслуживания статических файлов (например, CSS, JavaScript, изображения) и медиа файлов.
    # settings.MEDIA_URL - прописывается в файле settings.py показывает в какой папке лежат стат. файлы (img, css, js)
    # document_root=settings.MEDIA_ROOT - прописывается в файле settings.py и показывает папку где лежат медиа файлы