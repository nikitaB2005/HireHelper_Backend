from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, Review
from .serializers import TaskSerializer, ReviewSerializer
from request.models import TaskRequest
from notifications.models import Notification


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    """Create a new task and assign the current user as owner."""
    serializer = TaskSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_feed(request):
    """Fetch all open tasks for the global feed, excluding our own."""
    tasks = Task.objects.filter(status="open").exclude(created_by=request.user)
    serializer = TaskSerializer(tasks, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    """Fetch tasks created by the authenticated user."""
    tasks = Task.objects.filter(created_by=request.user)
    serializer = TaskSerializer(tasks, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    """Update task details. Restricted to the task owner."""
    try:
        task = Task.objects.get(id=task_id, created_by=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = TaskSerializer(task, data=request.data, partial=True, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    """Delete a task. Restricted to the task owner."""
    try:
        task = Task.objects.get(id=task_id, created_by=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    task.delete()
    return Response({"message": "Task deleted successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_task(request, task_id):
    """Mark a task as completed and update all accepted requests."""
    try:
        task = Task.objects.get(id=task_id, created_by=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    if task.status == 'completed':
        return Response({"error": "Task is already completed"}, status=400)

    if task.status != 'in_progress':
        return Response({"error": "Only in-progress tasks can be marked completed"}, status=400)

    task.status = 'completed'
    task.save(update_fields=['status', 'updated_at'])

    # Update associated accepted requests to COMPLETED status
    accepted_requests = TaskRequest.objects.filter(task=task, status='ACCEPTED').select_related('requester')
    for task_request in accepted_requests:
        task_request.status = 'COMPLETED'
        task_request.save(update_fields=['status', 'updated_at'])

        Notification.objects.create(
            user=task_request.requester,
            message=f'Your accepted task "{task.title}" has been marked completed by the hirer.',
            link='/my-requests'
        )

    return Response({"message": "Task marked as completed"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_review(request, task_id):
    """Submit a review for a completed task."""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    if task.status != 'completed':
        return Response({"error": "Task must be completed to leave a review"}, status=400)

    reviewer = request.user
    if reviewer == task.created_by:
        # Hirer reviewing the Helper
        try:
            task_request = TaskRequest.objects.get(task=task, status='COMPLETED')
            reviewee = task_request.requester
        except TaskRequest.DoesNotExist:
            return Response({"error": "No completed helper found for this task"}, status=400)
    else:
        # Helper reviewing the Hirer
        try:
            task_request = TaskRequest.objects.get(task=task, status='COMPLETED', requester=reviewer)
            reviewee = task.created_by
        except TaskRequest.DoesNotExist:
            return Response({"error": "You are not authorized to review this task"}, status=403)

    if Review.objects.filter(task=task, reviewer=reviewer).exists():
        return Response({"error": "You have already reviewed this task"}, status=400)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(task=task, reviewer=reviewer, reviewee=reviewee)
        
        # Notify the review recipient
        star_rating = serializer.validated_data['rating']
        notification_msg = f"{reviewer.username} left you a {star_rating} star review for task '{task.title}'."
        Notification.objects.create(user=reviewee, message=notification_msg, link='/dashboard')
        
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request, user_id):
    """Fetch all reviews received by a specific user."""
    reviews = Review.objects.filter(reviewee_id=user_id).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)