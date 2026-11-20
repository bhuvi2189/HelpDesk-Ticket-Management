
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Ticket, TicketComment


# Create New Ticket
@login_required
def create_ticket(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")

        Ticket.objects.create(
            title=title,
            description=description,
            priority=priority,
            status="Open",
            user=request.user
        )
        return redirect("my_tickets")

    return render(request, "tickets/create_ticket.html")


# User My Tickets
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "tickets/my_tickets.html", {"tickets": tickets})


# Admin Dashboard
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("dashboard")

    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status="Open").count()
    in_progress_tickets = Ticket.objects.filter(status="In Progress").count()
    resolved_tickets = Ticket.objects.filter(status="Resolved").count()

    tickets = Ticket.objects.all().order_by("-created_at")

    search_query = request.GET.get("search", "").strip()

    if search_query:
        tickets = tickets.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(user__username__icontains=search_query)
        )

    selected_status = request.GET.get("status", "")
    if selected_status:
        tickets = tickets.filter(status=selected_status)

    selected_priority = request.GET.get("priority", "")
    if selected_priority:
        tickets = tickets.filter(priority=selected_priority)

    employees = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).order_by("username")

    context = {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets,
        "tickets": tickets,
        "search_query": search_query,
        "selected_status": selected_status,
        "selected_priority": selected_priority,
        "employees": employees,
    }

    return render(request, "tickets/admin_dashboard.html", context)


# Update Ticket Status - Admin
@login_required
def update_ticket_status(request, ticket_id):
    if not request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=ticket_id)
        new_status = request.POST.get("status")

        if new_status in ["Open", "In Progress", "Resolved"]:
            ticket.status = new_status
            ticket.save()

    return redirect("admin_dashboard")


# Ticket Details
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if (
        not request.user.is_staff
        and ticket.user != request.user
        and ticket.assigned_to != request.user
    ):
        return redirect("dashboard")

    comments = ticket.comments.select_related("user").order_by("created_at")

    return render(request, "tickets/ticket_detail.html", {
        "ticket": ticket,
        "comments": comments
    })


# Add Comment / Reply
@login_required
def add_comment(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if (
            not request.user.is_staff
            and ticket.user != request.user
            and ticket.assigned_to != request.user
        ):
            return redirect("dashboard")

        message = request.POST.get("message", "").strip()

        if message:
            TicketComment.objects.create(
                ticket=ticket,
                user=request.user,
                message=message
            )

    return redirect("ticket_detail", ticket_id=ticket_id)


# Assign Ticket To Employee
@login_required
def assign_ticket(request, ticket_id):
    if not request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=ticket_id)
        employee_id = request.POST.get("employee")

        employee = get_object_or_404(
            User,
            id=employee_id,
            is_staff=False,
            is_superuser=False
        )

        ticket.assigned_to = employee
        ticket.save()

    return redirect("admin_dashboard")


# Employee Dashboard
@login_required
def employee_dashboard(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")

    tickets = Ticket.objects.filter(
        assigned_to=request.user
    ).order_by("-created_at")

    context = {
        "tickets": tickets,
        "total_tickets": tickets.count(),
        "open_tickets": tickets.filter(status="Open").count(),
        "in_progress_tickets": tickets.filter(status="In Progress").count(),
        "resolved_tickets": tickets.filter(status="Resolved").count(),
    }

    return render(request, "tickets/employee_dashboard.html", context)


# Employee Update Ticket Status
@login_required
def employee_update_status(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(
            Ticket,
            id=ticket_id,
            assigned_to=request.user
        )

        new_status = request.POST.get("status")

        if new_status in ["Open", "In Progress", "Resolved"]:
            ticket.status = new_status
            ticket.save()

    return redirect("employee_dashboard")

# User Profile
@login_required
def profile(request):
    return render(request, "accounts/profile.html", {
        "user": request.user
    })