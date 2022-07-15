from calendar import month
from itertools import groupby
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ['chicago','new york city','washington']
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        try:
            city = str(input('Which city do you want to analyse (Chicago, New York City, Washington)?').lower())	
            if city in cities:
                break
            else:
                city = str(input('Please enter a valid city (Chicago, New York City, Washington):').lower())
                if city in cities:
                    break
        except:
            print("Please enter a valid city like follows (Chicago, New York City, Washington):\n")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Which month do you want to analyse (All, January, February, ... , June)?').lower())	
            if month in months:
                break
            else:
                month = str(input('Please enter a valid month like follows (All, January, February, ... , June):').lower())
                if month in months:
                    break
        except:
            print("Please enter a valid month like follows (All, January, February, ... , June):\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Which day of week do you want to analyse (All, Monday, Tuesday, ... Sunday)?').lower())	
            if day in days:
                break
            else:
                day = str(input('Please enter a valid day like follows (All, Monday, Tuesday, ... Sunday):').lower())
                if day in days:
                    break
        except:
            print("Please enter a valid day like follows (All, Monday, Tuesday, ... Sunday):\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])

    #changing Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #create new columns months and day_of_week using extracted values 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #according to users intrest filter month
    if month != 'all':
        #get the corresponding int with the use of the inex of the month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #creating new dataframe with filtered month
        df = df[df['month'] == month]

   #according to users intrest filter month
    if day != 'all':
        #creating new dataframe with filterd day_of_week
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('The most common month: ',months[(df['month'].mode()[0])-1].title())

    # display the most common day of week
    print('The most common day of week: ',df['day_of_week'].mode()[0])

    # display the most common start hour
    # convert the Start Time column to datetime again to be confirm
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common start hour hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common start hour: ',common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    count_common_start_station = (df['Start Station']==common_start_station).sum()
    print('Most commonly used Start Station: {} count: {}'.format(common_start_station,count_common_start_station))

    # display most commonly used end station (df.education == '9th').sum()
    common_end_station = df['End Station'].mode()[0]    
    count_common_end_station = (df['End Station']==common_end_station).sum()
    print('Most commonly used End Station: {} count: {}'.format(common_end_station,count_common_end_station))

    # display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station']+','+df['End Station']).mode()[0]
    frequent_combination_count = ((df['Start Station']+','+df['End Station'])==frequent_combination).sum()
    print('Most frequent combination of trip: {} count: {}'.format(frequent_combination,frequent_combination_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ',total_travel_time)
    # display mean travel time
    travel_time_mean = df['Trip Duration'].mean()
    print("Mean of Travel time: ",travel_time_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Reason for using .to_string() to delete unnessary details about index
    print("Counts of user types:\n{}\n".format((df.groupby('User Type').size()).to_string()))

    # Display counts of gender 
    try:
        print("Counts of Gender:\n{}\n".format((df.groupby('Gender').size()).to_string()))
    except:
        print("Counts of Gender:\nThere is no Gender details available in this city Database\n")

    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest year of birth: ",int(df['Birth Year'].min()))
        print("Most recent year of birth: ",int(df['Birth Year'].max()))
        print("Most common year of birth: ",int(df['Birth Year'].mode()[0]))
    except:
        print("Earliest year of birth, Most recent year of birth, Most common year of birth:")
        print("'Birth Year' details are not available in this city, So it's unable to full fill the above requests")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    #Display Raw data is displayed upon request by the user
    count = 0
    while True:
        raw_data = input("\nWould you like to review 5 lines of Raw data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            count += 5
            print(df[count-5:count])
        elif raw_data.lower() == 'no':
            break
        else:
            print("Please enter a valid response. Thank you")
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)   
        restart = input("\nEnter 'yes' if you would like to restart?\n")
        if restart.lower() != 'yes':
            print("Thank you. Have a great day")
            break
    
if __name__ == "__main__":
	main()
