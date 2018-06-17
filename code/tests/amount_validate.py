def AmountValidate(field_name):
    Class = type('{}ValidateClass'.format(field_name), (), {})

    def test_empty_amount(self):
        self.findAndFillForm()
        getattr(self, field_name).clear()
        self.submitForm()
        self.findForm()
        self.assertTrue(self.checkHasClass(getattr(self, field_name), "error"))
    setattr(Class, 'test_empty_{}'.format(field_name), test_empty_amount)

    def test_nan_amount(self):
        self.findAndFillForm()
        getattr(self, field_name).send_keys('A')
        self.submitForm()
        self.findForm()
        self.assertTrue(self.checkHasClass(getattr(self, field_name), "error"))
    setattr(Class, 'test_nan_{}'.format(field_name), test_nan_amount)

    def test_negative_amount(self):
        self.findAndFillForm()
        getattr(self, field_name).clear()
        getattr(self, field_name).send_keys('-123')
        self.submitForm()
        self.findForm()
        self.assertTrue(self.checkHasClass(getattr(self, field_name), "error"))
    setattr(Class, 'test_negative_{}'.format(field_name), test_negative_amount)


    return Class
