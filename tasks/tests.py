# Import Django's TestCase class for creating unit tests
from django.test import TestCase
# Import User model for creating test users
from django.contrib.auth.models import User
# Import reverse to dynamically generate URLs from view names
from django.urls import reverse

# Import task models to test
from .models import NormalTask, ContinuousTask


class CompleteNormalTaskTestCase(TestCase):
    """
    Test case for verifying that normal tasks can be marked as complete.
    Tests the complete_task view functionality for NormalTask objects.
    """
    
    def setUp(self):
        """
        Set up test fixtures that run before each test method.
        Creates a test user and an uncompleted normal task.
        """
        # Create a test user for authentication
        self.user = User.objects.create_user(username='test', password='testpass')
        
        # Create a normal task assigned to the test user
        self.normal_task = NormalTask.objects.create(
            user=self.user,
            title='Test Normal Task',
            completed=False  # Task starts as incomplete
        )

    def test_user_completes_normal_task(self):
        """
        Test that a logged-in user can successfully complete a normal task.
        Verifies:
        1. The task's completed status changes to True
        2. The view redirects to the dashboard (302 status code)
        """
        # Log in the test user to simulate an authenticated session
        self.client.login(username='test', password='testpass')
        
        # Send POST request to complete_task view with task ID and type
        response = self.client.post(reverse('complete_task', args=[self.normal_task.id, 'normal']))
        
        # Reload the task from the database to get updated values
        self.normal_task.refresh_from_db()
        
        # Assert that the task is now marked as completed
        self.assertTrue(self.normal_task.completed)
        
        # Assert that the response redirects to dashboard (HTTP 302)
        self.assertEqual(response.status_code, 302)

    def test_user_can_not_complete_other_users_task(self):
        self.other_user = User.objects.create_user(username='other', password='otherpass')
        self.client.login(username='other', password='otherpass')
        response = self.client.post(reverse('complete_task', args=[self.normal_task.id, 'normal']))
        self.normal_task.refresh_from_db()
        self.assertFalse(self.normal_task.completed)
        self.assertEqual(response.status_code, 404)
        

class CompleteContinuousTaskTestCase(TestCase):
    """
    Test case for verifying that continuous tasks can be marked as complete.
    Tests the complete_task view functionality for ContinuousTask objects.
    """
    
    def setUp(self):
        """
        Set up test fixtures that run before each test method.
        Creates a test user and an uncompleted continuous task.
        """
        # Create a test user for authentication
        self.user = User.objects.create_user(username='test', password='testpass') 
        # Create a continuous task assigned to the test user
        self.continuous_task = ContinuousTask.objects.create(
            user=self.user,
            title='Test Continuous Task',
            work_time=5,
            completed=False  # Task starts as incomplete
        )   

    def test_user_increments_work_time(self):
        self.client.login(username='test', password='testpass')
        response = self.client.post(reverse('increment_work_time', args=[self.continuous_task.id]))
        self.continuous_task.refresh_from_db()
        self.assertEqual(self.continuous_task.work_time, 6)
        self.assertEqual(response.status_code, 302)

    def test_completed_tasks_never_appear_in_dice_roll(self):
        self.client.login(username='test', password='testpass')
        self.continuous_task.completed = True
        self.continuous_task.save()
        response = self.client.post(reverse('dice_roll'))
        session = self.client.session
        result = session.get('result', {})
        if result.get('type') == 'task':
            self.assertFalse(result.get('task_id') == self.continuous_task.id)

    def test_dice_roll_can_return_break(self):
        self.client.login(username='test', password='testpass')
        NormalTask.objects.all().update(completed=True)
        ContinuousTask.objects.all().update(completed=True)
        response = self.client.post(reverse('dice_roll'))
        session = self.client.session
        result = session.get('result', {})
        self.assertTrue(result.get('type') == 'break')