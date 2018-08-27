from django.shortcuts import get_object_or_404
from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from services.models import ServiceType, ServiceRequest
from tests.base_django import BaseDjangoTest
from users.models import User
from wallet.models import Currency
from django.utils import timezone


class ProcessRequestTest(BaseDjangoTest):
    def setUp(self):
        super(ProcessRequestTest, self).setUp()
        ServiceType.objects.create(
            short_name="toefl",
            name="TOEFL",
            currency=Currency.IRR,
        )
        ServiceRequest.objects.create(
            owner=get_object_or_404(User, email=self.CUSTOMER_INFO[0][0]),
            service_type=get_object_or_404(ServiceType, short_name="toefl"),
            amount=0,
            creation_date=timezone.now()
        )
        self.loginAsAgnet()
        self.getURL(reverse('services:requests_list'))

    def wait_until_list_is_gone(self):
        def link_has_gone_stale(driver):
            try:
                self.table.find_element_by_tag_name("tr")
                return False
            except StaleElementReferenceException:
                return True
        self.wait_for(link_has_gone_stale)

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='request_details_form']")

    def selectOneRequest(self):
        self.table = self.driver.find_element_by_id("list")
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found = False
        for td in first_row:
            try:
                td.find_element_by_tag_name("a").click()
                self.wait_until_list_is_gone()
                found = True
                break
            except:
                pass
        self.assertTrue(found)
        self.findForm()

    def findRequestByID(self):
        self.getURL(reverse('services:requests_list'))
        self.selectOneRequest()

    def submitForm(self, button):
        # Not using self.form.submit deliberately
        button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('request_details_form')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findForm()

    def loginWithManager(self):
        self.logout()
        self.loginAsManager()
        self.getURL(reverse('services:requests_list'))

    def test_select_one_request(self):
        self.selectOneRequest()

    def test_ok_accept_request(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.assertTrue('حال' in self.form.text)

    def test_double_accept(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        try:
            self.accept = self.driver.find_element_by_name('accept_button')
            self.assertTrue(False, 'Double accept is possible')
        except:
            pass

    def test_ok_reject_request(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.reject = self.driver.find_element_by_name('reject_button')
        self.submitForm(self.reject)
        self.assertTrue('انتظار' in self.form.text)

    def test_Free_reject(self):
        self.selectOneRequest()
        try:
            self.reject = self.driver.find_element_by_name('reject_button')
            self.assertTrue(False, 'Reject free is possible')
        except:
            pass

    def test_free_done(self):
        self.selectOneRequest()
        try:
            self.accomplish = self.driver.find_element_by_name('finish_button')
            self.assertTrue(False, 'Accomplish free is possible')
        except:
            pass

    def test_ok_accomplish_request(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('finish_button')
        self.submitForm(self.accomplish)
        self.assertTrue('شده' in self.form.text)

    def test_accomplish_accept(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('finish_button')
        self.submitForm(self.accomplish)
        try:
            self.accept = self.driver.find_element_by_name('accept_button')
            self.assertTrue(False, 'accept done is possible')
        except:
            pass

    def test_accomplish_reject(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('finish_button')
        self.submitForm(self.accomplish)
        try:
            self.reject = self.driver.find_element_by_name('reject_button')
            self.assertTrue(False, 'Reject done is possible')
        except:
            pass

    def test_double_accomplish(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('finish_button')
        self.submitForm(self.accomplish)
        try:
            self.accomplish = self.driver.find_element_by_name('finish_button')
            self.assertTrue(False, 'Accomplish done is possible')
        except:
            pass

    def test_reject_others(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.logout()
        self.loginAsAgnet(1)
        self.findRequestByID()
        try:
            self.reject = self.driver.find_element_by_name('reject_button')
            self.assertTrue(False, 'Reject others request is possible')
        except:
            pass

    def test_accomplish_others(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept_button')
        self.submitForm(self.accept)
        self.logout()
        self.loginAsAgnet(1)
        self.findRequestByID()
        try:
            self.accomplish = self.driver.find_element_by_name('finish_button')
            self.assertTrue(False, 'Accomplish others request is possible')
        except:
            pass

    def test_customer_accept_request(self):
        self.logout()
        self.loginAsCustomer()
        try:
            self.getURL(reverse('services:requests_list'))
            self.assertTrue(False, 'user can see list of requests.')
        except:
            pass
