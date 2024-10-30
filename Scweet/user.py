from Scweet.utils import init_driver, log_in

from . import utils
from time import sleep
import random
import json


def get_user_information(users, driver=None, headless=True):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)

    users_info = {}

    for i, user in enumerate(users):

        log_user_page(user, driver)

        if user is not None:

            try:
                following = driver.find_element_by_xpath(
                    '//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath(
                    '//a[contains(@href,"/followers")]/span[1]/span[1]').text
            except Exception as e:
                # print(e)
                return

            try:
                element = driver.find_element_by_xpath('//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                website = element.get_attribute("href")
            except Exception as e:
                # print(e)
                website = ""

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                # print(e)
                desc = ""
            a = 0
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                birthday = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                location = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
            except Exception as e:
                # print(e)
                try:
                    join_date = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    span1 = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                    if hasNumbers(span1):
                        birthday = span1
                        location = ""
                    else:
                        location = span1
                        birthday = ""
                except Exception as e:
                    # print(e)
                    try:
                        join_date = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        birthday = ""
                        location = ""
                    except Exception as e:
                        # print(e)
                        join_date = ""
                        birthday = ""
                        location = ""
            print("--------------- " + user + " information : ---------------")
            print("Following : ", following)
            print("Followers : ", followers)
            print("Location : ", location)
            print("Join date : ", join_date)
            print("Birth date : ", birthday)
            print("Description : ", desc)
            print("Website : ", website)
            users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            if i == len(users) - 1:
                driver.close()
                return users_info
        else:
            print("You must specify the user")
            continue


def log_user_page(user, driver, headless=True):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_two_level_follower_following(users, env, headless=True, wait=2):
    driver = init_driver(headless=headless, env=env, firefox=True)
    sleep(wait)
    log_in(driver, env, wait=wait)
    sleep(wait)
    file_follower_following_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers_following.json'
    file_follower_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_follower_path, 'r') as f:
        user_followers = json.load(f)

    with open(file_follower_following_path, 'r') as f:
        two_level_follower_old = json.load(f)

    for user, followers in user_followers.items():
        for follower in followers:
            if follower in two_level_follower_old[user]:
                print(follower+"'s following exist,skip")
                continue
            following = utils.get_users_follow(driver, [follower], headless, env, "following", verbose=1,
                                               wait=wait)
            print(follower + "'s following:" + str(following))
            two_level_follower_old[user][follower] = following.get(follower)
            with open(file_follower_following_path, 'w') as f:
                json.dump(two_level_follower_old, f)
                f.close()


def get_users_followers(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    driver = init_driver(headless=headless, env=env, firefox=True)
    sleep(wait)
    log_in(driver, env, wait=wait)
    sleep(wait)
    followers = utils.get_users_follow(driver, users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(followers, f)
        print(f"file saved in {file_path}")
    return followers


def get_users_following(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    driver = init_driver(headless=headless, env=env, firefox=True)
    sleep(wait)
    log_in(driver, env, wait=wait)
    sleep(wait)
    following = utils.get_users_follow(driver, users, headless, env, "following", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    with open(file_path, 'w') as f:
        json.dump(following, f)
        print(f"file saved in {file_path}")
    return following


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
