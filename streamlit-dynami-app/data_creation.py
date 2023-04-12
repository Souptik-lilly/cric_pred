'''
Function to create live data
'''
import os
import csv
import time

data_path = r'/Users/L010166/Library/CloudStorage/OneDrive-EliLillyandCompany/md_ids/Challenges/jarvis-2023/git_repo/cric_pred'
match_file = '1359475_results.csv'
write_path = r'/Users/L010166/Library/CloudStorage/OneDrive-EliLillyandCompany/md_ids/Challenges/jarvis-2023/git_repo/cric_pred/streamlit-dynami-app/data'

def create_file():

    read_file = os.path.join(data_path, match_file)
    write_file = os.path.join(write_path, match_file)

    # read rows from git repo for the current ipl mathc
    def read_row():
        with open(read_file, 'r') as r_file:
            csvreader = csv.reader(r_file)
            next(csvreader, None)
            for row in csvreader:
                yield row
    
    # write row to new file
    def write_row(row):
        with open(write_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    
    # create new file
    with open(write_file, 'w') as w_file:
        writer = csv.writer(w_file)
        writer.writerow(["Row_No", "Team1", "match_id", "is_batting_team",\
            "Team2", "innings_over", "innings_score", "innings_wickets", 
            "score_target", "total_runs", "player_dismissed", "predictions", 
            "wickets_in_over", "required_run_rate", "predicted_team1", "predicted_team2"
            ])
        
    for row in read_row():
        write_row(row)
        time.sleep(30)
        

if __name__=='__main__':


    create_file()