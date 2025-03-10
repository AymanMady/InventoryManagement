from django import forms
from accounts.models import Materiel,Employee,Etablissement,Emplacement,Affectation

# Materiel
class materielForm(forms.ModelForm):
    class Meta:
        model= Materiel
        fields = "__all__"



# Employees

class DateInput(forms.DateInput):
    input_type = 'date'


class employeForm(forms.ModelForm):
    date_naiss = forms.DateField(widget=DateInput)

    class Meta:
        widgets = {'my_date_field' : DateInput()}
        model= Employee
        fields = "__all__"

# Etablissement
class etablissementForm(forms.ModelForm):
    class Meta:
        model= Etablissement
        fields = "__all__"

class emplacementForm(forms.ModelForm):
    class Meta:
        model= Emplacement
        fields = "__all__"

class affectationForm(forms.ModelForm):
    class Meta:
        model= Affectation
        fields = "__all__"
