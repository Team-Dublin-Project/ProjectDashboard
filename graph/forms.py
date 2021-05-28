from django import forms
from .graph import Graph
from .models import Graph as modelGraph

GRAPH_TYPE_CHOICES = (
    ('line', 'Line Chart'),
    ('bar', 'Bar Chart'),
    ('pie', 'Pie Chart'),
    ('doughnut', 'Doughnut Chart'),
    ('polarArea', 'Polar Area'),
    ('bubble', 'Bubble Chart'),
    ('scatter', 'Scatter Chart'),
)

class GraphTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        file = kwargs.pop('file', None)
        super(GraphTypeForm, self).__init__(*args, **kwargs)
        self.fields['x_values'].choices = [(i, str(i)) for i in Graph.get_columns(file)]
        self.fields['y_values'].choices = [(i, str(i)) for i in Graph.get_columns(file)]
        self.fields['type'].label = "Type of graph"
        self.fields['x_values'].label = "Values to set for X-axis"
        self.fields['y_values'].label = "Labels to set for Y-axis"
    
    type = forms.TypedChoiceField(choices = GRAPH_TYPE_CHOICES)
    x_values = forms.TypedChoiceField()
    y_values = forms.TypedChoiceField()

class SaveGraphForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'wrap':'hard',
            'class': 'form-control pt-3',
            'placeholder': 'Title',
            'style':'resize:none; box-shadow: 0px 2px 3px 0px rgba(0,0,0,0.2);',
        }
    ))

    description = forms.CharField(max_length = 100, required=False, widget=forms.Textarea(
        attrs={
            'rows':'5', 'cols':'10', 'wrap':'hard',
            'class': 'post-form  form-control pt-3',
            'placeholder': 'Write a description...',
            'style':'resize:none; box-shadow: 0px 2px 3px 0px rgba(0,0,0,0.2);',
        }
    ))

    class Meta:
        model = modelGraph
        fields = ['title', 'description']