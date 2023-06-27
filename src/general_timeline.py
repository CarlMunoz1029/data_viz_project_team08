import pandas as pd
from datetime import timedelta
import plotly.express as px


def get_general_timeline(df_tl, start_date='2022-12-22', end_date='2023-01-18'):

    # start and end dates of the viz
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # create centered tickvals and text
    x_ticks_pos = pd.date_range(start_date + timedelta(hours=12), end_date + timedelta(days=1, hours=12), freq="24H")
    x_tick_text = pd.date_range(start_date, end_date + timedelta(days=1), freq="24H")

    idx_fom = 28 - int(end_date.strftime("%d"))
    x_tick_text_form = [x_tick_text[i].strftime("%d </br></br> %b %Y") if i in [0,idx_fom] else x_tick_text[i].strftime("%d") for i in range(len(x_tick_text))]

    fig = px.timeline(df_tl, x_start="DAY",
                      x_end='DAY',
                      y="PATIENT_ID",
                      range_x=[start_date, end_date+timedelta(days=1)])

    fig1 = px.timeline(df_tl.loc[df_tl['HAS_PAIN_MENTION'] != 0],
                       x_start="DAY",
                       x_end='END_RANGE_PAIN',
                       y="PATIENT_ID",
                       color_discrete_sequence=["cornflowerblue"],
                       range_x=[start_date, end_date+timedelta(days=1)],
                       hover_data=['PAIN_TIME', 'PAIN_SOURCE', 'HAS_PAIN_MENTION'])

    fig.add_trace(fig1.data[0])

    fig2 = px.timeline(df_tl.loc[df_tl['FALL_COUNT'] != 0],
                       x_start="DAY",
                       x_end='END_RANGE_FALL',
                       y="PATIENT_ID",
                       color_discrete_sequence=["sandybrown"],
                       range_x=[start_date, end_date+timedelta(days=1)],
                       hover_data=['FALL_TIME', 'FALL_SOURCE', 'FALL_COUNT'])

    fig.add_trace(fig2.data[0])

    fig3 = px.timeline(df_tl.loc[df_tl['HOSPITALIZATION_COUNT'] != 0],
                       x_start="DAY",
                       x_end='END_RANGE_HOSP',
                       y="PATIENT_ID",
                       color_discrete_sequence=["darkred"],
                       range_x=[start_date, end_date+timedelta(days=1)],
                       hover_data=['HOSPITALIZATION_TIME', 'HOSPITALIZATION_SOURCE', 'HOSPITALIZATION_COUNT'])

    fig.add_trace(fig3.data[0])

    fig.update_layout(title_text='Hospitalization, Fall and Pain mention',
                      title_x=0.5, title=dict(font=dict(size=20)),
                      autosize=False,
                      width=600,
                      height=600)

    fig.data[0].showlegend = False
    fig.data[1].showlegend = True
    fig.data[2].showlegend = True
    fig.data[3].showlegend = True

    fig.data[1].name = 'Pain'
    fig.data[2].name = 'Fall'
    fig.data[3].name = 'Hospitalization'

    fig.update_xaxes(tickangle=0,
                     tickvals=x_ticks_pos,
                     ticktext=x_tick_text_form,
                     dtick="D1",
                     tickfont=dict(size=12))

    #fig.update_yaxes(title = " ", visible=False, showticklabels=False)

    fig.update_yaxes(title=" ", titlefont=dict(size=5), showticklabels=False)

    fig.update_layout(plot_bgcolor='whitesmoke',
                      legend=dict(title="Event type:",
                                  font_family="roboto",
                                  font_size=15,),
                      hoverlabel=dict(bgcolor="white",
                                      font_size=16,
                                      font_family="roboto"),
                      width=700)

    fig.update_layout(margin=dict(l=0, r=10, b=0, t=40),
                      legend=dict(orientation="h",
                                  entrywidth=30,
                                  entrywidthmode='fraction',
                                  yanchor="top",
                                  y=-0.1,
                                  xanchor="right",
                                  x=1))

    fig.update_traces(hovertemplate="<b>%{y}</b><br><br>" +
                                     "<b>%{x|%d %b %Y}, %{customdata[0]}</b><br>" +
                                     "%{customdata[2]} Pain mention <br>" +
                                     "Source: %{customdata[1]}" +
                                     "<extra></extra>",
                      selector=({'name': 'Pain'}))

    fig.update_traces(hovertemplate="<b>%{y}</b><br><br>" +
                                     "<b>%{x|%d %b %Y}, %{customdata[0]}</b><br>" +
                                     "%{customdata[2]} Fall <br>" +
                                     "Source: %{customdata[1]}" +
                                     "<extra></extra>",
                      selector=({'name': 'Fall'}))

    fig.update_traces(hovertemplate="<b>%{y}</b><br><br>" +
                                     "<b>%{x|%d %b %Y}, %{customdata[0]}</b><br>" +
                                     "%{customdata[2]} Hospitalization <br>" +
                                     "Source: %{customdata[1]}" +
                                     "<extra></extra>",
                      selector=({'name': 'Hospitalization'}))

    return fig
