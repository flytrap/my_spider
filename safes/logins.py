# coding:utf8
# Author: flytrap
import time
from selenium import webdriver

from safes.exceptions import LoginException


class BaseLogin(object):
    index_url = ''

    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.username = username  # 用户名
        self.password = password  # 密码
        self.driver.get(self.index_url)  # 打开主页
        self.login()

    def login(self):
        """登录方法，继承必须有该方法"""
        raise Exception('Must login function')

    def input_user_and_pass(self):
        """填充用户名和密码"""
        self.driver.find_element_by_name('loginname').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)


class SinaLogin(BaseLogin):
    index_url = 'http://www.sina.com.cn/'

    def login(self):
        if self.check_login():
            return
        self.driver.find_element_by_link_text('登录').click()  # 点击登录

        self.input_user_and_pass()

        remember = self.driver.find_element_by_name('remember')
        if remember.is_selected():
            remember.click()  # 取消记忆
        self.driver.find_element_by_class_name('login_btn').click()  # 登录
        login_error_tips = self.driver.find_element_by_class_name('login_error_tips')
        if login_error_tips.text:
            # 有提示错误信息，表示登录失败，抛出异常
            raise LoginException(login_error_tips.text)
        time.sleep(2)
        if not self.check_login():
            self.login()

    def check_login(self):
        """检查登录状态"""
        self.driver.refresh()  # 刷新页面
        time.sleep(2)
        name = self.driver.find_element_by_id('SI_Top_Nick_Name')  # 获取用户名
        if name.text:
            print('login ok')
            return True
        return False

    def to_weibo(self):
        """打开微博窗口"""
        self.driver.find_element_by_id('SI_Top_Weibo').find_element_by_class_name('tn-tab').click()

    def switch_window(self, num=0, window=None):
        """
        切换窗口页签
        :param num: 递归调用，跳出条件，增加改值
        :param window: 目的窗口handle
        :return:
        """
        if num < len(self.driver.current_window_handle):
            if window is None:
                window = self.driver.window_handles[num]
            self.driver.switch_to.window(window)
            print('switch to: {}'.format(self.driver.title))
            return True
        return False

    def send_wb(self, text):
        """发送微博"""
        if not self.check_login():
            return
        for window in self.driver.window_handles:
            if 'weibo.com' not in self.driver.current_url:
                if self.switch_window(window=window):
                    time.sleep(2)
                    continue
                return
            break
        text_body = self.driver.find_element_by_xpath('//*[@id="v6_pl_content_publishertop"]/div/div[2]/textarea')
        text_body.clear()
        text_body.send_keys(text)

        send_bt = self.driver.find_element_by_xpath('//*[@id="v6_pl_content_publishertop"]/div/div[3]/div[1]/a')
        send_bt.click()  # 发布

    def get_weibo_list(self):
        """获取微博列表"""

    def del_weibo(self, wb_id):
        """删除微博"""

    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass
