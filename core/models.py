from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


CATEGORY_CHOICES = (
    ('S', 'SHIRT'),
    ('SW', 'SPORTS WEAR'),
    ('LW', 'LEISURE WEAR'),
    ('OW', 'OUTDOOR WEAR'),
    ('GW', 'GENERAL WEAR')
)

LABEL_COLOUR_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
    ('SU', 'success')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    discounted_price = models.FloatField(blank=True, null=True)
    price = models.FloatField()
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_COLOUR_CHOICES, max_length=2)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     object_pk = self.objects.filter(self.objects.pk).latest()
    #     self.slug = slugify(self.title)+slugify(object_pk.pk)  # set the slug explicitly
    #     super(Item, self).save(*args, **kwargs)

    def get_add_to_cart_url(self):
        return reverse("core:add_product", kwargs={"slug": self.slug})

    # def unique_slug_gen(cls):
    #     cls.slug = slugify(cls.title)
    #     while cls.objects.filter(slug=cls.slug).exists():
    #         object_pk = cls.objects.latest('pk')
    #         object_pk = object_pk.pk + 1
    #         cls.slug = f'{cls.slug}-{object_pk}
    #         return cls.slug


class OrderedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f"Item: {self.item.title}, qty: {self.qty}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedItem)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username