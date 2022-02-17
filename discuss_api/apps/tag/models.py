from django.db import models as m


class Tag(m.Model):
    name = m.CharField(max_length=50)

    def __str__(self):
        return self.name
