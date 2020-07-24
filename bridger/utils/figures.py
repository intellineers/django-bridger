import plotly.graph_objects as go
import pandas as pd

def get_hovertemplate_timeserie(is_pourcent=False, currency="$"):
    if is_pourcent:
        return f"""
        <b>%{{y:.2f}}%</b>
        """
    else:
        return f"""
        <b>{currency}%{{y:.2f}}{"%" if is_pourcent else ""}</b>
        """


def get_default_timeserie_figure(fig=None, add_rangeslider=True, is_legend_horizontal=True):
    if not fig:
        fig=go.Figure()
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        # paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        xaxis=dict(
            linewidth=0.5,
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            type="date",
            # showspikes=True,
            # spikethickness=1,
            zeroline=True,
            showline=True,  
            linecolor='grey',
            ticks="outside",
            tickwidth=1,
            tickcolor='black',
            ticklen=10,
            tickangle=45, 
            tickformatstops = [
                go.layout.xaxis.Tickformatstop(
                    dtickrange=[86400000, 604800000],
                    value="%e %b %y"
                ),
                go.layout.xaxis.Tickformatstop(
                    dtickrange=[604800000, "M1"],
                    value="%e %b %y"
                ),
                go.layout.xaxis.Tickformatstop(
                    dtickrange=["M1", "M12"],
                    value="%b %y"
                ),
                go.layout.xaxis.Tickformatstop(
                    dtickrange=["M12", None],
                    value="%Y"
                )
            ],
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label='1m',
                        step='month',
                        stepmode='backward'),
                    dict(count=6,
                        label='6m',
                        step='month',
                        stepmode='backward'),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(step='all')
                ]),
            ),
        ),
        autosize=True,
        hovermode="x unified",
        
    )
    if add_rangeslider:
        fig.update_layout(
            xaxis_rangeslider_visible=True
        )
    if is_legend_horizontal:
        fig.update_layout(
            legend_orientation="h"
        )
    return fig

def get_timeseries_chart(x_data, y_data, red, green, blue):
    fig = go.Figure([
        go.Scatter(
            x=x_data, y=y_data, fill='tozeroy',
            line=dict(color=f"rgb({red}, {green}, {blue})", width=1),
            fillcolor=f"rgba({red}, {green}, {blue}, 0.1)"
        )
    ])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            title="",
            titlefont=dict(
                color="#000000"
            ),
            tickfont=dict(
                color="#000000"
            ),
            anchor="x",
            side="right",
            showline=True,
            linewidth=1,
            linecolor='black',
        ),
        yaxis_type="log",
        xaxis=dict(
            title="",
            titlefont=dict(
                color="#000000"
            ),
            tickfont=dict(
                color="#000000"
            ),
            showline=True,
            linewidth=0.5,
            linecolor='black',
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        autosize=True,
        xaxis_rangeslider_visible=True,
    )


    return fig

def get_factsheet_timeseries_chart(df, color="rgb(120,214,255)", fillcolor="rgba(120,214,255, 0.5)", log_scale=True):
    df = df.sort_index()
    df.index = pd.to_datetime(df.index)
    trace = go.Scatter(x=df.index, y=df.iloc[:,0],fill="tonexty", line=dict(color=color, width=1))
    fig = go.Figure()
    fig.add_trace(trace)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
           showgrid=True, 
            zeroline=True,
            gridwidth=1, 
            showline=True,  
            gridcolor='grey', 
            linewidth=1, 
            linecolor='grey', 
            ticks="outside", 
            tickwidth=1,
            tickcolor='black', 
            ticklen=10,
            tickangle=45, 
            tickformatstops = [
                go.layout.xaxis.Tickformatstop(
                    dtickrange=[86400000, 604800000],
                    value="%e %b %y"
                ),
                go.layout.xaxis.Tickformatstop(
                    dtickrange=[604800000, "M1"],
                    value="%e %b %y"
                ),
                go.layout.xaxis.Tickformatstop(
                    dtickrange=["M1", "M12"],
                    value="%b %y"
                ),
                go.layout.xaxis.Tickformatstop(
                    dtickrange=["M12", None],
                    value="%Y"
                )
            ],
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label='1m',
                        step='month',
                        stepmode='backward'),
                    dict(count=6,
                        label='6m',
                        step='month',
                        stepmode='backward'),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(step='all')
                ]),
                x=0,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ), 
            rangeslider=dict(
                visible = True
            ),
            type='date',
            title="",
            titlefont=dict(
                color="#000000"
            ),
            tickfont=dict(
                color="#000000"
            )
        ),
        yaxis=dict(
            title="",
            titlefont=dict(
                color="#000000"
            ),
            tickfont=dict(
                color="#000000"
            ),
            anchor="x",
            side="right",
            autorange= True,
            fixedrange= False,
            showgrid=False, 
            zeroline=False,
        ),
    )
    if log_scale:
        fig.update_layout(yaxis=dict(type="log"))
    return fig

def get_horizontal_barplot(df, x_label="weighting", y_label="aggregated_title", colors=["#B4DAFF"], colors_label=None):
    
    df = df.dropna(how="any")
    if len(df.shape) == 1:
        df = df.sort_values(ascending = True)
        df = df.reset_index()
        df.columns = [y_label, x_label]


    if isinstance(x_label, list):
        data=[]
        df = df.sort_values(by=[x_label[0]], ascending=False)
        if colors_label:
            colors = df[colors_label]
        opacity = 1
        for i, label in enumerate(x_label):
            data.append(go.Bar(name=label, x=df.loc[:, label], y=df.loc[:, y_label],opacity=opacity, orientation='h', marker=dict(color=colors)))
            opacity -= 1/(len(x_label)+1)
        
        fig = go.Figure(data=data)
        fig.update_layout(barmode='group', yaxis_autorange='reversed')
    else:
        widths = [0.6] * df.shape[0]
        df = df.sort_values(by=[x_label])
        x = df[x_label]
        y = df[y_label]
        fig = go.Figure(go.Bar(
                x=x,
                y=y,
                name=x_label,
                orientation='h',
                width=widths,
                marker=dict(
                    color=colors[0])
            )
        )

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            tickformat = ".1%"
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
        ),
        margin=dict(b=0,r=20,l=20, t=0, pad=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # autosize=False,

        font=dict(
            family="roboto",
            size=12,
            color="black"
        )
    )
    height = df.shape[0]*40
    if height != 0:
        fig.update_layout(
            height= height
        )
    
    return fig

def get_piechart(df, x_label="weighting", y_label="aggregated_title", hoverinfo="label+text", max_number_label=3, height=280, with_legend=True, default_normalize=True, colors_map=None, colors_label=None):
    df = df.sort_values(by=[x_label], ascending=False)
    values = df[x_label]
    label = df[y_label]
    if default_normalize:
        values = df.loc[(df[x_label]>0), x_label]
        label = df.loc[(df[x_label]>0), y_label]

    text = values.map('{:,.1%}'.format)
    fig = go.Figure(data=[go.Pie(direction="clockwise", labels=label, values=values.abs(), text=text)])
    fig.update_traces(hoverinfo=hoverinfo, textinfo='none', textfont_size=8)
    if colors_map:
        fig.update_traces(marker=dict(colors=colors_map))
    elif colors_label:
        fig.update_traces(marker=dict(colors=df[colors_label]))
    fig.update_layout(
        margin=go.layout.Margin(b=0, l=0, r=0, t=0, pad=0),
        # showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    if with_legend:
        fig.update_layout(
            height=height,
            legend=go.layout.Legend(
                x=0,
                y=-1,
                yanchor="bottom",
                xanchor="left",
                bgcolor="rgba(0,0,0,0)",
                font=dict(
                    family="roboto",
                    size=11,
                    color="black"
                )
            )
        )
    else:
        fig.update_layout(
            showlegend=False
        ) 
    return fig
