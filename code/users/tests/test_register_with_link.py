from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from tests.base_django import BaseDjangoTest
from users.models import User


class RegisterWithLinkTest(BaseDjangoTest):
    def setUp(self):
        super(RegisterWithLinkTest, self).setUp()
        self.getURL(reverse('wallet:charge'))

    def charge(self):
        self.form = self.driver.find_element_by_css_selector("form[name='charge_form']")
        self.email = self.form.find_element_by_name('email')
        self.amount = self.form.find_element_by_name('amount')
        self.submit_button = self.form.find_element_by_name('submit')
        self.email.send_keys('test@test.com')
        self.amount.send_keys('100')
        self.submitForm(refill=False, element='email')
        self.form = self.driver.find_element_by_css_selector("form[name='charge_confirm_form']")
        self.submit_button = self.form.find_element_by_name('confirm_button')
        self.submitForm(refill=False, element='confirm_button')
        link = User.objects.filter(email="test@test.com")[0].link
        self.getURL(reverse('users:register_with_link', args=(link, )))

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='profile_form']")
        self.name = self.form.find_element_by_name('name')
        self.password = self.form.find_element_by_name('password1')
        self.password_confirmation = self.form.find_element_by_name('password2')
        self.submit_button = self.form.find_element_by_name('submit')

        self.name.send_keys('test')
        self.password.send_keys('password')
        self.password_confirmation.send_keys('password')

    def submitForm(self, refill=True, element='name'):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name(element)
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        if refill:
            self.findAndFillForm()

    def test_form_inputs(self):
        self.charge()
        self.findAndFillForm()

    def test_ok_register(self):
        self.charge()
        self.findAndFillForm()
        self.submitForm(refill=False)
        self.driver.find_element_by_class_name("success")

    def test_empty_name(self):
        self.charge()
        self.findAndFillForm()
        self.name.clear()
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.name, 'error'))

    def test_different_password_confirmation(self):
        self.charge()
        self.findAndFillForm()
        self.password_confirmation.clear()
        self.password_confirmation.send_keys("password:D")
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.password_confirmation, 'error'))
