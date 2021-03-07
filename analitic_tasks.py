import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    fixed_df = pd.read_csv('task_archive.csv', sep=',', encoding='utf-8', parse_dates=['DataTime'],
                           index_col='DataTime')
    fixed_df['ProjectName'].value_counts().plot(kind='pie')
    plt.show()
    # fixed_df.index = pd.to_datetime(fixed_df.index, format="%Y-%m-%d_%H.%M.%S")
    # projects = fixed_df[['ProjectName']].copy()
    # projects.loc[:, 'Month'] = projects.index.month
    # # projects["Month"].value_counts().plot(kind='pie')
    # month_counts = projects.groupby('Month')
    # month_counts.index = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
    # month_counts.plot(kind='bar')
    # plt.show()
