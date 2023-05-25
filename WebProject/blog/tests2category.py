from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

# Category
from .models import Category

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_0001 = User.objects.create_user(username='0001', password='somepassword')
        self.user_0002 = User.objects.create_user(username='0002', password='somepassword')

        # Category
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        # Post 게시물 생성
        self.post_001 = Post.objects.create(
            title='첫 번째 포스입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_0001,
        )
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_0002,
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content = 'category가 없어요.',
            author=self.user_0002,
        )

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_post_list(self):
        # 포스트가 있는 경우(setUp에서 3개의 포스트 생성함)
        self.assertEqual(Post.objects.count(), 3)

        # 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 페이지 타이들은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')

        # Category widget test
        self.category_card_test(soup)

        # main-area를 가져온다.
        main_area = soup.find('div', id='main-area')

        # 메인 영역에 포스트 3개를 각각 카테고리 테스트
        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)

    def test_post_detail(self):

        # 포스트의 url test
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 첫 번째 포스트의 상세 페이지 테스트
        # 첫 번째 post url로 접근하면 정상적으로 작동한다.
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # category widget test
        self.category_card_test(soup)

        # 첫 번째 포스트의 제목(title)이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다.
        main_area = soup.find('div', id = 'main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        # 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.
        self.assertIn(self.user_0001.username.upper(), post_area.text)
        # 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)


    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)