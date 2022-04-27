import os
import sys

from django.test import TestCase

# Create your tests here.
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Login.models import User

if __name__ == '__main__':
    def change_password(request):
        # 修改密码
        user = User.objects.get(pk=1)
        user.set_password('123')
        user.save()
        return ("修改密码")
