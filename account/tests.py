from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Permission, Group, ContentType

class UserModelTest(TestCase):

    fixtures = ['data.yaml']

    def setUp(self):
        self.u1 = amod.User.objects.get(id=101)
        self.u1.set_password(self.u1.password)
        self.u1.save()
        self.u2 = amod.User.objects.get(id=102)
        self.u2.set_password(self.u2.password)
        self.u2.save()

    def test_user_create_save_load(self):
        '''Tests round trip of User model data to/from database'''
        u2 = amod.User.objects.get(email='homer@simpsons.com')
        self.assertEquals(self.u1.first_name, u2.first_name)
        self.assertEquals(self.u1.last_name, u2.last_name)
        self.assertEquals(self.u1.email, u2.email)
        self.assertEquals(self.u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))

    def test_add_permissions_check_permissions(self):
        '''Add permissions to a user and check permissions'''
        p1 = Permission.objects.get(id=101)
        p1.save()

        self.u1.user_permissions.add(p1)
        self.u1.save()

        self.assertTrue(self.u1.has_perm('auth.delete_logentry'))

    def test_add_groups_check_permissions(self):
        '''Add groups to a user and check permissions'''
        g1 = Group.objects.get(id=101)
        g1.save()
        p1 = Permission.objects.get(id=102)
        p1.save()
        g1.permissions.add(p1)
        g1.save()

        self.u1.groups.add(g1)
        self.u1.save()

        self.assertTrue(self.u1.has_perm('auth.change_logentry')) #manually added group permission
        self.assertTrue(self.u1.has_perm('auth.delete_logentry')) #default group permission from fixture
