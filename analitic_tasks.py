import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

if __name__ == '__main__':
    plt.figure(1, figsize=(12, 10))
    # all time
    plt.subplot2grid((2, 2), (0, 0), colspan=2)
    task_df = pd.read_csv('task_archive.csv', sep=',', encoding='utf-8')
    task_df['ProjectName'].value_counts().plot(kind='pie', autopct='%1.1f%%', title='Summary')
    plt.xlabel("")
    plt.ylabel("")
    plt.axis('equal')

    # current year
    plt.subplot2grid((2, 2), (1, 0))
    task_df['date'] = pd.DatetimeIndex(
        task_df['DataTime'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d_%H.%M.%S').date()))
    current_date = pd.to_datetime('now')
    current_year_df = task_df[task_df['date'].dt.year == current_date.year]
    current_year_df['ProjectName'].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                                       title=f'Current year: {current_date.year}')
    plt.xlabel("")
    plt.ylabel("")
    plt.axis('equal')

    # current month
    plt.subplot2grid((2, 2), (1, 1))
    current_month_df = current_year_df[task_df['date'].dt.month == current_date.month]
    current_month_df['ProjectName'].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                                        title=f'Current month: {current_date.month}')
    plt.xlabel("")
    plt.ylabel("")
    plt.axis('equal')
    plt.show()


