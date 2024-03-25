from django.core.paginator import Paginator  # Импорт класса Paginator из модуля django.core.paginator, который используется для разбиения данных на страницы
from django.shortcuts import render,  get_object_or_404  # Импорт функции render из модуля django.shortcuts, которая используется для рендеринга шаблонов в Django
from django.views import View   
from .models import Post, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm,  CommentForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from taggit.models import Tag


class MainView(View):                                          # Объявление класса MainView, который является представлением (view) в Django и наследует функциональность от класса View
    def get(self, request, *args, **kwargs):                    # Определение метода get, который будет обрабатывать GET-запросы к данному представлению. Принимает аргументы request, *args, **kwargs
        posts = Post.objects.all().order_by('-created_at')    # менеджер обьектов, который возвращает все посты и сортировка их по полю created_at в порядке убывания
        paginator = Paginator(posts, 6)                 # Создание объекта класса Paginator, который разбивает список posts на страницы по 6 элементов на каждой

        page_number = request.GET.get('page')             # Получение номера запрошенной страницы из GET-параметра 'page'
        page_obj = paginator.get_page(page_number)                # Получение объекта страницы с номером page_number с помощью метода get_page объекта paginator

        return render(request, 'myblog/index.html', context={
            'page_obj': page_obj
        })                        # Рендеринг шаблона 'myblog/index.html' с передачей контекста, включающего переменную 'posts', содержащую все посты (не страницу) для отображения на странице


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:5]
        comment_form = CommentForm()
        return render(request, 'myblog/post_detail.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts,
            'comment_form': comment_form
        })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Post, url=slug)
            Comment.objects.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'myblog/post_detail.html', context={
            'comment_form': comment_form
        })

class SignUpView(View):                                # определяем класс SignUpView
    def get(self, request, *args, **kwargs):                  # определяем метод GET и его аргументы
            form = SignUpForm()                                         # создаем новый экземпляр (переменную)
            return render(request, 'myblog/signup.html', context={       
                'form': form           # связываем значения отсюда из HTML файла
            })                # Рендеринг шаблона 'myblog/signup.html' с передачей контекста, включающего переменную 'form', содержащую все формы

    def post(self, request, *args, **kwargs):      # определяем метод POST, и его аргументы ддя отправки на сервер
            form = SignUpForm(request.POST)    # создаем экземпляр формы, и передаем ей аргумент который говорит что это POST запрос
            if form.is_valid():              # проверка на валидацию
                user = form.save()          # сохранение нового пользователя
                if user is not None:        # проверка успешного создания (если юзер не равно не найден)
                    login(request, user)    # функция для авторизации, с аргументом request и  user (объект пользователя который успешно прошел регистрацию)
                    return HttpResponseRedirect('/')    # Если пользователь успешно зарегистрирован и авторизован, происходит перенаправление на главную страницу сайта.
                return render(request, 'myblog/signup.html', context={
                'form': form
            })    

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Неправильный пароль или указанная учётная запись не существует!")
                return render(request, "myblog/signin.html", {"form": form})
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })

def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html', context={
            'form': form,
            'title': 'Написать мне'
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f' От {name} | {subject}', message, from_email, ['aleksandrpanin@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myblog/success', context={
            'title': 'Спасибо'
        })

class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        results = ""
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })
    
class TagView(View):
    def get(self, request, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.object.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'myblog/tag.html', context={
            'title': "f#ТЕГ {tag}",
            'posts': posts,
            'common_tags': common_tags
        })


