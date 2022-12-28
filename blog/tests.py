from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Tag
from django.contrib.auth import get_user_model

User = get_user_model()


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_one = User.objects.create_user(
            username="one",
            password="test123!@#",
        )
        self.user_two = User.objects.create_user(
            username="two",
            password="test123!@#",
        )

        self.category_programming = Category.objects.create(
            name="programming", slug="programming"
        )
        self.category_music = Category.objects.create(name="music", slug="music")

        self.tag_python_kor = Tag.objects.create(name="파이썬 공부", slug="파이썬-공부")
        self.tag_python = Tag.objects.create(name="python", slug="python")
        self.tag_hello = Tag.objects.create(name="hello", slug="hello")

        self.post_001 = Post.objects.create(
            title="first",
            content="1",
            category=self.category_programming,
            author=self.user_one,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title="second",
            content="2",
            category=self.category_music,
            author=self.user_two,
        )

        self.post_003 = Post.objects.create(
            title="third", content="3", author=self.user_one
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")
        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find("div", id="main-area")

        self.assertIn(self.category_programming.name, main_area.text)

        # 메인 영역에서 선택한 카테고리의 이름인 "programming"이 있는지 확인하고, 이 카테고리에 해당하는 포스트만 노출되어 있는지 확인
        # 그렇지 않은 post_002, post_003의 타이틀은 메인 영역에 존재하면 안됨
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def category_card_test(self, soup):
        categories_card = soup.find("div", id="categories-card")
        self.assertIn("Categories", categories_card.text)
        self.assertIn(
            f"{self.category_programming.name} ({self.category_programming.post_set.count()})",
            categories_card.text,
        )
        self.assertIn(
            f"{self.category_music.name} ({self.category_music.post_set.count()})",
            categories_card.text,
        )
        self.assertIn(f"미분류 (1)", categories_card.text)

    def navbar_test(self, soup):
        navbar = soup.nav
        # 1.5. Blog, About Me라는 문구가 내비게이션 바에 있다.
        self.assertIn("Home", navbar.text)
        self.assertIn("Blog", navbar.text)
        self.assertIn("About Me", navbar.text)
        self.assertIn("Contact", navbar.text)

        # test_button
        test_button_link = {
            "woohaen Blog": "/",
            "Home": "/",
            "About Me": "/about_me/",
            # "Contact": "/",
            "Blog": "/blog/",
        }
        # Logo
        for (key, value) in test_button_link.items():
            btn = navbar.find("a", text=key)
            self.assertEqual(btn.attrs["href"], value)
        # logo_btn = navbar.find("a", text="woohaen Blog")
        # self.assertEqual(logo_btn.attrs["href"], "/")

    def test_post_list(self):
        # 수정 setUp()함수에서 포스트를 3개 만든 상태로 시작하므로 포스트가 있는 경우와 없는 경우 나누어서 진행
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, "html.parser")

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find("div", id="main-area")
        self.assertNotIn("아직 게시물이 없습니다.", main_area.text)

        post_001_card = main_area.find("div", id="post-1")
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)

        post_002_card = main_area.find("div", id="post-2")
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)

        post_003_card = main_area.find("div", id="post-3")
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn("미분류", post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)

        self.assertIn(self.user_one.username.upper(), main_area.text)
        self.assertIn(self.user_two.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get("/blog/")
        soup = BeautifulSoup(response.content, "html.parser")
        main_area = soup.find("div", id="main-area")
        self.assertIn("아직 게시물이 없습니다.", main_area.text)

    def test_post_detail(self):
        # post_000 = Post.objects.create(
        #     title="1",
        #     content="1",
        #     author=self.user_one,
        # )

        self.assertEqual(self.post_001.get_absolute_url(), "/blog/1/")

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, "html.parser")

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find("div", id="main-area")
        post_area = soup.find("div", id="post-area")
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.user_one.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)
