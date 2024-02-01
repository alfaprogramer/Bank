from django import forms

class formedu(forms.Form):
   
    forfield = forms.CharField(label="For which field of study")
    colsch= forms.CharField(label="College or School Name")
    income= forms.CharField(label="Family annual income")
    duration = forms.CharField(label="Duration of Study",help_text=" eg: 5years ")
     # Add a radio button field
    study_type_choices = [
        ('5 ', '5'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
    ]
    study_type = forms.ChoiceField(
        label="Loan Tenure",
        choices=study_type_choices,
        widget=forms.RadioSelect,
    )


class formhome(forms.Form):
     occu = forms.CharField(label="Occupation")
     anuincome = forms.CharField(label="Annual Income")
      # Add a radio button field
     study_type_choices = [
        ('5 ', '5'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
    ]
     study_type = forms.ChoiceField(
        label="Loan Tenure",
        choices=study_type_choices,
        widget=forms.RadioSelect,
    )
     




 