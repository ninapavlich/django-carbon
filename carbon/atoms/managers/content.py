from django.db import models



class PublishableQueryset(models.query.QuerySet):

    DRAFT = 10
    REVIEW = 20
    PUBLISHED = 100
    UNPUBLISHED = 40

    def published(self):
        return self.filter(publication_status = PublishableQueryset.PUBLISHED)

    def drafts(self):
        return self.filter(publication_status__lte = PublishableQueryset.PUBLISHED)

    def unpublished(self):
        return self.filter(publication_status = PublishableQueryset.UNPUBLISHED)


class PublishableManager(models.Manager):
    def get_queryset(self):
        return PublishableQueryset(self.model, using=self._db)

    def published(self):
        # WARNING: Just because something is set to be published doesn't mean
        # it should be published -- an item could be expired or have some
        # other limitation
        return self.get_queryset().published()

    def drafts(self):
        return self.get_queryset().drafts()
    
    def unpublished(self):
        return self.get_queryset().unpublished()

