import streamlit as st
import pandas as pd
from plotly.express import histogram, bar, scatter
from wordcloud import WordCloud

st.set_page_config(page_title="Data Analyst",page_icon=":bar_chart:",layout="wide")

# QUESTION qu'on se pose
st.title('OU UN DATA ANALYSTE PEUT IL TRAVAILLER? :technologist:')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

data = pd.read_csv('C:\\Users\\DELL\\Documents\\dataViz\\Data_analyst.csv')
data_load_state = st.text('Loading data...')
data_load_state.text('Loading data...done!')

col1, col2 = st.columns((2))

st.sidebar.text("Nom & Prénom: Oriane Assalé")
st.sidebar.text("Classe: M1")
st.sidebar.text("Filière: BIA")
st.sidebar.text("Promo : 2025")
st.sidebar.text("Nom du professeur: DILMI")
st.sidebar.link_button(url ="https://www.linkedin.com/in/oriane-assale/",label="Linkedin",use_container_width=True)

st.sidebar.header("Choisi ton filtre : ")
Location = st.sidebar.multiselect("Choisi la localisation" , data['Location'].unique())
if not Location:
    df=data.copy()
else:
    df=data[data["Location"].isin(Location)]


salaire_maximal = df.groupby(["Location", "Job Title"])["Max_Salary"].max().reset_index()
job_title = df['Job Title'][~df['Job Title'].isnull()]
data_analyst = df[df['Job Title'] == 'Data Analyst']
easy_apply=df[df['Easy Apply']==True]
easy=easy_apply.groupby('Company Name')['Easy Apply'].count().reset_index().head(10)
taux_moyen = df.groupby("Job Title")["Rating"].mean().reset_index()



with col1 :
    st.title("Nuage des mots")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(' '.join(job_title))
    st.image(wordcloud.to_array())

    st.subheader("   ")
    st.subheader("   ")
    st.subheader("   ")

    #2e graphe
    fig = bar(salaire_maximal, x='Job Title', y='Max_Salary', color='Location', barmode='group', title='Salaire maximal par job en fonction de la localisation')
    fig.update_xaxes(title_text=None)  # Supprimer le nom de l'axe des x
    fig.update_yaxes(title_text=None)
    st.plotly_chart(fig, use_container_width=True)


    #3e graphe
    fig_min_salary = histogram(
        df,
        title='Distribution des salaires minimaux pour les datas analystes',
        x='Min_Salary',
        nbins=20  # Ajustez le nombre de bacs au besoin
    )
    fig.update_xaxes(title_text=None)  # Supprimer le nom de l'axe des x
    st.plotly_chart(fig_min_salary)



with col2 :
    colors = {
        '1 to 50 employees': 'red',
        '51 to 200 employees': 'green',
        '201 to 500 employees': 'blue',
        '501 to 1000 employees': 'orange',
        '1001 to 5000 employees': 'purple',
        '5001 to 10000 employees': 'pink',
        '10000+ employees': 'yellow',
        'Unknown': 'gray'
    }
    df['Color'] = df['Size'].map(colors)

    #1er graphe
    st.subheader("Nombre de data analystes par secteur")
    data_analyst_df = df[df['Sector'] != '0']
    sector_counts = data_analyst_df['Sector'].value_counts()
    st.bar_chart(sector_counts)

    # 2e graphe
    fig = bar(df, x='Company Name', color='Size', color_discrete_map=colors, title='Distribution de la taille des entreprises ')
    fig.update_xaxes(title_text=None)
    st.plotly_chart(fig)

    #3e graphe
    fig_max_salary = histogram(
        df,
        x='Max_Salary',
        title='Distribution des salaires maximaux pour les Data Analysts',
        nbins=20
    )
    fig.update_xaxes(title_text=None)
    st.plotly_chart(fig_max_salary)


#4e graphe
fig = scatter(taux_moyen, x='Job Title', y='Rating', color='Rating', hover_data=['Job Title'],
              title='Le taux des personnes embauchées en fonction du job')
fig.update_layout(
        xaxis_title="Taux",
        yaxis_title="Salaire Maximum",
    )
fig.update_xaxes(title_text=None)
fig.update_yaxes(title_text=None)
st.plotly_chart(fig)

#5e graphe
fig = histogram(easy, x='Company Name', color='Easy Apply', histnorm='percent', title='Les entreprises qui acceptent facilement les dépots de candidatures')
fig.update_xaxes(title_text=None)
st.plotly_chart(fig, use_container_width=True)


#6e graphe
entreprise = data_analyst['Company Name'].value_counts().reset_index()
entreprise.columns = ['Company Name', 'Count']
# Triez les entreprises par nombre de Data Analysts embauchés
entreprise_counts = entreprise.sort_values(by='Count', ascending=False)
# Affichez les 10 premières entreprises qui embauchent le plus de Data Analysts
top_10_entreprise = entreprise_counts.head(10)

fig = bar(top_10_entreprise, x='Company Name', y='Count', title='Top 10 des entreprises qui embauchent les data Analaystes')
fig.update_xaxes(title_text=None)
fig.update_yaxes(title_text=None)
st.plotly_chart(fig)






