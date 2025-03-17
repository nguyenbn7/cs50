import time
import random
import os
from urllib.parse import urlencode
from django.test import TestCase
from django.urls import reverse
from .models import User, Post, Like

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# Create your tests here.


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="foo", email="foo@example.com", password="1234")

    def test_create_post(self):
        content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.client.login(username="foo", password="1234")
        response = self.client.post(reverse("post_new"), {"content": content})
        self.client.logout()
        post = Post.objects.filter(user=self.user).first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.content, content)
        self.assertEqual(post.user.username, self.user.username)

    def test_create_post_empty_content(self):
        self.client.login(username="foo", password="1234")
        response = self.client.post(
            reverse("post_new"), {"content": ""}, follow=True)
        self.client.logout()
        messages = response.context["messages"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(
            *messages), "Can not create post because post's content is blank or post's content is the (nearly) same with another")

    def test_like_post(self):
        content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.client.login(username="foo", password="1234")
        self.client.post(
            reverse("post_new"), {"content": content}, follow=True)
        post = Post.objects.filter(user=self.user).first()
        self.client.post(reverse("like", kwargs={"post_id": post.id}))
        self.client.logout()

        self.assertEqual(len(Like.objects.all()), 1)


class SeleniumPostTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.chrome = webdriver.Chrome(executable_path=os.environ.get(
            "chromedriver", "D:/Tools/chromedriver.exe"))
        self.user = User.objects.create_user(
            username="foo", email="foo@example.com", password="1234")
        self.home_page = self.live_server_url
        self.login_page = self.home_page + '/login'
        time.sleep(2)

    def tearDown(self):
        self.chrome.close()
        time.sleep(2)
        self.chrome.quit()

    def test_create_edit_like_post(self):
        # login to web page
        self.chrome.get(f"{self.login_page}")
        self.chrome.find_element_by_name("username").send_keys("foo")
        self.chrome.find_element_by_name("password").send_keys("1234")
        self.chrome.find_element_by_class_name("btn").click()

        time.sleep(2)

        # test create new post with non empty content
        content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.chrome.find_element_by_xpath("//a[@href='#newpost']").click()
        self.chrome.find_element_by_name("content").send_keys(content)
        self.chrome.find_element_by_class_name("btn-primary").click()
        self.assertEqual(
            self.chrome.find_element_by_tag_name("p").text, content)
        time.sleep(2)

        # test create new post with empty content
        self.chrome.find_element_by_xpath("//a[@href='#newpost']").click()
        self.chrome.find_element_by_name("content").send_keys("")
        self.chrome.find_element_by_class_name("btn-primary").click()
        error_message = self.chrome.find_element_by_class_name(
            "alert-danger").text[:-1].strip()
        exp_err_msg = "Can not create post because post's content is blank or post's content is the (nearly) same with another"
        self.assertEqual(error_message, exp_err_msg)
        time.sleep(2)

        # test edit post
        new_content = "Ut id turpis et enim sollicitudin pharetra."
        self.chrome.find_element_by_class_name("btn-link").click()
        self.chrome.find_element_by_name("content").clear()
        self.chrome.find_element_by_name("content").send_keys(new_content)
        self.chrome.find_element_by_class_name("btn-primary").click()
        self.chrome.get(f"{self.home_page}")
        self.assertEqual(self.chrome.find_element_by_tag_name(
            "p").text, new_content)
        time.sleep(2)

        # test like post
        like_btn = self.chrome.find_element_by_css_selector("a.like-btn")
        like_text = self.chrome.find_elements_by_class_name(
            "text-secondary")[1]
        like_img = self.chrome.find_element_by_css_selector("i.fa")

        # like btn is clicked then increase like text and change class of icon
        like_btn.click()
        time.sleep(1)
        self.assertEqual(like_img.get_attribute('class'), "fa fa-heart")
        self.assertEqual(like_text.text, "Likes: 1")
        time.sleep(3)

        # like btn is clicked again then reset to original
        like_btn.click()
        time.sleep(1)
        self.assertEqual(like_img.get_attribute('class'), "fa fa-heart-o")
        self.assertEqual(like_text.text, "Likes: 0")
        time.sleep(2)


posts_dump_data = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Ut id turpis et enim sollicitudin pharetra.",
    "Nam malesuada dolor quis lorem vestibulum, id laoreet nisl aliquet.",
    "Proin cursus ipsum vitae ante maximus, ut tempor libero volutpat.",
    "Maecenas a eros gravida enim dignissim blandit.",
    "Sed in purus ultrices, pharetra dui non, tempus eros.",
    "In ac tellus sed erat eleifend rutrum.",
    "Phasellus dignissim sem eget augue ullamcorper semper.",
    "Proin feugiat urna eget malesuada cursus.",
    "Vivamus tincidunt mi nec ornare tincidunt.",
    "Phasellus scelerisque velit sit amet libero interdum aliquet.",
    "In convallis urna at ultrices maximus.",
    "Donec semper nisi quis ipsum elementum, quis sodales nibh convallis.",
    "Donec blandit erat id leo faucibus facilisis.",
    "Nulla et lectus eu lorem auctor ornare sit amet ut neque.",
    "Aliquam sed sapien hendrerit, ullamcorper nulla at, finibus ipsum.",
    "Sed suscipit neque ut dui iaculis, ac egestas risus semper.",
    "Nunc quis nulla blandit, mollis quam ut, interdum velit.",
    "Nam porta nisl eu lacus convallis, vitae ullamcorper augue luctus.",
    "Maecenas maximus lacus iaculis, hendrerit enim at, porta justo.",
    "Sed euismod tellus eleifend est dignissim, vel porta quam vehicula.",
    "Suspendisse porta dui nec orci sollicitudin rhoncus.",
    "Etiam vitae purus vitae magna elementum volutpat nec a arcu.",
    "Duis eget metus eu nisl porttitor porttitor eget eu nisl.",
    "Nullam lobortis ex in vulputate laoreet.",
    "Morbi eu nibh at nibh dictum venenatis eget vel nunc.",
    "Nunc ullamcorper massa condimentum pretium vestibulum.",
    "Etiam eget erat ultricies, elementum erat finibus, ullamcorper orci.",
    "Vestibulum ut arcu accumsan, luctus ante ac, hendrerit felis.",
    "Ut nec lorem ac massa accumsan cursus non vitae erat.",
    "Curabitur sed ipsum ac nisi consectetur imperdiet sit amet nec augue.",
    "Morbi eget massa euismod, blandit urna nec, vestibulum dolor.",
    "Maecenas varius tortor luctus, pretium dui aliquet, convallis diam.",
    "Nullam viverra nisl at arcu euismod tristique.",
    "Donec ac ex at enim convallis ultrices ac quis tortor.",
    "Nunc imperdiet ligula non lorem viverra, et mattis est interdum.",
    "Nam mollis libero luctus vestibulum interdum.",
    "Sed scelerisque tellus vitae neque convallis maximus.",
    "Nulla consectetur mi eget nisl faucibus pulvinar.",
    "Etiam in nisi faucibus, ullamcorper nisi vitae, mollis nibh.",
    "Suspendisse gravida turpis id purus ornare, sit amet viverra diam gravida.",
    "Donec eget arcu ut est varius consectetur nec porta nunc.",
    "Nullam faucibus justo non ex pulvinar, sed viverra nisi consequat.",
    "Nullam consectetur mauris id imperdiet tristique.",
    "Phasellus et mi maximus, porttitor nisl ac, sagittis neque.",
    "Proin ac turpis ac lacus rhoncus commodo.",
    "Fusce non velit tristique, viverra dui eget, feugiat nisl.",
    "Duis semper libero id purus ultricies aliquet.",
    "Quisque dapibus orci sed mauris porttitor, id interdum tellus molestie.",
    "Nunc eget urna ullamcorper, consectetur arcu non, tempus sem.",
    "Curabitur efficitur leo at nisl aliquet, non vehicula neque malesuada.",
    "Integer et magna vel nulla ullamcorper hendrerit.",
    "In in orci ac sapien pulvinar scelerisque et sit amet leo.",
    "Mauris nec sem ut velit rhoncus tempus sit amet non massa.",
    "Suspendisse scelerisque est vitae justo feugiat, non efficitur risus consequat.",
    "Suspendisse consectetur nisi quis odio luctus, ac ornare libero semper.",
    "Suspendisse elementum eros at congue mattis.",
    "Aenean in orci sed leo consequat placerat.",
    "Nunc sit amet lacus condimentum, luctus nisl sed, finibus ligula.",
    "Nam in orci consequat, mattis odio nec, lacinia tellus.",
    "Aenean commodo quam ac dolor mollis, ac lobortis nisl lobortis.",
    "Vivamus ut dolor in erat convallis rutrum ac eget neque.",
    "Curabitur pretium est vitae cursus rhoncus.",
    "Proin porttitor ligula quis tellus cursus venenatis.",
    "Sed congue sem fermentum, ultricies dui a, bibendum lacus.",
    "Integer lobortis dolor vitae ligula mattis lacinia.",
    "Sed commodo velit a ex finibus, a tincidunt turpis luctus.",
    "Maecenas et ligula ornare, aliquet ligula sed, porta nibh.",
    "Sed consectetur eros et purus consectetur, ut placerat augue placerat.",
    "Suspendisse sit amet ipsum eu libero pharetra auctor.",
    "Proin porta tortor nec eros consequat placerat.",
    "Suspendisse ac augue nec mauris auctor maximus.",
    "Donec consequat lacus ac felis sagittis laoreet.",
    "Morbi venenatis nulla quis viverra sagittis.",
    "Quisque et odio sed diam faucibus auctor sit amet ut dui.",
    "Sed eu tellus elementum erat vehicula iaculis.",
    "Donec blandit nisl id facilisis efficitur.",
    "Nullam nec orci porta, blandit libero sit amet, congue lectus.",
    "In ultricies tortor sit amet enim fringilla, eu accumsan ex malesuada.",
    "Morbi aliquam purus eu arcu molestie, nec dapibus ex vulputate.",
    "Nulla ac augue viverra, semper massa in, vulputate quam.",
    "Pellentesque pulvinar mauris vitae dolor finibus, in tincidunt eros semper.",
    "Ut aliquet odio ut metus tincidunt pellentesque.",
    "Mauris pretium arcu at tellus rutrum, bibendum pharetra purus egestas.",
    "Ut vitae odio elementum, finibus tellus ac, pulvinar arcu.",
    "In elementum augue id nisi dapibus consectetur.",
    "Nunc dapibus neque sollicitudin, luctus risus a, efficitur nunc.",
    "Sed hendrerit nulla sed neque dapibus, eget tempor odio ullamcorper.",
    "Donec tempor ipsum vitae ex imperdiet convallis eget sit amet ante.",
    "Mauris quis odio et risus varius ultricies.",
    "Curabitur pretium nunc sed arcu tincidunt suscipit.",
    "Aenean eu ligula id augue euismod tincidunt vel quis neque.",
    "Cras aliquet magna et euismod sollicitudin.",
    "Donec id erat vel tellus ultrices auctor.",
    "Ut vel dui at diam accumsan vehicula.",
    "Donec semper massa ac gravida aliquet.",
    "Phasellus interdum quam et sapien vulputate, eu gravida tortor imperdiet.",
    "Sed suscipit sapien vel luctus lobortis.",
    "Duis a lectus facilisis, imperdiet quam non, maximus mi.",
    "Proin interdum arcu at magna mattis dapibus.",
    "Integer vel neque vestibulum, fringilla metus in, tristique risus.",
    "Nunc consequat lacus nec ex tincidunt aliquam.",
    "Nulla consequat lorem nec sollicitudin efficitur.",
    "Praesent in dui eget justo iaculis malesuada.",
    "Vestibulum suscipit tortor et velit pellentesque fermentum.",
    "Sed non enim eu velit tristique tempus.",
    "Pellentesque semper lectus at justo facilisis, faucibus tincidunt purus dictum.",
    "Nulla at tortor quis nibh rhoncus laoreet et at magna.",
    "Suspendisse ac urna a nisi volutpat condimentum ut vitae enim.",
    "Proin tempus nulla non venenatis imperdiet.",
    "Ut dignissim purus facilisis egestas tincidunt.",
    "Suspendisse suscipit justo non nibh egestas sodales.",
    "In viverra arcu in lorem mollis gravida.",
    "Phasellus fringilla mi nec leo condimentum aliquet.",
    "In tincidunt nibh eget elit malesuada, vel consectetur metus vulputate.",
    "Cras sed nisl venenatis felis interdum laoreet.",
    "Cras varius dolor quis augue placerat lacinia.",
    "Suspendisse eleifend enim nec leo placerat dapibus.",
    "Proin a libero et metus commodo placerat.",
    "Ut eu leo sit amet odio accumsan pulvinar.",
    "Morbi id urna suscipit, vestibulum dolor et, consectetur ipsum.",
    "Pellentesque efficitur tellus eu pretium pharetra.",
    "Suspendisse posuere nisl non mattis malesuada.",
    "Quisque tristique arcu lobortis scelerisque egestas.",
    "Duis vehicula felis ac nunc convallis, a luctus risus euismod.",
    "Morbi eleifend turpis vitae mauris posuere, ut bibendum mi commodo.",
    "Vivamus gravida sapien eleifend aliquet hendrerit.",
    "Etiam dapibus eros vitae est hendrerit, eu tincidunt orci iaculis.",
    "Fusce fringilla urna ac eleifend tincidunt.",
    "Vivamus tempus leo vitae sapien eleifend, nec laoreet tellus luctus.",
    "Praesent fringilla orci eget tellus convallis consequat ac quis mauris.",
    "Vivamus finibus ipsum id enim maximus fringilla.",
    "Integer et velit facilisis, posuere lectus efficitur, semper sapien.",
    "Sed fermentum purus ac commodo fringilla.",
    "Duis sit amet ipsum consequat, malesuada ipsum sed, ornare turpis.",
    "Sed fermentum purus sollicitudin, dapibus ante vel, tempor dolor.",
    "Nullam ullamcorper erat id hendrerit suscipit.",
    "Vestibulum eget mauris eu est vehicula facilisis.",
    "Curabitur sodales neque sed commodo malesuada.",
    "Pellentesque ac elit a ipsum pharetra maximus sit amet vel magna.",
    "Ut et dolor sit amet diam maximus malesuada.",
    "Suspendisse facilisis nisi vitae tempor varius.",
]

users_dump_data = [
    "foo",
    "bar",
    "baz",
    "cs50",
    "jdoe",
    "dumb"
]


def generate_dump_data():
    driver = webdriver.Chrome("D:/Tools/chromedriver.exe")
    home_page_url = "localhost:8000"

    init_users(driver, home_page_url)
    init_posts_user(driver, home_page_url)
    random_like_per_user(driver, home_page_url)


def init_users(driver, home_page_url):
    driver.get(home_page_url)
    register_link = reverse("register")
    for user in users_dump_data:
        driver.find_element_by_xpath(f"//a[@href='{register_link}']").click()
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user)
        email_input = driver.find_element_by_name("email")
        email_input.send_keys(f"{user}@example.com")
        password_input = driver.find_element_by_name("password")
        password_input.send_keys("1234")
        confirmation_input = driver.find_element_by_name("confirmation")
        confirmation_input.send_keys("1234")
        driver.find_element_by_class_name("btn").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            f"//a[@href='{reverse('logout')}']").click()


def init_posts_user(driver, home_page_url):
    driver.get(home_page_url)
    posts_per_user = len(posts_dump_data) // len(users_dump_data)
    start = 0
    end = posts_per_user
    for user in users_dump_data:
        driver.find_element_by_xpath(
            f"//a[@href='{reverse('login')}']").click()
        driver.find_element_by_name("username").send_keys(user)
        driver.find_element_by_name("password").send_keys("1234")
        driver.find_element_by_class_name("btn-primary").click()

        for i in range(start, end):
            driver.find_element_by_xpath("//a[@href='#newpost']").click()
            driver.find_element_by_name(
                "content").send_keys(posts_dump_data[i])
            driver.find_element_by_class_name("btn-primary").click()
        driver.find_element_by_xpath(
            f"//a[@href='{reverse('logout')}']").click()

        start += posts_per_user
        end += posts_per_user
        time.sleep(1)


def random_like_per_user(driver, home_page_url):
    driver.get(home_page_url)
    total_page = len(posts_dump_data) // 10 + \
        (1 if len(posts_dump_data) % 10 == 0 else 0)

    for user in users_dump_data:
        driver.find_element_by_xpath(
            f"//a[@href='{reverse('login')}']").click()
        driver.find_element_by_name("username").send_keys(user)
        driver.find_element_by_name("password").send_keys("1234")
        driver.find_element_by_class_name("btn-primary").click()

        driver.find_element_by_xpath("//a[@href='?page=1']").click()
        for page in range(2, total_page + 1):

            like_btns = driver.find_elements_by_class_name("like-btn")

            s = set()
            for _ in range(3):
                idx = random.randint(0, 9)
                while idx in s:
                    idx = random.randint(0, 9)
                s.add(idx)
                like_btns[idx].click()

            driver.find_element_by_xpath(f"//a[@href='?page={page}']").click()

        driver.find_element_by_xpath(
            f"//a[@href='{reverse('logout')}']").click()
        time.sleep(1)
