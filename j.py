#!/usr/bin/python3
from models.user import User
from models import storage

# create a new user
new_user = User(email='john.doe@example.com', password='password123',
                first_name='John', last_name='Doe')

# add the new user to the database
storage.new(new_user)
storage.save()
