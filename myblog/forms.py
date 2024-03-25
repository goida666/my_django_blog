from django import forms
from django.contrib.auth.models import User    #  для аутентификации и авторизации пользователей в вашем приложении.
from django.contrib.auth import authenticate     # для проверки учетных данных пользователя. Она принимает имя пользователя и пароль, и если они соответствуют учетной записи пользователя, она возвращает объект этого пользователя.
from .models import Comment

class SignUpForm(forms.Form):           # класс для всей формы
    username = forms.CharField(              # определяем поле с именем пользователя (username - экземпляр, forms.CharField - класс)
        max_length=100,                # макс длина
        required=True,                        # обязаьельное для заполнения
        widget=forms.TextInput(attrs={          # виджет для текстового поля (опред. как отоброж. данные)
            'class': "form-control",        # стилизует весь элемент
            'id': "inputusername",             # присваивание id чтобы можно было привязать CSS или JS
            'type': "username",                   # 
            'placeholder': "Имя пользователя",    # текст которым заполнено поля до ввода
        }),
    )

    password = forms.CharField(      
        required = True,
        widget=forms.TextInput(attrs={
            'class': "form-control",     # стилизует весь элемент
            'id': "inputpassword",      # присваивание id чтобы можно было привязать CSS или JS
            'type': "password",         # тип того что вводится
            'placeholder': "Пароль",   # текст которым заполнено поля до ввода
            }),
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",       # стилизует весь элемент
            'id': "ReInputPassword",      # присваивание id чтобы можно было привязать CSS или JS
            'type': "password",                # тип того что вводится
            'plaseholder': "Повторите пароль",   # текст которым заполнено поля до ввода
        })
    )

    def clean(self):                                 # вызывается метод clean который сравнивает пароли в формах
        password = self.cleaned_data['password']     # cleaned_data - атрибут self, для извлечения значени введенного в переменную password
        confirm_password = self.cleaned_data['repeat_password']  # cleaned_data - атрибут self, для извлечения значени введенного в переменную repeat_password

        if password != confirm_password: 
            raise forms.Validation.Error(
                "Пароли не совпадают"       # если эти значения не совпадают то выводим надпись
            )

    def save(self):                            # определение метода save, для сохранения в базе данных и self, который ссылается на текущий экземпляр объекта формы
        user = User.objects.create_user(             # обьявляем переменную  user, модель User, для работы с менеджером модели user.objects и подключаем create_user - метод для созд. нового пользователя
            username=self.cleaned_data['username'],   # новые данные которые были проверены и очищено поле
            password=self.cleaned_data['password'],   # новые данные которые были проверены и очищено поле
        )
        user.save()                                  # сохраняет нового пользователя
        auth = authenticate(**self.cleaned_data)     # Эта строка аутентифицирует пользователя с помощью функции authenticate, которая принимает данные пользователя в качестве аргументов.
        return auth 
        # функция возвращает результат аутентификации. Если аутентификация прошла успешно, будет возвращен объект пользователя. В противном случае будет возвращено None

class SignInForm(forms.Form):
    username = forms.CharField(
        max_length = 100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
        })
    )
    password = forms.CharField(
        max_length = 100,
        required=True,
        widget=forms.PasswordInput(attrs={
        'class': "form-control mt-2",
        'id': "inputUsername",
        })
    )

class FeedBackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",       # стилизует весь элемент
            'id': "name",      # присваивание id чтобы можно было привязать CSS или JS
            'plaseholder': "Ваше имя",   # текст которым заполнено поля до ввода)
        })
    )

    email = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "email",
            'plaseholder': "Ваш email",
        })
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': "Тема"
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control md-textarea',
            'id': 'message',
            'rows': 2,
            'placeholder': "Ваше сообщение"
        })
    )

class CommentForm(forms.ModelForm):    #  Это определение класса CommentForm, который наследуется от forms.ModelForm

    class Meta:           # вложенный класс Meta, который используется для настройки класса ModelForm
        model = Comment    # указание на модель, на основе которой должна быть создана форма. В данном случае используется модель Comment
        fields = ('text', )  # кортеж полей модели, которые должны быть включены в форму. В данном случае в форму включено только поле text
        widgets = {    # словарь виджетов, которые должны быть использованы для отображения полей формы
            'text': forms.Textarea(attrs={   # указание на то, что поле text должно быть отображено как текстовая область (Textarea
                'class': 'form-control mb-3',  # добавление классов CSS к виджету. В данном случае к текстовой области добавлены классы form-control и mb-3
                'rows': 3  # указание на то, что текстовая область должна содержать 3 строки
            }),
        }