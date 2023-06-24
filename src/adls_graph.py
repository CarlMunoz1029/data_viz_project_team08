import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Pre processing
def get_patient_graph(patient_name):
    df = pd.read_csv('./assets/timeline_dataset.csv')

    df['DAY'] = pd.to_datetime(df['DAY'])

    df['UNCOMPLETED_ADLS'] = df['TOTAL_ADLS'] - df['TOTAL_COMPLETED_ADLS']

    #patient_name = 'Céline Dion'

    df = df.loc[df['PATIENT_ID'] == patient_name]

    df_hosp = df[df['HOSPITALIZATION_COUNT'] != 0]

    df_fall = df[df['FALL_COUNT'] != 0]

    df_count = df.melt(id_vars=['DAY'], value_vars=['FALL_COUNT', 'HOSPITALIZATION_COUNT'], value_name='Count', var_name='Event')

    df_count = df_count[df_count['Count'] != 0]

    # Create subplots

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights = [500, 150]
    )

    # Add bar count traces

    fig.add_trace(
        go.Bar(name='COMPLETED ADLS', x=df['DAY'], y=df['TOTAL_COMPLETED_ADLS'], marker_color='rgb(51, 102, 255)'),
        row=1, col=1)

    fig.add_trace(
        go.Bar(name='UNCOMPLETED ADLS', x=df['DAY'], y=df['UNCOMPLETED_ADLS'], marker_color='rgb(179, 198, 255)'), 
        row=1, col=1)

    # Add bar percentage traces

    fig.add_trace(
        go.Bar(name='COMPLETED ADLS', x=df['DAY'], y=df['ADL_COMPLETION_PERCENTAGE'], marker_color='rgb(51, 102, 255)', visible=False),
        row=1, col=1)

    fig.update_xaxes(dtick='D1',
                    tickformat = '%d\n%b %y',
                    showgrid=True)



    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Count",
                        method="update",
                        args=[{"visible": [True, True, False, True]}]),
                    dict(label="Percentage",
                        method="update",
                        args=[{"visible": [False, False, True, True]}]),
                ]),
                direction = 'down',
                showactive = True,
                x = 1,
                xanchor = 'right',
                y = 1.1,
                yanchor = 'top'
            )
        ])


    fig.update_layout(
        barmode='stack', 
        title=dict(text=f'ADLS of {patient_name}',
                font=dict(size=16), 
                x = 0.1,
                xanchor = 'left')
    )

    # Add scatter traces

    event_trace = go.Scatter(
        name = 'Event', x=df_count['DAY'], y=df_count['Event'], 
        mode='markers',
        hoveron = 'points',
        text=df_count['Count'],
        legendrank=3,
        marker=dict(line_width=0,
                    opacity=1,
                    size=df_count['Count'].astype(float),
                    sizeref=0.5,
                    sizemode='diameter', 
                    sizemin=4,
                    symbol=['square', 'cross'],
                    color=['rgb(236, 161, 101)', 'rgb(126,1,0,255)']
            ),
        hovertemplate='%{text}<extra></extra>'
    )

    fig.add_trace(event_trace, row=2, col=1)

    fig.update_yaxes(visible=True, row=2, col=1)

    fig.update_layout(legend=dict(itemsizing='constant'))


    return fig