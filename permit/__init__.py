
'''
class permitform(ModelForm):
	def __init__(self, current_user, *args, **kwargs);
		super(businesspermitForm, self).queryset=self.fields['business_no'].queryset/exclude(id=current_user.id)

	class Meta:
		model=Business_permit
		exclude=['owner','businesspermit_number']

'''