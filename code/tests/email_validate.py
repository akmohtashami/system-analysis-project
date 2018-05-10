def EmailValidate(field_name):
    Class = type('{}ValidateClass'.format(field_name), (), {})

    def test_empty_email(self):
        self.findAndFillForm()
        getattr(self, field_name).clear()
        self.submitForm()
        self.assertTrue("error" in getattr(self, field_name).get_attribute("class"))
    setattr(Class, 'test_empty_{}'.format(field_name), test_empty_email)

    def test_invalid_email_no_at_sign(self):
        self.findAndFillForm()
        getattr(self, field_name).clear()
        getattr(self, field_name).send_keys("salam")
        self.submitForm()
        self.findForm()
        self.assertTrue("error" in getattr(self, field_name).get_attribute("class"))
    setattr(Class, 'test_invalid_{}_no_at_sign'.format(field_name),
            test_invalid_email_no_at_sign)

    def test_invalid_email_no_tld(self):
        self.findAndFillForm()
        getattr(self, field_name).clear()
        getattr(self, field_name).send_keys("salam@gmail")
        self.submitForm()
        self.findForm()
        self.assertTrue("error" in getattr(self, field_name).get_attribute("class"))
    setattr(Class, 'test_invalid_{}_no_tld'.format(field_name),
            test_invalid_email_no_tld)

    def test_invalid_email_no_address(self):
        self.findAndFillForm()
        getattr(self, field_name).clear()
        getattr(self, field_name).send_keys("@gmail.com")
        self.submitForm()
        self.findForm()
        self.assertTrue("error" in getattr(self, field_name).get_attribute("class"))
    setattr(Class, 'test_invalid_{}_no_address'.format(field_name),
            test_invalid_email_no_address)

    return Class
