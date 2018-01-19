from django import forms



class CheckButton(forms.Form):
   
    #your_name = forms.CharField(label='Your name', max_length=100)
    your_email = forms.CharField(label='Your email',max_length=20)
    #number = forms.CharField(label='number', max_length=10)
    docfile = forms.FileField()
   
    def clean(self):
        docfile = self.cleaned_data.get('docfile')
        if not docfile:
            raise forms.ValidationError('File required')
        if not docfile.name.endswith('.dat'):
            raise forms.ValidationError('Incorrect format')
        return super(CheckButton, self).clean()   

   
