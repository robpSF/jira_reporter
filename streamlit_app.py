import streamlit as st
import pandas as pd
import plotly.express as px

myfile = st.file_uploader("Enter Jira export file")

show_assignee = st.sidebar.checkbox("Assignee chart")
show_fixtimes = st.sidebar.checkbox("Fix duration chart")


def assignee_chart(df):
    st.subheader("Bug Master")
    assignee_counts = df['Assignee'].value_counts()
    #bar chart
    fig = px.bar(assignee_counts, y=assignee_counts.index, x=assignee_counts.values,orientation='h',
                 labels={'y': 'Assignee', 'x': 'Count'})
    st.plotly_chart(fig)

    #pie chart
    fig = px.pie(assignee_counts, values=assignee_counts.values, names=assignee_counts.index, title='Assignee Counts')
    st.plotly_chart(fig)
    return

def fix_duration(df):
    st.subheader("How long did it take to fix the bugs?")
    interval = st.slider("Group fix duration by how many days?",1,7)
    df['Created'] = pd.to_datetime(df['Created'])
    df['Updated'] = pd.to_datetime(df['Updated'])
    df['Duration'] = (df['Updated'] - df['Created']).dt.total_seconds() / (3600 * 24)

    duration_grouped = df.groupby(pd.cut(df['Duration'], bins=range(0, int(df['Duration'].max()), interval))).count()
    duration_grouped.index = duration_grouped.index.astype(str)

    # remove any 0 rows
    duration_grouped = duration_grouped[duration_grouped['Assignee'] > 0]

    fig = px.bar(duration_grouped, x=duration_grouped['Duration'], y=duration_grouped.index, orientation='h',
                 labels={'x': 'Count', 'y': 'Duration (Days)'})
    st.plotly_chart(fig)

    fig = px.pie(duration_grouped, values='Duration', names=duration_grouped.index, title='Time to fix (Days)')
    st.plotly_chart(fig)

    return


if myfile != None:
    df = pd.read_csv(myfile)
    total_rows = df.shape[0]
    st.write("Total number of bugs:", total_rows)

    if show_assignee:  assignee_chart(df)
    if show_fixtimes: fix_duration(df)
