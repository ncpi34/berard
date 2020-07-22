from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(label='',
    #                                   choices=PRODUCT_QUANTITY_CHOICES,
    #                                   coerce=int)
    quantity = forms.IntegerField(label='',
                                  min_value=0,
                                  widget=forms.NumberInput(
                                      attrs={
                                          'class': 'quantity_val',
                                          'style': ''
                                                   'width:40px;'
                                          # 'max-width:50%;'
                                          # 'min-width:30%;'
                                                   'max-height:60%',
                                          'placeholder': '0'})
                                  )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput(
                                    attrs={
                                        'class': 'hidden_value'
                                    }
                                ))
    url = forms.CharField(required=False,
                          widget=forms.HiddenInput(
                              attrs={
                                  'id': 'hidden_url',
                              })
                          )


class CartCheckAllProductsForm(forms.Form):
    quantity = forms.CharField(required=False,
                               widget=forms.HiddenInput(
                                   attrs={
                                       'id': 'hidden_values',
                                   })
                               )
