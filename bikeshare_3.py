import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze..

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        try:
            city = input('Would you like to see the data for Chicago, New York or Washington?\n').lower()
            assert city in CITY_DATA.keys(), "'Invalid Data! Try again'"
            break
        except AssertionError as e:
            print(e)

    expected_options = ['month', 'day', 'both', 'none']
    while True:
        try:
            option = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter \n').lower()
            assert option in expected_options, "'Invalid Data! Try again\n'"
            break
        except AssertionError as e:
            print(e)
    
    month = 'all'
    day = 'All'
    # get user input for month (all, january, february, ... , june)
    if(option == 'month' or option == 'both'):
        expected_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        while True:
            try:
                month = input('Which month? January, February, March, April, May, June or all? \n').lower()
                assert month in expected_months, "'Invalid Data! Try again\n'"
                break
            except AssertionError as e:
                print(e)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if(option == 'day' or option == 'both'):
        expected_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'All']
        while True:
            try:
                day = input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all? \n').title()
                assert day in expected_days, "'Invalid Data! Try again\n'"
                break
            except AssertionError as e:
                print(e)
    if(option == 'none'):
        month = 'all'
        day = 'All'


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()   
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    df['day of week'] = df['Start Time'].dt.day_name()   
    popular_day = df['day of week'].mode()[0]
    print('Most Popular Day of Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour   
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' - ' + df['End Station']
    most_frequent_trip = df['trip'].mode()[0]
    print('Most Popular trip from start to end:', most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])  

    # display total travel time
    df['total travel time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['total travel time'].sum()
    total_seconds = total_travel_time.total_seconds()
    print("Total Travel Time:", total_seconds)


    # display mean travel time
    mean_travel_time = df['total travel time'].mean()
    mean_seconds = mean_travel_time.total_seconds()
    print("Average Travel Time:", mean_seconds)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Breakdown of Users:\n", df['User Type'].value_counts())    

    if city != 'washington':
        # Display counts of gender
        print("Breakdown of Genders:\n", df['Gender'].value_counts()) 

        # Display earliest, most recent, and most common year of birth
        print("Oldest, Youngest and Most Popular Year of Birth : {}, {}, {}".format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]))
    
    else:
        print('Gender and Birth Year stats cannot be calculated because Gender and Birth Year does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    while (view_data == 'yes' and (start_loc+5) <= len(df)):
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no?").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print('data = ',new)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
