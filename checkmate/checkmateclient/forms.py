# This file is part of Checkmate. 
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Copyright 2015 Ozge Lule(ozge.lule@ceng.metu.edu.tr), 
#                Esref Ozturk(esref.ozturk@ceng.metu.edu.tr)


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

ENABLEBOOK_CHOICES = ( ( 'enabled', 'enabled'  ),
                     ( 'disabled','disabled'),
)


class startForm(forms.Form):
    color = forms.ChoiceField(choices=COLOR_CHOICES, initial='White')
    mode = forms.ChoiceField(choices=MODE_CHOICES, initial='single')
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, initial='hard')


class connectForm(forms.Form):
    gameid = forms.IntegerField(min_value=1, max_value=1000000)
    color = forms.ChoiceField(choices=COLOR_CHOICES, initial='White')

class hiddenForm(forms.Form):
    gameid = forms.IntegerField(widget=forms.HiddenInput())
    color = forms.ChoiceField(choices=COLOR_CHOICES,widget=forms.HiddenInput())
    bookenabled = forms.ChoiceField(choices=ENABLEBOOK_CHOICES,widget=forms.HiddenInput())

class playForm(forms.Form):
    moves = forms.CharField(widget=forms.HiddenInput())

class depthForm(forms.Form):
    depth = forms.IntegerField(min_value=1, max_value=10)

class modeForm(forms.Form):
    mode = forms.ChoiceField(choices=MODE_CHOICES)

class bookForm(forms.Form):
    book = forms.FileField()

class enablebookForm(forms.Form):
    enablebook = forms.ChoiceField(choices=ENABLEBOOK_CHOICES)

class bookmodeForm(forms.Form):
    bookmode = forms.ChoiceField( choices=BOOKMODE_CHOICES )

class saveForm(forms.Form):
    savefile = forms.CharField()

class loadForm(forms.Form):
    loadfile = forms.CharField()

class hintForm(forms.Form):
    hint = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))



