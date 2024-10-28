from django import forms
from core.models import AddressBook, ProductReview
from phone_field import PhoneField

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write a review'}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']



class AddnewAddressForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your address ..."}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "City..."}))
    state = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "State..."}))
    mobile = PhoneField(help_text='Mobile number ...')
    class Meta:
        model = AddressBook
        fields = ["address", "city", "state", "mobile",]
        exclude = ["is_default"]