# vps_manager_django_api

***ДАННЫЙ ПРОЕКТ ЯВЛЯЕТСЯ ПРАКТИКОЙ, ЧТОБЫ НЕ РАСТЕРЯТЬ УЖЕ ИМЕЮЩИЕСЯ ЗНАНИЯ И ПОПРОБОВАТЬ ЧТО-ТО НОВОЕ***<br />
Данный проект представляет собой сервис по управлению виртуальными серверами (VPS). Проект написан на DRF, для документирования API используется OpenApi 3,
для авторизации выбрана авторизация по JWT токену.
<br />Что такое VPS:
VDS (Virtual Dedicated Server) или VPS (Virtual Private Server) — это хостинг-услуга, где пользователю предоставляется виртуальный сервер 
с максимальными привилегиями. VDS или VPS эмулирует работу реального физического сервера — есть root-доступ, возможна установка своих операционных
систем и программного обеспечения. На одном физическом сервере обычно работает несколько независимых виртуальных серверов.
В проекте (на данный момент) имеется 4 модели: Vps, Users, Profile, Applications.<br />
***VPS***<br />
        
```python
class Vps(models.Model):
    STATUSES = [
        ("started", "started"),
        ("blocked", "blocked"),
        ("stopped", "stopped"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpu = models.IntegerField() # Кол-во ядер сервера
    ram = models.IntegerField() # Кол-во оперативноя памяти сервера (в гигабайтах)
    hdd = models.IntegerField() # Объем жесткого диска сервера (в гигабайтах)
    status = models.CharField(choices=STATUSES, default="started", max_length=7) # Статус сервера (Возможные статусы указаны в STATUSES)
    maintained_by = models.ManyToManyField(User) # Список юзеров, которые занимаются администрированием сервера
    deployed_applications = models.ManyToManyField(Application) # Список приложений (программ), развернутых на сервере
```
        
<br />***USERS***<br />
        
```python
class User(AbstractBaseUser):
    email = models.EmailField(unique=True) # электронная почта пользователя, используется для авторизации в системе
    created_at = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    objects = UserMnanager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'user'
        ordering = ['id']
```
        
<br />***PROFILE***<br />
        
```python
class Profile(models.Model):
    last_name = models.CharField(max_length=64, blank=True, null=False) # Фамилия пользователя
    first_name = models.CharField(max_length=64, blank=True, null=False) # Имя пользователя
    middle_name = models.CharField(max_length=64, blank=True) # Отчество пользователя
    phone = models.CharField(max_length=64, blank=True) # Телефонный номер пользователя
    birth_date = models.DateField(null=True, blank=True) # Дата рождения пользователя

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True) # Юзер, которому принадлежит данный профиль

    class Meta:
        db_table = 'profile'
        ordering = ['last_name']
        indexes = [
            models.Index(fields=['first_name']),
            models.Index(fields=['middle_name']),
            models.Index(fields=['last_name']),
        ]

    @staticmethod
    def check_phone_len(phone): # Метод для проверки длинны введенного телефонного номера
        """Phone len must be greater or equal than 5 digits and less or equal than 19.
         If it is not, returns False"""
        if phone.isdigit():
            return 5 <= len(phone) <= 19
        return 5 <= len(phone[1:]) <= 19

    @classmethod
    def normalize_phone(cls, phone): # Метод, приводящий телефонные номера под стандарт РФ
        characters_to_remove = ['-', ' ', '.', '*', '(', ')', '/']
        for character in characters_to_remove:
            phone = phone.replace(character, '')
        if not cls.check_phone_len(phone):
            msg = 'Phone number must be between 5 and 19 characters!'
            raise ValidationError(msg)

        if phone.startswith('8') and len(phone) == 11 and phone.isdigit():
            return '+7' + phone[1:]
        elif phone.startswith('+7') and len(phone) == 12 and phone[1:].isdigit():
            return phone
        elif phone.startswith('+') and phone[1:].isdigit():
            return phone
        elif phone.isdigit():
            return '+' + phone
        else:
            msg = 'The phone number must contain only numbers and start with a plus sign!'
            raise ValidationError(msg)
```
        
<br />***APPLICATIONS***<br />
        
```python
class Application(models.Model):
    title = models.CharField(max_length=64) # Название прилодения
    deployer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # Пользователь, который развернул приложение на сервере
    size = models.FloatField() # Сколько место занимает приложение на жестком диске сервера (в мегабайтах)
    deployed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'
        ordering = ['title']
```
        
