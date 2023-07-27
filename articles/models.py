from uuid import uuid4

from django.db import models
from django.conf import settings


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        abstract = True


# Create your models here.
class Post(TimestampMixin):
    id = models.AutoField(primary_key=True)
    article_title = models.CharField(max_length=48, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст статьи")    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", 
                                   verbose_name="Автор",
                                   on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f"{self.article_title} (#{self.id} от {self.created_at.strftime('%d.%m.%Y')})"
    
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


def image_upload_to_default_path(instance: 'Image', filename: str):
    return f"media/posts/{instance.post.id}/{uuid4().__str__()}.{filename.split('.')[-1]}"


class Image(TimestampMixin):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=image_upload_to_default_path)

    @property
    def url(self) -> str:
        return self.file.url
    
    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Tag(TimestampMixin):
    name = models.CharField(max_length=48, unique=True)
    posts = models.ManyToManyField(Post, related_name="tags")
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Poll(TimestampMixin):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="polls")
    title = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class PollOption(TimestampMixin):
    id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.text
    
    class Meta:
        verbose_name = "Вариант ответа (опрос)"
        verbose_name_plural = "Варианты ответа (опрос)"


class UserPollAnswer(TimestampMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="poll_answers")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answer = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
        unique_together = ('user', 'poll')
