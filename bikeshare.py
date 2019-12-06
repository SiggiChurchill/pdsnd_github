import time
import pandas as pd
import numpy as np
import sys



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
    print("""\n
888     d8b                        888         
888     Y8P                        888         
888                                888         
88888b. 888 .d8888b888  888 .d8888b888 .d88b.  
888 "88b888d88P"   888  888d88P"   888d8P  Y8b 
888  888888888     888  888888     88888888888 
888 d88P888Y88b.   Y88b 888Y88b.   888Y8b.     
88888P" 888 "Y8888P "Y88888 "Y8888P888 "Y8888  
                        888                    
                   Y8b d88P                    
                    "Y88P"                     
             
Hello! Let's explore some US bikeshare data!

""")
    
    
    # get user input for city (chicago, new york city, washington). 
    city=""
    valid_cities = ['chicago','chi','new york city','nyc','washington','wtn']

    while city not in valid_cities:
        city = str(input("What city would you like data for? Chicago(chi), "
                         "New York City(nyc) or Washington(wtn): ")).lower()
        if city == 'exit':
            while city =='exit':
                sys.exit()
        if city not in valid_cities:
            print("That's not a valid selection! Please check and try again.")
        # adjust city name to full name if abbreviation was entered
        elif valid_cities.index(city)%2 != 0:
            city = valid_cities[valid_cities.index(city)-1]
    print("Pulling data for {}.".format(city.upper()))
    
    
    # get user input for month (all, january, february, ... , june)
    month =""
    valid_months = ['january','february','march','april','may','june','all']

    while month not in valid_months:
        month = str(input("What month would you like data for? Select All or a"
                          " month from January to June: ")).lower()
        if month == 'exit':
            sys.exit()
        if month not in valid_months:
            print("That's not a valid selection! Please check and try again.")
    print("Pulling data for {}.".format(month.upper()))


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day =""
    valid_days = ['monday','tuesday','wednesday','thursday','friday','saturday'
                  ,'sunday','all']
    
    while day not in valid_days:
        day = str(input("What day would you like data for? Select All or a day"
                        " from Monday to Sunday: ")).lower()
        if day == 'exit':
            sys.exit()
        if day not in valid_days:
            print("That's not a valid selection! Please check and try again.")
    print("Pulling data for {}.".format(day.upper()))


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
    
    # drop added index column
    df = df.drop(['Unnamed: 0'], axis=1)

    # convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract start time, month, day of week and travel time from Start Time to 
    # create new columns
    df['start_hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['travel time'] = df['End Time'] - df['Start Time']
    
    


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    

    return df


def get_data(df):
    """
    Allows user to review five rows of raw data in the console, or to export
    all requested raw data to a .csv file in home directory
    """
    entry = ""
    valid_entry = ['y','n','export']
    while entry not in valid_entry:
        entry = input('\nWould you like to sample the data? Enter Y, N or' 
                      ' export.\n').lower()
        if entry == 'exit':
            sys.exit()
        if entry =='y':
            x=5
            while x<len(df):
                print(df[x-5:x])
                x+=5
                entry = input('\nContinue sample? Y or N\n')
                if entry.lower()!='y':
                    return df
        elif entry =='export':
            start_time = time.time()
            print("Exporting...")
            df.to_csv('BikeShare Data Export_{}.csv'.format(time.time()))
            print("Export complete! Saved as BikeShare Data Export_{}.csv".format(
                    time.time()))
            print("\nThis took {} seconds.".format(round(((time.time() - 
                  start_time)),6)))
            return df
        elif entry =='n':
            return df

        else:
            print("\nThat's not a valid selection! Please check and try again.")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')
    
    # display the most common month - skips if specific month selected
    month_dict={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June'}
    if df['month'].nunique()> 1:
        print("The most common month in the requested data is {}.".format(
                month_dict[df['month'].mode().max()]))
    else:
        print("The data is filtered to {} only.".format(
                month_dict[df['month'].max()]))
        
    # display the most common day of week
    if df['day_of_week'].nunique()> 1:
        print("The most common day of week in the requested data is {}.".format(
                df['day_of_week'].mode().max()))
    else:
        print("The data is filtered to {} only.".format(df['day_of_week'].max()))

    # display the most common start hour
    print("The most common start hour in the requested data is {}:00.".format(
            df['start_hour'].mode().max()))

    print("\nThis took {} seconds.".format(round(((time.time() - start_time)),6)))
    print('-'*40)
    
    #offer data sample / export
    get_data(df)

        
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station in the requested data is {}.".
          format(df['Start Station'].mode().max()))

    # display most commonly used end station
    print("The most commonly used end station in the requested data is {}.".
          format(df['End Station'].mode().max()))

    # display most frequent combination of start station and end station trip 
    # (creates crosstab)
    xtab_stat = pd.crosstab(df['Start Station'],df['End Station'])
    print("The most common journey in the requested data is from {} to {}.".
          format(xtab_stat.max(axis=0).idxmax(), 
          xtab_stat.max(axis=1).idxmax()))

    print("\nThis took {} seconds.".format(round(((time.time() - start_time)),6)))
    print('-'*40)
    
    #offer data sample / export
    get_data(df)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    print("The total travel time in the requested data is {}.".format(
          df['travel time'].sum()))

    # display mean travel time
    print("The mean travel time in the requested data is {}.".format(
          df['travel time'].mean()))

    print("\nThis took {} seconds.".format(round(((time.time() - start_time)),6)))
    print('-'*40)
    
    #offer data sample / export
    get_data(df)


def user_stats(df):
    """Displays statistics on bikeshare users."""  
     
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = np.array(df['User Type'].unique(), dtype = 'object')
    print("The breakdown of user types is as follows:")
    for user_type in user_types:
        if str(user_type).lower() == 'nan':
            print("No Record: {}".format(df['User Type'].isnull().sum().sum()))
        else:             
            print("{}: {}".format(user_type,df['User Type'][df['User Type']==
                  user_type].count()))
        
    # Display counts of gender (if data available)
    if 'Gender' in df:        
        genders = np.array(df['Gender'].unique(), dtype = 'object')
        print("\nThe breakdown of customers' gender is as follows:")
        for gender in genders:
            #don't fillna as will cause problems for Data Errors function!
            if str(gender).lower() == 'nan':
                print("No Record: {}".format(df['Gender'].isnull().sum().sum()))
            else:
                print("{}: {}".format(gender,df['Gender'][df['Gender']==
                  gender].count()))
        
    # Display earliest, most recent, and most common year of birth 
    # (if data available)  
    if 'Birth Year' in df:       
        print("\nThe earliest birth year in the requested data is {}.".format(
                int(df['Birth Year'].min())))
        print("The latest birth year in the requested data is {}.".format(
                int(df['Birth Year'].max())))
        print("The most common birth year in the requested data is {}.".format(
                int(df['Birth Year'].mode().max())))
            
        
    print("\nThis took {} seconds.".format(round(((time.time() - start_time)),6)))
    print('-'*40)

    #offer data sample / export
    get_data(df)
    
def data_errors(df):
    """Flags potential data errors"""
    print('\nChecking for data errors...\n')
    start_time = time.time()
    
    # Check for negative travel times
    print("{} instances of negative travel times.\n".format(df['travel time'][
            df['travel time'].dt.days<0].count()))
          
    # Check for nulls
    if (df.isnull().sum().sum()) == 0:
        print("No null data found in requested data.\n")
    else:
        print("Null data found in requested data:\n{}".format(df.isnull().sum()))
              
    
    print("\nThis took {} seconds.".format(round(((time.time() - start_time)),6)))
    print('-'*40)

    #offer data sample / export
    get_data(df)

def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            # stat selection menu 
            print("""
                  1 - All stats
                  2- Travel Time Stats
                  3- Popular Station Stats
                  4- Trip Duration Stats
                  5- User Stats
                  6- Data Errors
                  
                  Enter 'Exit' at any time to exit the program.""")
            
            statint = '0'
            while statint not in str(range(1,6,1)):
                statint = input("Please select required stats (enter number): ")
                if statint.lower() == 'exit':
                    sys.exit()
                    
                if  statint == '1':
                    time_stats(df)
                    station_stats(df)
                    trip_duration_stats(df)
                    user_stats(df)
                    data_errors(df)
                    break
                elif statint == '2':
                    time_stats(df)
                    break
                elif statint == '3':
                    station_stats(df)
                    break
                elif statint == '4':
                    trip_duration_stats(df)
                    break
                elif statint == '5':
                    user_stats(df)
                    break
                elif statint == '6': 
                    data_errors(df)
                    break
                else:
                    print("That is not a valid selection! Please check and try again.")
                    if statint == "":
                        statint = '0'
    
            restart = input('\nWould you like to restart? Enter Y or N.\n')
            if restart.lower() != 'y':
                break
        except SystemExit:
            print("Exiting Program.")
            break
  
if __name__ == "__main__":
	main()
