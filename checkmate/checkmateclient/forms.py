from django import forms

COLOR_CHOICES = (   ( 'White', 'White' ),
                    ( 'Black', 'Black' ),
)

DIFFICULTY_CHOICES = (   ( 'easy', 'easy' ),
                         ( 'hard', 'hard' ),
)
MODE_CHOICES = (   ( 'single', 'single' ),
                   ( 'multi', 'multi' ),
)

BOOKMODE_CHOICES = ( ( 'worst', 'worst'  ),
                     ( 'best','best'),
                     ('random','random')
)


class startForm(forms.Form):
    color = forms.ChoiceField(choices=COLOR_CHOICES, initial='White')
    mode = forms.ChoiceField(choices=MODE_CHOICES, initial='single')
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, initial='hard')
    book = forms.FileField()


class connectForm(forms.Form):
    gameid = forms.IntegerField(min_value=1, max_value=1000000)
    color = forms.ChoiceField(choices=COLOR_CHOICES, initial='White')

class hiddenForm(forms.Form):
    gameid = forms.IntegerField(widget=forms.HiddenInput())
    color = forms.ChoiceField(choices=COLOR_CHOICES,widget=forms.HiddenInput())

class playForm(forms.Form):
    moves = forms.CharField(widget=forms.HiddenInput())

class depthForm(forms.Form):
    depth = forms.IntegerField(min_value=1, max_value=10)

class modeForm(forms.Form):
    mode = forms.ChoiceField(choices=MODE_CHOICES)

class bookmodeForm(forms.Form):
    bookmode = forms.ChoiceField( choices=BOOKMODE_CHOICES )
