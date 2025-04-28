from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """Render the home page for the Learning Logs website."""
    return render(request, "learning_logs/index.html")


def topics(request):
    """Show all the topics for the Learning Logs website."""
    topic_list = Topic.objects.order_by("date_added")
    context = {"topics": topic_list}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """Show a topic and all of its entries."""
    topic_chosen = Topic.objects.get(id=topic_id)
    entries = topic_chosen.entry_set.order_by("-date_added")
    context = {"topic": topic_chosen, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


def new_topic(request):
    """Add a new topic to the list."""
    if request.method != "POST":
        # If there isn't data, create a new topic.
        form = TopicForm()
    else:
        # Process the data submitted.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topics")

    # Display the form if it is blank or invalid.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def new_entry(request, topic_id):
    """Add a new entry to a topic."""
    chosen_topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # If there isn't data, create a new topic.
        form = EntryForm()
    else:
        # Process the data submitted.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.topic = chosen_topic
            entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    # Display the form if it is blank or invalid.
    context = {"topic": chosen_topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    chosen_topic = entry.topic

    if request.method != "POST":
        # Fill the form with the current entry by default.
        form = EntryForm(instance=entry)
    else:
        # Process the data submitted.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=chosen_topic.id)

    context = {"entry": entry, "topic": chosen_topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)