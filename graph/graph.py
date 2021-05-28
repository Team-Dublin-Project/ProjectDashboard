from django.http import request
import pandas as pd
from django.conf import settings

class Graph(object):
    def __init__(self, request):
        """
        Initialize the graph
        """
        self.session = request.session
        graph = self.session.get(settings.GRAPH_SESSION_ID)
        if not graph:
            graph = self.session[settings.GRAPH_SESSION_ID] = {}
        self.graph = graph
    
    def set_session(self, file, type, x_values, y_values):
        """
        Clean the dataframe so the graph can be generrated in the view.

        Read the dataframe and check if any of the selected columns have any NaN values.
        """
        self.graph['type'] = type
        self.graph['x_values'] = x_values
        self.graph['y_values'] = y_values
        self.save()

    def save(self):
        # mark the session as 'modified' to make sure it gets saved
        self.session.modified = True

    def get_columns(file):
        df = pd.read_csv(f'media/{file.file_loc}')
        return df.columns.values

    def clear(self):
        # remove cart from session
        del self.session[settings.GRAPH_SESSION_ID]
        self.save()