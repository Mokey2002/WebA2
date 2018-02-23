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


class BarcodeInfo(forms.Form):
    your_email = forms.CharField(label='your_email',max_length=100)
    your_name = forms.CharField(label='your_name', max_length=100)
    company = forms.CharField(label='company', max_length=100)
    address = forms.CharField(label='address', max_length=100)
    city = forms.CharField(label = 'city', max_length= 50)
    region = forms.CharField(label='region', max_length =50)
    postal_code = forms.CharField(label='postal-code', max_length=10)
    country = forms.CharField(label='country', max_length=20)

class Barcode_Process(forms.Form):
    
    labware = forms.CharField(label='labware', max_length = 50)
    docfile = forms.FileField()

   # def clean(self):
   #     docfile = self.cleaned_data.get('docfile')
   #     return super(Barcode_Process, self).clean()   
    

class Employee_Info(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    pss = forms.CharField(label='pss', max_length=50)

class Delete_Data(forms.Form):
    name = forms.CharField(label='name', max_length=50)
    company = forms.CharField(label='company', max_length=50)






#docfile = forms.FileField()
    
