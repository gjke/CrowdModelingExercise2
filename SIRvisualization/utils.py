# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def file_df_to_count_df(df,
                        ID_SUSCEPTIBLE=1,
                        ID_INFECTED=0, ID_REMOVED=2):
    """
    Converts the file DataFrame to a group count DataFrame that can be plotted.
    The ID_SUSCEPTIBLE, ID_INFECTED and ID_REMOVED specify which ids the groups have in the Vadere processor file.
    """
    pedestrian_ids = df['pedestrianId'].unique()
    sim_time_index = np.arange(df['simTime'].min(), df['simTime'].max(), 1)
    pid_group_changes = {pid: (
        df[df['pedestrianId'] == pid]
        .set_index('simTime')['groupId-PID5']
        .reindex(sim_time_index)
        .ffill()
    ) for pid in pedestrian_ids}
    wide_df = pd.DataFrame(pid_group_changes)

    return pd.DataFrame({
        'simTime': sim_time_index,
        'group-s': (wide_df == ID_SUSCEPTIBLE).sum(axis=1).values,
        'group-i': (wide_df == ID_INFECTED).sum(axis=1).values,
        'group-r': (wide_df == ID_REMOVED).sum(axis=1).values
    })


def create_folder_data_scatter(folder):
    """
    Create scatter plot from folder data.
    :param folder:
    :return:
    """
    file_path = os.path.join(folder, "SIRinformation.csv")
    if not os.path.exists(file_path):
        return None
    data = pd.read_csv(file_path, delimiter=" ")

    ID_SUSCEPTIBLE = 1
    ID_INFECTED = 0
    ID_REMOVED = 2

    group_counts = file_df_to_count_df(
        data, ID_INFECTED=ID_INFECTED, ID_SUSCEPTIBLE=ID_SUSCEPTIBLE, ID_REMOVED=ID_REMOVED)

    print(group_counts)
    # group_counts.plot()
    scatter_s = go.Scatter(x=group_counts['simTime'],
                           y=group_counts['group-s'],
                           name='susceptible ' + os.path.basename(folder),
                           mode='lines')
    scatter_i = go.Scatter(x=group_counts['simTime'],
                           y=group_counts['group-i'],
                           name='infected ' + os.path.basename(folder),
                           mode='lines')
    scatter_r = go.Scatter(x=group_counts['simTime'],
                           y=group_counts['group-r'],
                           name='removed ' + os.path.basename(folder),
                           mode='lines')

    return [scatter_s, scatter_i, scatter_r], group_counts
