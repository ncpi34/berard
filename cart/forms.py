from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(label='',
    #                                   choices=PRODUCT_QUANTITY_CHOICES,
    #                                   coerce=int)
    quantity = forms.IntegerField(label='',
                                  min_value=0,
                                  widget=forms.NumberInput(
                                      attrs={'style': ''
                                                      'max-width:50%;'
                                                      'min-width:30%;'
                                                      'max-height:60%',
                                             'placeholder': '0'}))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
