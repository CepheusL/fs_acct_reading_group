import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from streamlit_calendar import calendar

# Initialize session state variables to store data across user interactions
if 'availability' not in st.session_state:
    # DataFrame to track user availability by date and name
    st.session_state['availability'] = pd.DataFrame(columns=['Date', 'Name'])

if 'topics' not in st.session_state:
    # DataFrame to store meeting topics and their associated vote counts
    st.session_state['topics'] = pd.DataFrame(columns=['Topic', 'Votes'])

# Title of the application
st.title("Meeting Organizer")

# Create two tabs for different functionalities: calendar and Meeting Topics
tabs = st.tabs(["calendar", "Meeting Topics"])

# Tab 1: calendar Functionality
with tabs[0]:
    st.header("Indicate Your Availability")

    # Display a calendar where users can click to select dates
    st.subheader("Select a date to add your availability")
    selected_date = calendar(events=st.session_state['availability'], 
                             events_label='title', 
                             events_start='start', 
                             events_end='end', 
                             key='calendar')

    # Input for the user's name
    name = st.text_input("Enter your name:")

    # Button to submit availability for the selected date
    if st.button("Submit Availability"):
        if name and selected_date:
            # Add the selected date and name to availability DataFrame
            new_entry = {'Date': selected_date, 'Name': name}
            st.session_state['availability'] = pd.concat(
                [st.session_state['availability'], pd.DataFrame([new_entry])],
                ignore_index=True
            )
            st.success(f"Availability added for {name} on {selected_date}.")
        else:
            st.error("Please enter your name and select a date.")

    # Section to display and summarize availability data
    st.subheader("Availability Overview")
    if not st.session_state['availability'].empty:
        # Show the full availability DataFrame
        st.write(st.session_state['availability'])

        # Summarize availability by grouping names for each date
        availability_summary = st.session_state['availability'].groupby('Date').Name.agg(list).reset_index()
        availability_summary['Count'] = availability_summary['Name'].apply(len)  # Count of people available per date

        # Visualize availability using a bar chart
        fig = px.bar(
            availability_summary, 
            x='Date', 
            y='Count', 
            text='Name', 
            title="Availability Summary"
        )
        st.plotly_chart(fig)
    else:
        st.write("No availability has been submitted yet.")

# Tab 2: Meeting Topics Functionality
with tabs[1]:
    st.header("Suggest and Vote on Topics")

    # Input field for suggesting a new meeting topic
    topic = st.text_input("Suggest a new topic:")

    # Button to add the new topic
    if st.button("Add Topic"):
        if topic:
            # Check if the topic already exists
            if topic not in st.session_state['topics']['Topic'].values:
                # Add the new topic with initial votes set to 0
                new_topic = {'Topic': topic, 'Votes': 0}
                st.session_state['topics'] = pd.concat(
                    [st.session_state['topics'], pd.DataFrame([new_topic])],
                    ignore_index=True
                )
                st.success(f"Topic '{topic}' added.")
            else:
                st.warning(f"Topic '{topic}' already exists.")
        else:
            st.error("Please enter a topic to add.")

    # Section to vote on topics
    st.subheader("Vote on Topics")
    if not st.session_state['topics'].empty:
        # Iterate through each topic and provide a voting button
        for index, row in st.session_state['topics'].iterrows():
            if st.button(f"Vote for '{row['Topic']}'"):
                # Increment the vote count for the selected topic
                st.session_state['topics'].at[index, 'Votes'] += 1
                st.success(f"You voted for '{row['Topic']}'.")

        # Display the topics sorted by votes in descending order
        st.write(st.session_state['topics'].sort_values(by='Votes', ascending=False))
    else:
        st.write("No topics have been added yet.")
