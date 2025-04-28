from django.db import models

# Models for the Learning Logs app.

class Topic(models.Model):
    """A topic that the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Print the text stored in the class."""
        return self.text


class Entry(models.Model):
    """Specific details about a topic."""
    # Cascade deletion to prevent unlinked data.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadata for entries."""
        verbose_name_plural = "entries"

    def __str__(self):
        """Return a shortened version of the entry."""
        if len(str(self.text)) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text