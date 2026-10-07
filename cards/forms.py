from django import forms
from .models import Student


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "name", "class_name", "roll", "designation",
            "blood_group", "address", "phone", "email", "profile_picture"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "পূর্ণ নাম"}),
            "class_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "ক্লাস / ব্যাচ"}),
            "roll": forms.TextInput(attrs={"class": "form-control", "placeholder": "রোল নম্বর"}),
            "designation": forms.TextInput(attrs={"class": "form-control", "placeholder": "পদবি"}),
            "blood_group": forms.Select(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "ঠিকানা"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "০১XXXXXXXXX"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@example.com"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }
        labels = {
            "name": "নাম *",
            "class_name": "ক্লাস",
            "roll": "রোল",
            "designation": "পদবি",
            "blood_group": "ব্লাড গ্রুপ",
            "address": "ঠিকানা",
            "phone": "ফোন",
            "email": "ইমেইল",
            "profile_picture": "প্রোফাইল পিকচার",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
