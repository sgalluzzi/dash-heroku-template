import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

%%capture
gss = pd.read_csv("https://raw.githubusercontent.com/sgalluzzi/dash-heroku-template/master/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

markdown_text = '''

"I've been devalued, I've been disrespected and dismissed because I am a woman. I've been told that I don't deserve any more than less because I am a woman."
-- Megan Rapinoe, [Sports Illustrated](https://www.si.com/soccer/2021/03/24/megan-rapinoe-testifies-congress-gender-pay-gap)

Over the last few years, more and more light has been shed on the gender wage gap that exists in the United States.  Women, such as Rapinoe, have used their platforms to stand up for women's rights in the workplace.  
Sadly, even after Rapinoe spoke these words at the White House, the [National Partnership for Women and Families](https://www.nationalpartnership.org/our-work/resources/economic-justice/fair-pay/americas-women-and-the-wage-gap.pdf) still estimates women are paid 83 cents for every dollar to men.  This disparity is a by-product of
the underlying sexism and collective values that exist in America.  Fortunately, American values are malleable.  By exploring data regarding the gender wage gap and presenting the data in an informative way, I hope to 
help push this conversation forward while being an advocate for women's rights in the workplace.

The data explored is from the General Social Survey [GSS](https://gss.norc.org/), a survey conducted in the United States since 1972 that aims to study the growth and complexities of American life. This particular data set is from the 2018 survey.
The data contains variables such as years of education, income, job prestige, and sex.  Below are many plots and figures illustrating information regarding the gender wage gap.  Something I found particularly interesting was
the fact that though women are on average more educated and hold positions of higher job prestige, they still make less than their male counterparts.  Please take some time to explore the data, and become better informed about
the disparity between wages of men and women.

'''

gss_2 = gss_clean.groupby('sex').agg({'income':'mean',
                                        'job_prestige':'mean',
                                         'socioeconomic_index':'mean',
                                      'education':'mean'})
gss_2= round(gss_2, 2)


gss_2 = gss_2.rename({'income':'Avg. Income',
                                   'job_prestige':'Job Prestige Rating',
                                   'socioeconomic_index':'SES',
                                   'education':'Education (yrs)'}, axis=1)








gss_2 = gss_2.reset_index().rename({'sex':'Sex'}, axis = 1)

gss_2

t = gss_2[['Sex', 'Avg. Income', 'Job Prestige Rating', 
                            'SES', 'Education (yrs)']]


fig2 = ff.create_table(gss_2)


fig2.show()

three = gss_clean[['sex','male_breadwinner']]

crosstb = pd.crosstab(three.male_breadwinner, three.sex)

crosstb

fig3 = px.bar(crosstb,
             labels={'male_breadwinner':'Stance: It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family.', 
                        'value':'Total'})
fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))
fig3.show()

p4 = gss_clean[['job_prestige', 'income', 'sex','education','socioeconomic_index']]

p4 = p4[~p4.sex.isnull()]

p4 = p4[~p4.income.isnull()]

p4=p4[~p4.education.isnull()]

p4=p4[~p4.socioeconomic_index.isnull()]

fig4 = px.scatter(p4.head(200), x='job_prestige', y='income', color = 'sex', 
                 height=600, width=600,
                 trendline='ols',
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig4.update(layout=dict(title=dict(x=0.5)))
fig4.show()

fig5 = px.box(gss_clean, x='income', y = 'sex',
                   labels={'sex':'', 'income':'Income'})
fig5.update(layout=dict(title=dict(x=0.5)))
fig5.show()

fig5b = px.box(gss_clean, x='job_prestige', y = 'sex',
                   labels={'sex':'', 'job_prestige':'Job Prestige'})
fig5b.update(layout=dict(title=dict(x=0.5)))
fig5b.show()

sixer = gss_clean[['income','sex','job_prestige']].dropna(axis = 0)

sixer.describe()

category = pd.cut(sixer.job_prestige, bins = [16,26.6,37.2,47.8,58.4,69,80], labels = ['Little to No Prestige','Low Presitige','Some Prestige',
                                                                                       'Good Prestige','Great Prestige','Ultimate Prestige'])
sixer.insert(3, 'Prestige_Rank', category)

sixer = sixer[~sixer.Prestige_Rank.isnull()]

fig6 = px.box(sixer, x='income', y = 'sex',
             facet_col='Prestige_Rank', facet_col_wrap=2,
                   labels={'income':'Income'})
fig6.update(layout=dict(title=dict(x=0.5)))
fig6.show()

app2 = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app2.layout = html.Div(
    [
        html.H1("Exploring the Gender Wage Gap"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Gender Wage Gap Table"),
        
        dcc.Graph(figure=fig2),
        
        html.H2("Traditional Gender Roles Support"),
        
        dcc.Graph(figure=fig3),
        
        html.H2("Income and Job Prestige of Genders Scatter Plot"),
        
        dcc.Graph(figure=fig4),
        
        html.H2("Income of Genders Box Plot"),
        
        dcc.Graph(figure=fig5),
        
        html.H2("Job Prestige of Genders Box Plot"),
        
        dcc.Graph(figure=fig5b),
        
        html.H2("Income by Job Prestige Categories of Genders Box Plots"),
        
        dcc.Graph(figure=fig6)
        
    
    ]
)

if __name__ == '__main__':
    app2.run_server(mode='inline', debug=True, port=8059)
