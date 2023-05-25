from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

# Category
from .models import Category, Tag

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_staff = User.objects.create_user(username='staff', password='somepassword')
        self.user_normal = User.objects.create_user(username='normal', password='somepassword')
        self.user_staff.is_staff = True
        self.user_staff.save()

        # Category
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')


        # Post 게시물 생성
        self.post_001 = Post.objects.create(
            title='첫 번째 포스입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_normal,
        )

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_staff,
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content = 'category가 없어요.',
            author=self.user_staff,
        )

    def test_create_post(self):
        # 로그인하지 않으면 status code가 200이면 안 된다.
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # 일반 사용자가 로그인을 한다
        self.client.login(username='normal', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff 사용자가 로그인을 한다
        self.client.login(username='staff', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn("Create New Post", main_area.text)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Post Form 만들기',
                'content': "Post Form 페이지를 만듭시다.",
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, "staff")

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # 로그인을 하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_normal)
        self.client.login(username=self.user_normal.username, password='somepassword')
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403) # 접근 권한 없음

        # 작성자(staff)가 접근하는 경우
        self.client.login(username=self.user_staff.username, password='somepassword')
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn("Edit Post", main_area.text)

        response = self.client.post(
            update_post_url,
            {
                'title': '세 번째 포스트를 수정했습니다.',
                'content': '안녕 세계? 우리는 하나!',
                'category': self.category_music.pk,
            },
            follow=True
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn("세 번째 포스트를 수정했습니다.", main_area.text)
        self.assertIn("안녕 세계? 우리는 하나!", main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
