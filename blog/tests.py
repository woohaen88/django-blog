from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

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
        # 1.1. 포스트 목록 페이지를 가져온다.
        response = self.client.get("/blog/")
        # 1.2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3. 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertEqual(soup.title.text, "Blog")
        # 1.4. 내비게이션 바가 있다.
        self.navbar_test(soup)

        # 2.1. 메인 영역에 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2. '아직 게시물이 없습니다'라는 문구가 보인다.
        main_area = soup.find("div", id="main-area")
        self.assertIn("아직 게시물이 없습니다", main_area.text)

        # 3.1. 게시물이 2개 있다면
        post_001 = Post.objects.create(title="1", content="1")
        post_002 = Post.objects.create(title="2", content="2")
        self.assertEqual(Post.objects.count(), 2)

        # 3.2. 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get("/blog/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertEqual(response.status_code, 200)
        # 3.3. 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find("div", id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4. '아직 게시물이 없습니다.'라는 문구는 더 이상 보이지 않는다.
        self.assertNotIn("아직 게시물이 없습니다", main_area.text)

    def test_post_detail(self):
        # 1.1. 포스트가 하나 있다.
        post_001 = Post.objects.create(title="1", content="1")
        # 1.2. 포스트의 url은 '/blog/1/'이다.
        self.assertEqual(post_001.get_absolute_url(), "/blog/1/")

        # 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫번째 포스트의 url로 접근하면 정상적으로 작동한다(status code: 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, "html.parser")

        # 2.2. 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        self.navbar_test(soup)

        # 2.3. 첫번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(post_001.title, soup.title.text)

        # 2.4. 첫번재 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find("div", id="main-area")
        post_area = main_area.find("div", id="post-area")
        self.assertIn(post_001.title, post_area.text)

        # 2.5. 첫번째 포스트의 작성자가 포스트 영역에 있다.(미구현)

        # 2.6. 첫 번재 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)
