from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
# Create your models here.

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(publish__lte=timezone.now())



class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass
        return reverse("posts_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug != None:
        instance.title = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
