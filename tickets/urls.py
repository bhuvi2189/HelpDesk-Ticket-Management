from django.urls import path
from . import views


urlpatterns = [

    path(
        "create/",
        views.create_ticket,
        name="create_ticket"
    ),

    path(
        "my-tickets/",
        views.my_tickets,
        name="my_tickets"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "update-status/<int:ticket_id>/",
        views.update_ticket_status,
        name="update_ticket_status"
    ),

    path(
        "detail/<int:ticket_id>/",
        views.ticket_detail,
        name="ticket_detail"
    ),

    path(
        "add-comment/<int:ticket_id>/",
        views.add_comment,
        name="add_comment"
    ),

    path(
        "assign-ticket/<int:ticket_id>/",
        views.assign_ticket,
        name="assign_ticket"
    ),

    # Employee Dashboard
    path(
        "employee-dashboard/",
        views.employee_dashboard,
        name="employee_dashboard"
    ),

    # Employee Status Update
    path(
        "employee-update-status/<int:ticket_id>/",
        views.employee_update_status,
        name="employee_update_status"
    ),
]