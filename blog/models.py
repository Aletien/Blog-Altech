from django.db import models
from PIL import Image
from django.conf import settings
from django.template.defaultfilters import slugify

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def blog_count(self):
        return self.blogs.all().count()
    
class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def blog_count(self):
        return self.blogs.all().count()


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    publishing_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', default=1)
    tags = models.ManyToManyField(Tag, related_name='blogs')
    slider_blog = models.BooleanField(default=False)
    hit = models.PositiveIntegerField(default=0)


    def comment_count(self):
        return self.comments.all().count()

    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def blog_tags(self):
        return ", ".join([tag.title for tag in self.tags.all()])

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name