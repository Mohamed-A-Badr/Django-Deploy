from django import forms
from passlib.context import CryptContext
from .models import Chair, Patient

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ChairAdminForm(forms.ModelForm):
    class Meta:
        model = Chair
        fields = ["parcode", "password", "available"]

    def save(self, commit=True):
        chair = super().save(commit=False)
        chair.password = pwd_context.hash(self.cleaned_data["password"])

        if commit:
            chair.save()
        return chair


class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"

    def save(self, commit=True):
        patient = super().save(commit=False)
        chair = patient.chair

        if chair:
            chair.available = False
            chair.save()

        if commit:
            patient.save()

        return patient
