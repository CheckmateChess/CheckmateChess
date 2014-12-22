from django import forms

COLOR_CHOICES = (   ( 'White' , 'White' ),
					( 'Black' , 'Black' ),
				)


DIFFICULTY_CHOICES = (   ( 'easy' , 'easy' ),
					( 'hard' , 'hard' ),
				)
MODE_CHOICES = (   ( 'single' , 'single' ),
					( 'multi' , 'multi' ),
				)

class startForm(forms.Form):
	color = forms.ChoiceField( choices = COLOR_CHOICES , initial = 'White' )
	mode = forms.ChoiceField( choices = MODE_CHOICES, initial = 'single' )
	difficulty = forms.ChoiceField( choices = DIFFICULTY_CHOICES, initial = 'hard' )
	book = forms.FileField()

class connectForm(forms.Form):
	gameid = forms.IntegerField( min_value=1 , max_value=1000000 ) 
	color = forms.ChoiceField( choices = COLOR_CHOICES , initial = 'White' )
