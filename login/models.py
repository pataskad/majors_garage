from django.db import models
from django.conf import settings
from django.contrib import messages
import re
import bcrypt



# Create your models here.
class Product(models.Model):
    name= models.CharField(max_length=100)
    category= models.CharField(max_length=15)
    price=models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserManager(models.Manager):
    def validate(self, form):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['first_name'],
            email = form['email'],
            password = pw,
        )


class User(models.Model):
    first_name = models.CharField(max_length=45, default=True)
    last_name = models.CharField(max_length=45, default=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return str(self.email)

# OrderItem, Order, and Transaction created with help from https://github.com/justdjango/Shopping_cart/blob/master/shopping_cart/models.py

class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    is_purchased = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_purchased = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    ref_code = models.CharField(max_length=10)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_purchased = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_purchased = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.order_id