from githubUserInfo import username, password
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


class Instagram:
    def __init__(self, username, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages':'en, en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.username = username
        self.password = password


    def signIn(self):
        self.browser.get("https://www.instagram.com/?hl=tr")
        time.sleep(2)

        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(self.username)
        passwordinput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
        passwordinput.send_keys(self.password)
        passwordinput.send_keys(Keys.ENTER)
        time.sleep(4)

    def getFollowers(self, max):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)

        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followerCount = len(dialog.find_elements_by_css_selector("li"))

        print(f"first count: {followerCount}")

        action = webdriver.ActionChains(self.browser)

        while followerCount < max:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)

            newCount = len(dialog.find_elements_by_css_selector("li"))

            if followerCount != newCount:
                #followerCount = newCount
                print(f"second count: {newCount}")
                time.sleep(1)
            else:
                break

        followers = dialog.find_elements_by_css_selector("li")

        followerList = []
        i = 0
        for user in followers:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            followerList.append(link)
            i += 1
            if i == max:
                break

        with open("followers.txt", "w", encoding="UTF-8") as file:
            for item in followerList:
                file.write(item + "\n")

    def followUser(self, username):
        self.browser.get("http://www.instagram.com/"+username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name("button")

        if followButton.text != "Message":
            followButton.click()
            time.sleep(2)
        else:
            print("Already followed.")

    def unfollowUser(self, username):
        self.browser.get("http://www.instagram.com/"+username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name("button")

        if followButton.text == "Message":
            self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div/span").click()
            confirmButton = self.browser.find_element_by_xpath('//button[text()= "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following.")


insta = Instagram(username, password)
insta.signIn()
insta.getFollowers(50)
insta.followUser("egeuni")
insta.unfollowUser("egeuni")

