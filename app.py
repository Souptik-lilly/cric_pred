#write a streamlit app to predict the winner of the match
import streamlit as st
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import plotly.express as px


# load the model from disk
model = pickle.load(open('model.pkl', 'rb'))

def create_feature_map(features):
    outfile = open('xgb.fmap', 'w')
    for i, feat in enumerate(features):
        outfile.write('{0}\tq\n'.format(feat))
    outfile.close()

# define a function which will make the prediction using the data which the user inputs
def predict_winner(selected_elements):
    team1 = selected_elements[0]
    team2 = selected_elements[1]
    is_batting_team = selected_elements[2]
    innings_over = selected_elements[3]



    # Pre-processing user input
    innings_over = innings_over.split('_')
    innings = innings_over[0]
    over = innings_over[1]

    #replace innings_over with innings and over
    selected_elements[3] = innings
    selected_elements.append(over)


    if is_batting_team == team1:
        selected_elements[2] = 1 #is batting team
    elif is_batting_team == team2:
        selected_elements[2] = 0 #is batting team

    #if toss decision is bat, then replace with 1 else 0
    if selected_elements[7] == 'bat':
        selected_elements[7] = 1
    else:
        selected_elements[7] = 0
    
    # drop team1 and team2
    selected_elements = selected_elements[2:]
    
    # Making predictions
    prediction = model.predict(xgb.DMatrix(data=np.array([selected_elements],dtype=object)))
   
    print(len(prediction))

    pred = prediction
    
    return pred

# this is the main function in which we define our webpage
def main():
    # front end elements of the web page
    html_temp = """
    <div style ="background-color:tomato;padding:13px">
    <h1 style ="color:white;text-align:center;">IPL Winner Prediction ML App</h1>
    </div>
    """ 
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True)

    # following lines create boxes in which user can enter data required to make prediction
    team1 = st.selectbox('Team 1',('Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad'))
    team2 = st.selectbox('Team 2',('Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad'))
    is_batting_team = st.selectbox('Batting Team',(team1, team2))

    innings_over = st.selectbox('Innings and over',('1_1', '1_2', '1_3', '1_4', '1_5', '1_6', '1_7', '1_8', '1_9', '1_10', '1_11', '1_12', '1_13', '1_14', '1_15', '1_16', '1_17', '1_18', '1_19', '1_20', '2_1', '2_2', '2_3', '2_4', '2_5', '2_6', '2_7', '2_8', '2_9', '2_10', '2_11', '2_12', '2_13', '2_14', '2_15', '2_16', '2_17', '2_18', '2_19', '2_20'))

    innings_score = st.number_input("Innings score",min_value=0)
    innings_wickets = st.number_input("Innings wickets",min_value=0)
    score_target = st.number_input("Score target",min_value=-1)
    toss_decision = st.selectbox('Toss decision',('bat', 'field'))
    total_runs = st.number_input("Total runs",min_value=0)
    remaining_target = st.number_input("Remaining target",min_value=-1)
    run_rate = st.number_input("Run rate",min_value=0)
    required_run_rate = st.number_input("Required run rate",min_value=-1)
    runrate_diff = st.number_input("Runrate difference",min_value=-1)
    player_dismissed = st.number_input("Player dismissed",min_value=0)

    # make a list of all streamlit elements
    elements = [team1, team2, is_batting_team, innings_over, innings_score, innings_wickets, score_target, toss_decision, total_runs, remaining_target, run_rate, required_run_rate, runrate_diff, player_dismissed]
    # pass all elements as a list to the function which makes the prediction using the data which the user inputs
    
    result =""
    # when 'Predict' is clicked, make the prediction and store it
    if st.button("Predict"):
        result = predict_winner(elements)
        #create a slider to show the winning probability for team 1 and team 2
        st.slider('{}'.format(team1), 0.0, 100.0, (float(result[0]*100)))
        st.slider('{}'.format(team2), 0.0, 100.0, (float(100 - result[0]*100)))

        # create a dataframe to store results for team 1 and team 2
        df = pd.DataFrame({'Team': [team1, team2], 'Winning Probability': [float(result[0]*100), float(100 - result[0]*100)]})
        df2 = df.set_index("Team").unstack().to_frame().reset_index()
        # create a bar chart to show the winning probability for team 1 and team 2 with text inside the bar chart
        fig = px.bar(df2, x=0, y='level_0', color='Team', orientation='h',color_discrete_sequence=px.colors.qualitative.Dark2)
        #remove x axis label and y axis label
        #fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        # remove x axis title and y axis title
        fig.update_xaxes(title_text='Winning Probability')
        fig.update_yaxes(title_text='')
        team2_logo = 'data:image/jpeg;base64,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'
        team1_logo = 'data:image/jpeg;base64,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'

        # add logo to the chart and make it transparent
        
        fig.update_layout(
            images=[
                dict(
                    source=team1_logo,
                    xref="paper", yref="paper",
                    x=0.1, y=1.05,
                    sizex=0.5, sizey=0.5,
                    xanchor="right", yanchor="bottom"
                ),
                dict(
                    source=team2_logo,
                    xref="paper", yref="paper",
                    x=0.95, y=1.05,
                    sizex=0.5, sizey=0.5,
                    xanchor="right", yanchor="bottom"
                )
            ])
        
        # add figsize of the chart
        fig.update_layout(
            height=200,
            width=800,
            title_text="",
            title_x=0.1,
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
        # add xticks to the chart in group of 5 within 0-100
        fig.update_xaxes(
            tickmode = 'array',
            tickvals = [i for i in range(0,105,5)],
            ticktext = [i for i in range(0,105,5)]
        )

        # display the chart
        st.plotly_chart(fig)



    if st.button("About"):
        st.text("Lets Learn")
        st.text("Built with Streamlit")



if __name__=='__main__':
    main()




