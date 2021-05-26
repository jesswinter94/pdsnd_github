import time
import pandas as pd
import numpy as np


#importing data from the provided csv's.
CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv', 'washington': 'washington.csv' }

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Done: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #setting empty city variable to start with
    city = ''
   
    # To print all keys and values concatenated together
    print ('Available cities imported: {} '.format(CITY_DATA.keys()))   
    city=input('Please insert the city to investigate: \n').lower()
    
    while city not in CITY_DATA:
        print ('Not a valid city - please see valid valid value: ', str(CITY_DATA.keys()))
        city=input('Please enter valid value: \n').lower()
        
    print(f"\nConfirmed -  {city.title()} as selected City.")    

    # Done: get user input for month (all, january, february, ... , june)
    MONTH_DATA = {'all': 0, 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6 }
    month = ''
    
    print ('Available months of data: {}', MONTH_DATA.keys())
    month=input('Please insert the month to investigate: \n').lower() 
    
    while month not in MONTH_DATA.keys():
        print("\nEnter the month, between January to June, for which you're seeking the data \nTo investigate data for all months enter 'all'")
        month = input('Please enter valid value: \n').lower()

    print(f"\nConfirmed -  {month.title()} as selected month.")

    # Done: get user input for day of week (all, monday, tuesday, ... sunday)
    DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    
    print ('Available days of data: ', *DAYS)
    day=input('Please insert the day to investigate: \n').lower() 
    
    while day not in DAYS:
        print("\nEnter a valid day, or select all as an option: ", *DAYS)
        day = input('Please enter valid value: \n').lower()

    print(f"\nConfirmed -  {day.title()} as selected day.")

    print('-'*40)
    
    print('Confirmed inputs: \nCity:',city, '\nMonth: ', month, '\nDay: ',day)
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
    print("\nLoading ", city , " data for analysis")
    df = pd.read_csv(CITY_DATA[city])

    #Converting the StartTime column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    
    
    #Filter by month if applicable
    if month != 'all':
        #Index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Done:: display the most common month
    common_month = df['month'].mode()[0]
    print('Month as index = January = 0, February = 1, March = 2 etc....')
    print('Most common Month:', common_month)


    # Done:: display the most common day of week
    common_day = df['day'].mode()[0]
    print('Most common day of week: ', common_day)

    # Done: display the most common start hour
    #Getting hour from StartTime which was defined above
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common start hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Done: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most  common start station:', common_start_station)



    # Done: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station: ', common_end_station)

    #Done: display most frequent combination of start station and end station trip
    #Creating a new variable that is a concatination of the Start & End stations
    #Will then use mode - similar to previous calculations to get the most popular
    
    df['Start_End'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    Start_End = df['Start_End'].mode()[0]
    print('Most common start & end stations combined: ', Start_End)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Done: display total travel time
    #Will use the sum method to get total stats
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)
    #Finds out the duration in minutes and seconds format
    mins, secs = divmod(total_travel_time, 60)
    #Finds out the duration in hour and minutes format
    print('This translates as ',mins , ' minutes and ' , secs , ' seconds')

    #Done: display mean travel time
    #Will use the mean method to get mean stats
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)
    MeanMins, MeanSecs = divmod(mean_travel_time, 60)
    #Finds out the duration in hour and minutes format
    print('This translates as ',MeanMins , ' minutes and ' , MeanSecs , ' seconds')

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Done: Display counts of user types
    #Reading from User Type field from data csv. - Either Customer or Subscriber
    print('\nUser Types:')
    print(df['User Type'].value_counts())

    #Done: Display counts of gender
    #not all the files available have gender as an option - therefore need to deal with this scenario
    #will use a try except for this
    try:
        print('\nGender Stats:')
        gender = df['Gender'].value_counts()
        print(gender)
    except:
        print('There is no Gender column in this file.')

    #Done: Display earliest, most recent, and most common year of birth
    #similarly to Gender - not all files have the birth year field in the raw data so will use try except again
    try:
        print('\nBirth Year Stats:')
        #casting to int to remove floating .0 after the Year values
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print('Earliest year of birth: ',earliest, '\nMost recent year of birth: ', most_recent,'\nMost common year of birth: ', common)
    except:
        print ('There is no Birth Year column in this file.')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    """
    Allow the user to view the raw data loaded into the dataframe. Will iterate in rows of 5.
    """
    #begin row counter at 0 for beginning of df and take first 5 rows.
    readData = 0
    endData = 5
    view_input = ''
    #being the while loop for user to decide if they want to view data
    while view_input.lower() not in ['yes', 'no']:
        view_input = input('View raw data from file?\'Yes\' or \'No\'\n')
        if view_input.lower() not in ['yes', 'no']:
            print('Not valid input. Enter Yes to continue or No to exit \n')
        elif view_input.lower() == "yes":
            #Using Pandas & iloc functionality for integer based indexing
            print(df.iloc[readData:endData])
            #option to continue viewing data if user chooses to
            while True:
                continue_input = input('\nContinue viewing data from file?\'Yes\' or \'No\'\n')
                if continue_input.lower() not in ['yes', 'no']:
                    print('Not valid input. Enter Yes to continue or No to exit \n')
                elif continue_input.lower() == "yes":
                    readData += 5
                    endData += 5
                    print(df.iloc[readData:endData])
                elif continue_input == "no":
                    return
        elif continue_input.lower() == "no":
            return
    return    
    
    
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
