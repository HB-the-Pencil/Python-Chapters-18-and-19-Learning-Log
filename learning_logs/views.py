from tabnanny import check

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404


# Create your views here.
def index(request):
    """Render the home page for the Learning Logs website."""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    """Show all the topics for the Learning Logs website."""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Show a topic and all of its entries."""
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Add a new topic to the list."""
    if request.method != "POST":
        # If there isn't data, create a new topic.
        form = TopicForm()
    else:
        # Process the data submitted.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")

    # Display the form if it is blank or invalid.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry to a topic."""
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(topic, request)

    if request.method != "POST":
        # If there isn't data, create a new topic.
        form = EntryForm()
    else:
        # Process the data submitted.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.topic = topic
            entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    # Display the form if it is blank or invalid.
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(topic, request)

    if request.method != "POST":
        # Fill the form with the current entry by default.
        form = EntryForm(instance=entry)
    else:
        # Process the data submitted.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)