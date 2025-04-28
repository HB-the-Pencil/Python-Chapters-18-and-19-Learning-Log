"""Define the URLs for the Learning Logs app."""

from django.urls import path

from . import views

app_name = "learning_logs"
urlpatterns = [
    # The website home page.
    path("", views.index, name="index"),
    # Topics page.
    path("topics/", views.topics, name="topics"),
    # Page for an individual topic.
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    # Page to add a topic.
    path("new_topic/", views.new_topic, name="new_topic"),
    # Page to add an entry.
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),
    # Page to edit an entry.
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
]