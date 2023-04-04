# exec(open(r'C:\Users\Shree\Desktop\B8\B8_Django\Library\firstapp\db_shell.py').read())

from django.contrib.auth.models import User, Group, app1

# print(User.objects.all())

# User.objects.create_user(username= "suchita shelke", password= "python123", email = "sfsgmail.com")
# from django.utils.crypto import get_random_string
# print(get_random_string(5))
# exec(open(r'C:\Users\Shree\Desktop\B8\B8_Django\first_project\app1\db.shell.py').read())
data = Book.objects.raw('select * from book;')
for i in data:
    print(i)
# print(data)