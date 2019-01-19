import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
cities = ['Chicago', 'New York City', 'Washington']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to explore the data of Chicago, New York City or Washington?\n').title()
    while city not in cities:
       city = input('Invalid input!  Please enter again: \n').title()
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Which month do you want to input?(e.g. all, january, february, march, april, may, june)\n').title()
    while month not in months:
        month = input('Invalid input!  Please enter again: \n').title()
      # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Could you type one of the week day you want to analyze?(e.g. all, monday, tuesday, wednesday, ..., sunday)\n').title()
    while day not in days:
        day = input('Invalid input!  Please enter again: \n').title()
 
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month =  months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is: \n', most_common_month)

    # TO DO: display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is: \n', most_common_day_of_week)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: \n', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: \n', most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: \n', most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + 'to' + df['End Station']
    combination_trip = df['combination'].value_counts().index[0]
    print('The most commonly frequent combination of start station and end station is: \n{}'.format(combination_trip))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = df['Trip Duration'].sum()
    print('Total travel time is: \n', total)

    # TO DO: display mean travel time
    mean = df['Trip Duration'].mean()
    print('Mean travel time is: \n', mean)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The result of counts of user types is: \n', user_types)

    # TO DO: Display counts of gender
    cities_columns = df.columns
    if 'Gender' in cities_columns:
        gender_counts = df['Gender'].value_counts()
        print('The reuslt of counts of gender is: \n', gender_counts)
    else:
        print('Sorry, this city doesn\'t have gender data')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in cities_columns:
        birth_year = df['Birth Year']
        most_common_year = birth_year.value_counts().index[0]
        print('The most common birth year is: \n', most_common_year)
        most_recent = birth_year.max()
        print('The most recent birth year is: \n', most_recent)
        earliest_year = birth_year.min()
        print('The most earliest birth year is: \n', earliest_year)
    else:
        print('Sorry, this city doesn\'t have birth data')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

#View 5 lines of raw data and display that data if the answer is 'yes'
def display_raw_data(df):
    print(df.head())
    next = 0
    while True:
        show_raw_data = input('\nWould you like to view next five rows of raw data?  Pleasue enter yes or no.\n')
        if show_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            show_raw_data = input('\nWould you like to view next five rows of raw data?  Pleasue enter yes or no.\n')
            if show_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
	main()
