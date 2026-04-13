import pandas as pd

def calculate_team_metrics(actual_df, analysis_columns):
    current_sprint = analysis_columns[-1]
    previous_sprint = analysis_columns[-2] if len(analysis_columns) > 1 else None

    current_total = actual_df[current_sprint].sum()
    previous_total = actual_df[previous_sprint].sum() if previous_sprint else 0
    velocity_delta = current_total - previous_total

    actual_df['Global_Total'] = actual_df[analysis_columns].sum(axis=1)
    global_sprints_total = actual_df['Global_Total'].sum()

    average_per_member = current_total / len(actual_df) if len(actual_df) > 0 else 0

    return {
        "current_total": current_total,
        "velocity_delta": velocity_delta,
        "average_per_member": average_per_member,
        "people_count": len(actual_df),
        "global_sprints_total": global_sprints_total
    }

def calculate_individual_metrics(actual_df, analysis_columns, name_col, selected_member):
    current_sprint = analysis_columns[-1]
    previous_sprint = analysis_columns[-2] if len(analysis_columns) > 1 else None

    member_data = actual_df[actual_df[name_col] == selected_member].iloc[0]
    member_history = member_data[analysis_columns].astype(float)
    
    current_delivery = member_history[current_sprint]
    previous_delivery = member_history[previous_sprint] if previous_sprint else 0
    individual_delta = current_delivery - previous_delivery
    
    individual_average = member_history.mean()
    individual_median = member_history.median()
    individual_std_dev = member_history.std() if len(member_history) > 1 else 0
    
    team_total = actual_df[analysis_columns].sum().sum()
    participation_percentage = (member_history.sum() / team_total * 100) if team_total > 0 else 0

    return {
        "member_history": member_history,
        "current_delivery": current_delivery,
        "individual_delta": individual_delta,
        "individual_average": individual_average,
        "individual_median": individual_median,
        "individual_std_dev": individual_std_dev,
        "total_deliveries": member_history.sum(),
        "best_sprint": member_history.max(),
        "worst_sprint": member_history.min(),
        "participation_percentage": participation_percentage
    }