from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "users"


class Request(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    visibility = models.BooleanField(default=True)
    status = models.PositiveSmallIntegerField()
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="user_requests"
    )
    manager = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="manager_requests"
    )

    class Meta:
        db_table = "requests"


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="messages")
    request = models.ForeignKey(
        Request, on_delete=models.RESTRICT, related_name="messages"
    )

    class Meta:
        db_table = "messages"
