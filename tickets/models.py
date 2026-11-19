
from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    priority = models.CharField(max_length=20)

    status = models.CharField(max_length=20)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_tickets"
)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TicketComment(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Ticket #{self.ticket.id} by {self.user.username}"

    
