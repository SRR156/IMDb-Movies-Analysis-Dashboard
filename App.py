import dash
from dash import html
from dash import dcc
import dash 
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots


###################################################################################################################

external_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css',]
app=dash.Dash(__name__,external_stylesheets=external_style)


############################################################################################

data_all=pd.read_csv('data/IMDb movies.csv')
country = pd.read_csv('data/country.csv')
moviesVsYears = pd.read_csv('data/moviesVsYears.csv')
movies = pd.read_csv('data/movies.csv')
rating = pd.read_csv('data/rating.csv')
genres=pd.read_csv('data/genres.csv')
companies = pd.read_csv('data/companies.csv')
directors = pd.read_csv('data/directors.csv')

############################################################################################

max_year=data_all['release_year'].max()
min_year=data_all['release_year'].min()

######################################################################################################################################################################################################3

header=html.Div([html.H1('IMDb Movies Analysis',
                style={'font-family':'Impact','font-size':60,'backgroundColor':'gold','color':'black','textAlign':'center',
                'marginBottom': 10,'fontWeight': 'bold', 'marginTop': 20,'marginLeft':5})],
                style={'marginBottom': 20,'backgroundColor':'gold'},className='four columns')

ban1=html.Div(id='ban1',className='two columns',style={'backgroundColor':'black'})
ban2=html.Div(id='ban2',className='two columns',style={'backgroundColor':'black'})
ban3=html.Div(id='ban3',className='two columns',style={'backgroundColor':'black'})
ban4=html.Div(id='ban4',className='two columns',style={'backgroundColor':'black'})

bans=html.Div([ban1,ban2,ban3,ban4],className='row')
head_div=html.Div([header,bans],className='row')

##################################################################################################################################################

main_slider=dcc.RangeSlider(
    id='main_slider',
    min=min_year,
    max=max_year,
    step=1,
    value=[min_year,max_year],
    marks={str(i):{'label':str(i),'style': {'color': 'white','text-orientation': '45'}} for i in range(min_year,max_year,2)},
    included=False,
    tooltip={"placement": "top", "always_visible": True}
)

second_slider=dcc.Slider(
    id='second_slider',
    min=5,
    max=10,
    step=1,
    value=7,
    marks={str(i):{'label':str(i),'style': {'color': 'white'}} for i in range(4,11)},
    included=False,
    tooltip={"placement": "top", "always_visible": True} ,
    className='six columns',
)

main_slider_title_div=html.Div(id='main_slider_title')
second_slider_title_div=html.Div(id='second_slider_title')
bar=html.Div(html.Br())

sliders_div=html.Div([main_slider_title_div,main_slider,second_slider_title_div,second_slider,bar,bar],style={'marginBottom': 30})


map_grpah = html.Div([dcc.Graph(id='map')],className='six columns')
time_graph = html.Div([dcc.Graph(id='time')],className='six columns')

top_movieprof_grpah = html.Div([dcc.Graph(id='top_Profit')],className='six columns')
top_movierate_graph = html.Div([dcc.Graph(id='top_rate')],className='six columns')

top_comp_grpah = html.Div([dcc.Graph(id='top_comp')],className='six columns')
top_genre_grpah = html.Div([dcc.Graph(id='top_genre')],className='six columns')


row_1=html.Div([map_grpah,time_graph],className='row')
row_2=html.Div([top_movieprof_grpah,top_movierate_graph],className='row')
row_3=html.Div([top_comp_grpah,top_genre_grpah],className='row')


app.layout=html.Div([head_div,sliders_div,row_1,bar,bar,row_2,bar,bar,row_3],style={'backgroundColor':'black'})
#########################################################################################################################################
#########################################################################################################################################

@app.callback(
    Output(component_id='main_slider_title',component_property='children'),
    Output(component_id='second_slider_title',component_property='children'),
    
    Input(component_id='main_slider',component_property='value'),
    Input(component_id='second_slider',component_property='value'))
def write_sliders_title(years,num):
    return html.H4("From Year {} to Year {}".format(*years),style={'color':'white','fontWeight':'bold'}),\
    html.H6("Show Top {}".format(num),style={'color':'white'})
####################################################################################################################

@app.callback(
    Output(component_id='ban1',component_property='children'),
    Output(component_id='ban2',component_property='children'),
    Output(component_id='ban3',component_property='children'),
    Output(component_id='ban4',component_property='children'),

    Input(component_id='main_slider',component_property='value')
)
def update_bans(years):
  
    movies_selected = movies[(movies['release_year'] <= years[1]) & (movies['release_year'] >= years[0])]
    top_mov_prof = movies_selected.head(1)['original_title']
    
    directors_selected = directors[(directors['release_year'] <= years[1]) & (directors['release_year'] >= years[0])].groupby('director',as_index = False)['profit'].sum().sort_values(by = 'profit', ascending = False)
    top_dir_prof = directors_selected.head(1)['director']
    
    companies_selected = companies[(companies['release_year'] <= years[1]) & (companies['release_year'] >= years[0])].groupby('production_companies',as_index = False)['profit'].sum().sort_values(by = 'profit', ascending = False)
    top_comp_prof = companies_selected.head(1)['production_companies']
   
    genres_selected = genres[(genres['release_year'] <= years[1])&(genres['release_year'] >= years[0])].groupby('genres',as_index = False)['profit'].sum().sort_values(by = 'profit', ascending = False)
    top_gen_prof = genres_selected.head(1)['genres']
    
   
    h1=html.P('Top Movie',style={'text-align':'center','color':'white','marginTop': 20})
    h2=html.H3(top_mov_prof,style={'fontWeight': 'bold','text-align':'center','color':'white'})

    h3=html.P('Top Director',style={'text-align':'center','color':'white','marginTop': 20})
    h4=html.H3(top_dir_prof,style={'fontWeight': 'bold','text-align':'center','color':'white'})
     
    h5=html.P('Top Companies',style={'text-align':'center','color':'white','marginTop': 20})
    h6=html.H3(top_comp_prof,style={'fontWeight': 'bold','text-align':'center','color':'white'})
     
    h7=html.P('Top Genres',style={'text-align':'center','color':'white','marginTop': 20})
    h8=html.H3(top_gen_prof,style={'fontWeight': 'bold','text-align':'center','color':'white'})

    return html.Div([h1,h2]),html.Div([h3,h4]),html.Div([h5,h6]),html.Div([h7,h8])
#####################################################################################################################################################

@app.callback(
    Output(component_id='map',component_property='figure'),
    
    # Input(component_id='main_slider',component_property='value'),
    Input(component_id='second_slider',component_property='value'))
def second_graph(num):
    top_country = country.head(num)
    data = [go.Bar(y=top_country['country'],x=top_country['original_title'],textfont=dict(size=14),marker_color=['white']*num, 
                orientation='h',text=top_country['country'])]
    layout = go.Layout(font={'color':'white','size':14},plot_bgcolor='#181818',paper_bgcolor='#181818',title='<b>Top Country </b>',
    yaxis={'visible': True, 'showticklabels': False},xaxis_title='Numer of movies',yaxis_title='Countries')
    return {'data':data,'layout':layout}


@app.callback(
    Output(component_id='time',component_property='figure'),
    
    Input(component_id='main_slider',component_property='value'))
def second_graph(years):
    yy=moviesVsYears[(moviesVsYears['release_year'] <= years[1]) & (moviesVsYears['release_year'] >= years[0])]
    data = [
        go.Scatter(x=yy['release_year'],y = yy['original_title'], name = 'Year vs Movies')]
    layout= go.Layout(yaxis={'showgrid':False},font={'color':'white'},
                        title_text="<b>Numer of movies over the years</b>",
                        title_font_size=17,
                        title_x=0.5,
                        plot_bgcolor='#181818',
                        paper_bgcolor='#181818',
                        xaxis_title="Year",
                        yaxis_title="Number of Movies"
    )
    return {'data':data,'layout':layout}



@app.callback(
    Output(component_id='top_Profit',component_property='figure'),
    
    Input(component_id='main_slider',component_property='value'),
    Input(component_id='second_slider',component_property='value'))
def second_graph(years,num):
    movies_selected = movies[(movies['release_year'] <= years[1]) & (movies['release_year'] >= years[0])]
    top_mov = movies_selected.head(num)
    
    data = [
        go.Bar(
           y=top_mov['original_title'],
           x=top_mov['profit'], orientation='h',marker_color=['white']*num,text=top_mov['original_title'],textfont=dict(size=14)
       )]

    layout = go.Layout(font={'color':'white','size':14},plot_bgcolor='#181818',paper_bgcolor='#181818',
    title='<b>Top Movies</b>',yaxis={'visible': True, 'showticklabels': False},xaxis_title='Profit $',yaxis_title='Movies')
    return {'data':data,'layout':layout}

@app.callback(
    Output(component_id='top_rate',component_property='figure'),
    
    Input(component_id='main_slider',component_property='value'),
    Input(component_id='second_slider',component_property='value'))
def second_graph(years,num):
    movies_selected = rating[(movies['release_year'] <= years[1]) & (rating['release_year'] >= years[0])]
    top_mov = movies_selected.head(num)
    
    data = [
        go.Bar(
           y=top_mov['original_title'],
           x=top_mov['avg_vote'], orientation='h',marker_color=['white']*num,text=top_mov['original_title'],textfont=dict(size=14)
       )]

    layout = go.Layout(font={'color':'white','size':14},plot_bgcolor='#181818',paper_bgcolor='#181818',
    title='<b>Top Rating</b>',yaxis={'visible': True, 'showticklabels': False},xaxis_title='Top Rate',yaxis_title='Movies')
    return {'data':data,'layout':layout}

    
@app.callback(
    Output(component_id='top_comp',component_property='figure'),
    
    Input(component_id='main_slider',component_property='value'),
    Input(component_id='second_slider',component_property='value'))
def second_graph(years,num):
    companies_selected = companies[(companies['release_year'] <= years[1]) & (companies['release_year'] >= years[0])].groupby('production_companies',as_index = False)['profit'].sum().sort_values(by = 'profit', ascending = False)
    top_comp = companies_selected.head(num)
    data = [go.Bar(y=top_comp['production_companies'],x=top_comp['profit'],textfont=dict(size=14),marker_color=['white']*num, orientation='h',text=top_comp['production_companies'])]
    layout = go.Layout(font={'color':'white','size':14},plot_bgcolor='#181818',paper_bgcolor='#181818',title='<b>Top Production Companies</b>',yaxis={'visible': True, 'showticklabels': False},xaxis_title='Profit $',yaxis_title='Companies')
    return {'data':data,'layout':layout}

@app.callback(
    Output(component_id='top_genre',component_property='figure'),
    
    Input(component_id='main_slider',component_property='value'),
    Input(component_id='second_slider',component_property='value'))
def fifth_graph(year,num):
    genres_selected = genres[(genres['release_year'] <= year[1])&(genres['release_year'] >= year[0])].groupby('genres',as_index = False)['profit'].sum().sort_values(by = 'profit', ascending = False)
    top_genres = genres_selected.head(num)
    data = [go.Bar(y=top_genres['genres'],x=top_genres['profit'], orientation='h',textfont=dict(size=14),marker_color=['white']*num,text=top_genres['genres'])]
    layout = go.Layout(font={'color':'white','size':14},plot_bgcolor='#181818',paper_bgcolor='#181818',title='<b>Top Genres</b>',yaxis={'visible': True, 'showticklabels': False},
                       xaxis_title='Profit $',yaxis_title='Genres')
    return {'data':data,'layout':layout}




if __name__ == '__main__':
    app.run_server(debug=True)
