def AmountValidate(field_name):
    Class = type('{}ValidateClass'.format(field_name), (), {})

    def test_empty_amount(self):
        self.findAndFillForm()
        self.amount.clear()
        self.submitForm()
        self.assertTrue("error" in self.amount.get_attribute("class"))
    setattr(Class, 'test_empty_{}'.format(field_name), test_empty_amount)

    def test_nan_amount(self):
        self.findAndFillForm()
        self.amount.send_keys('A')
        self.submitForm()
        self.assertTrue("error" in self.amount.get_attribute("class"))
    setattr(Class, 'test_nan_{}'.format(field_name), test_nan_amount)

    def test_negative_amount(self):
        self.findAndFillForm()
        self.amount.clear()
        self.amount.send_keys('-123')
        self.submitForm()
        self.assertTrue("error" in self.amount.get_attribute("class"))
    setattr(Class, 'test_negative_{}'.format(field_name), test_negative_amount)


    return Class
