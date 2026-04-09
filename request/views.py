from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import send_mail

from .models import TaskRequest
from .serializers import TaskRequestSerializer
from tasks.models import Task
from notifications.models import Notification


import threading

def _send_request_email(subject: str, message: str, recipient_email: str):
    """Utility to send task-related emails in a background thread."""
    def send():
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=True, # Prevent app crash if SMTP fails
            )
        except Exception:
            pass # Background failure should not affect user

    # Fire and forget
    thread = threading.Thread(target=send)
    thread.start()
    return True, None


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request):
    """Helper applies for a task."""
    task_id = request.data.get("task_id")
    message = (request.data.get("message") or "").strip()

    if not task_id:
        return Response({"error": "task_id is required"}, status=400)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    # Business Logic Checks
    if task.created_by == request.user:
        return Response({"error": "You cannot request your own task"}, status=400)

    if task.status != 'open':
        return Response({"error": "This task is no longer open"}, status=400)

    # Check for existing request
    if TaskRequest.objects.filter(task=task, requester=request.user).exists():
        return Response({"error": "You have already applied for this task"}, status=400)

    try:
        task_request = TaskRequest.objects.create(
            task=task,
            requester=request.user,
            message=message,
        )
    except IntegrityError:
        return Response({"error": "Duplicate request detected"}, status=400)

    # Notify the Hirer
    username = request.user.username
    Notification.objects.create(
        user=task.created_by,
        message=f'New application for "{task.title}" from {username}.',
        link='/requests'
    )

    # Send background email
    hirer_email = task.created_by.email
    if hirer_email:
        subject = f"New Application: {task.title}"
        email_body = f"Hello,\n\nYou have a new request for '{task.title}' from {username}.\nMessage: {message if message else 'N/A'}"
        _send_request_email(subject, email_body, hirer_email)

    serializer = TaskRequestSerializer(task_request)
    return Response({"message": "Request sent successfully", "request": serializer.data}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_requests(request):
    """List requests sent by the authenticated helper."""
    # select_related("task", "task__created_by") fixes N+1 for task details and hirer info
    requests = TaskRequest.objects.filter(requester=request.user).select_related("task", "task__created_by").order_by("-created_at")
    serializer = TaskRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_my_request(request, request_id):
    """Helper updates or withdraws their pending application."""
    try:
        task_request = TaskRequest.objects.get(id=request_id, requester=request.user)
    except TaskRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)

    if task_request.status != "PENDING":
        return Response({"error": "Action only allowed for pending requests"}, status=400)

    if request.method == 'DELETE':
        task_request.delete()
        return Response({"message": "Application withdrawn successfully"})

    # Update message
    message = (request.data.get("message") or "").strip()
    task_request.message = message
    task_request.save(update_fields=["message", "updated_at"])

    # Notify Hirer
    Notification.objects.create(
        user=task_request.task.created_by,
        message=f"{request.user.username} updated their application for: {task_request.task.title}",
    )

    serializer = TaskRequestSerializer(task_request)
    return Response({"message": "Application updated", "request": serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request, request_id):
    """Hirer accepts a specific helper request."""
    try:
        task_request = TaskRequest.objects.get(id=request_id, task__created_by=request.user)
    except TaskRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)

    task_request.status = "ACCEPTED"
    task_request.save()

    # Update task status
    task_request.task.status = "in_progress"
    task_request.task.save()

    # Notify and Email the Helper
    Notification.objects.create(
        user=task_request.requester,
        message=f'Your application for "{task_request.task.title}" was ACCEPTED!',
        link='/my-requests'
    )

    helper_email = task_request.requester.email
    if helper_email:
        subject = "Application Accepted!"
        email_body = f"Congratulations! Your request for '{task_request.task.title}' has been accepted."
        _send_request_email(subject, email_body, helper_email)

    return Response({"message": "Request accepted successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_request(request, request_id):
    """Hirer rejects a specific helper request."""
    try:
        task_request = TaskRequest.objects.get(id=request_id, task__created_by=request.user)
    except TaskRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)

    task_request.status = "REJECTED"
    task_request.save()

    # Notify Helper
    Notification.objects.create(
        user=task_request.requester,
        message=f"Your application for \"{task_request.task.title}\" was not accepted."
    )

    return Response({"message": "Request rejected"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def received_requests(request):
    """List all requests received by the hirer for their tasks."""
    # select_related("task", "requester") fixes N+1 for task details and helper info
    requests = TaskRequest.objects.filter(task__created_by=request.user).select_related("task", "requester").order_by("-created_at")
    serializer = TaskRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reply_to_request(request, request_id):
    """Hirer sends a reply message to a helper's application."""
    hirer_reply = (request.data.get("hirer_reply") or "").strip()

    try:
        task_request = TaskRequest.objects.get(id=request_id, task__created_by=request.user)
    except TaskRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)

    task_request.hirer_reply = hirer_reply
    task_request.save(update_fields=["hirer_reply", "updated_at"])

    # Notify Helper
    Notification.objects.create(
        user=task_request.requester,
        message=f"{request.user.username} sent a reply regarding: {task_request.task.title}",
    )

    serializer = TaskRequestSerializer(task_request)
    return Response({"message": "Reply sent successfully", "request": serializer.data})
