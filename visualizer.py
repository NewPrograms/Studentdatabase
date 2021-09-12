import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import offline

def unload_data(data):
    titles = []
    x_values = []
    y_values = []
    for key, values in zip(data.keys(), data.values()):
        titles.append(key)
        for x, y in zip(values.keys(), values.values()):
            x_values.append(x)
            y_values.append(y)
    return 	titles, y_values, x_values

def subplot(title, data):
    data_set = unload_data(data)
    fig = make_subplots(rows=1, cols=1)
    exp_x = []
    exp_y = []
    n = -1
    for x, y in zip(data_set[2], data_set[1]):
        exp_x.append(x)
        exp_y.append(y)
        print('\nx:', x, 'y:',y)
        if len(exp_x) and len(exp_y) == 9:
            n+=1
            fig.add_trace(go.Bar(name = '{}'.format(data_set[0][n]), x = exp_x,
                                  y = exp_y), row=1, col=1)
            exp_y.clear()
            exp_x.clear()
    fig.update_layout(title_text ="Average Grades of Students According to their {}".format(title))
    fig.show() 
# 	TITLES, X_VALUES, Y_VALUES = UNLOAD_DATA(DATA)
#	
# dict_of_fig = dict({
    # "data": [{"type": "%".format(type),
            #   "x": x_values],
            #   "y": y_values,
    # "layout": {"title": {"text": title}}
# })

# fig = go.Figure(dict_of_fig)

# fig.show()

    