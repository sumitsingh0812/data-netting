#Analysing the data for cards
# Importing the necessary liberaries
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

#importing the csv file
file=r"C:\Users\Admin\Desktop\cards_data.csv"
Dataframe=pd.read_csv(file)

#Checking if there are missing values
missing_values=Dataframe.isnull().values.any()
print('Are there any missing values?',missing_values)

# Selecting numeric columns for outlier detection
numeric_cols = Dataframe.select_dtypes(include=[np.number]).columns
print("\nNumeric columns to analyze:", numeric_cols)

# Detecting outliers using the IQR method
for col in numeric_cols:
    Q1 = Dataframe[col].quantile(0.25)
    Q3 = Dataframe[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.0 * IQR
    upper_bound = Q3 + 1.0 * IQR
    
    outliers = Dataframe[(Dataframe[col] < lower_bound) | (Dataframe[col] > upper_bound)]
    print(f"Outliers in {col} using IQR method:\n", outliers)


# Detecting outliers using Z-score
for col in numeric_cols:
    z_scores = np.abs(stats.zscore(Dataframe[col]))
    outliers = Dataframe[z_scores > 3]
    print(f"Outliers in {col} using Z-score method:\n", outliers)


#changing the date time format
Dataframe['expires'] = pd.to_datetime(Dataframe['expires'], format='%b-%y')
Dataframe['acct_open_date'] = pd.to_datetime(Dataframe['acct_open_date'], format='%b-%y')


# Reformat both columns to 'MM/YYYY' format
Dataframe['expires'] = Dataframe['expires'].dt.strftime('%m/%Y')
Dataframe['acct_open_date'] = Dataframe['acct_open_date'].dt.strftime('%m/%Y')


#Dropping the duplicates
Drop_duplicate=Dataframe.drop_duplicates()

#saving the csv file
csv_file = r"C:\Users\Admin\Desktop\cards_data_Modified.csv"
#Dataframe.to_csv(csv_file, index=False, date_format='%m/%Y')



# Answering few questions which one could ask



# 1. Total number of cards issued
Cards_issued = Dataframe['num_cards_issued'].sum()
print("Total number of cards issued:", Cards_issued)

# 2. Sum of different types of cards issued
Type_card_issued = Dataframe.groupby("card_type")['num_cards_issued'].sum()
print("\nSum of different types of cards issued:")
print(Type_card_issued)

# 3. Sum of all the chipped cards with brand
# Converting 'has_chip' to binary values: 1 for 'yes', 0 for 'no'
Dataframe['has_chip'] = Dataframe['has_chip'].str.lower().map({'yes': 1, 'no': 0})

# Grouping by 'card_brand' and summing the 'has_chip' values to get the number of chipped cards per brand
chip_cards = Dataframe.groupby('card_brand')['has_chip'].sum()
print("\nSum of chipped cards by card brand:")
print(chip_cards)

# 4. Number of cards on the dark web by card type
# Converting 'card_on_dark_web' to binary values: 1 for 'yes', 0 for 'no'
Dataframe['card_on_dark_web'] = Dataframe['card_on_dark_web'].str.lower().map({'yes': 1, 'no': 0})

# Grouping by 'card_type' and summing the 'card_on_dark_web' values to get the number of cards found on the dark web per card type
Darkweb_cards = Dataframe.groupby('card_type')['card_on_dark_web'].sum()
print("\nNumber of cards found on the dark web by card type:")
print(Darkweb_cards)


# Ensuring 'credit_limit' is clean and numeric
Dataframe['credit_limit'] = Dataframe['credit_limit'].replace('[\$,]', '', regex=True)  # Remove dollar signs
Dataframe['credit_limit'] = pd.to_numeric(Dataframe['credit_limit'], errors='coerce')  # Convert to numeric, coercing errors to NaN

# Dropping rows where credit_limit is NaN if necessary
Dataframe = Dataframe.dropna(subset=['credit_limit'])

# Calculating the average card limit
avg_cardlmt = Dataframe.groupby('card_brand')['credit_limit'].mean()
print("Average card limit by brand:\n", avg_cardlmt)


#Which year had the most PIN updates?
# Find the year with the most PIN updates
most_pin_updates_year = Dataframe['year_pin_last_changed'].value_counts().idxmax()

print(f"The year with the most PIN updates is {most_pin_updates_year}.")

# Using matplotlib to show the graphs

#Card Brand Distribution

Dataframe['card_brand'].value_counts().plot(kind='bar', title="Card Brand Distribution")
plt.xlabel("Card Brand")
plt.ylabel("Count of Cards")
plt.show()


#Percentage of Cards with Chips
chip_data = Dataframe['has_chip'].value_counts()
chip_data.plot(kind='pie', title="Cards with Chips vs Without", autopct='%1.1f%%')
plt.ylabel("")
plt.show()



#Expiration Dates

Dataframe['expires'] = pd.to_datetime(Dataframe['expires'], errors='coerce')
Dataframe['expires'].dt.year.value_counts().sort_index().plot(kind='bar', title="Card Expiration Year Distribution")
plt.xlabel("Year of Expiration")
plt.ylabel("Count of Cards")
plt.show()



#Accounts Opened by Year
Dataframe['acct_open_date'] = pd.to_datetime(Dataframe['acct_open_date'], errors='coerce')
Dataframe['acct_open_date'].dt.year.value_counts().sort_index().plot(kind='bar', title="Accounts Opened by Year")
plt.xlabel("Year Account Opened")
plt.ylabel("Count of Accounts")
plt.show()



#Account Age vs Last PIN Change Year
Dataframe['year_pin_last_changed'] = pd.to_datetime(Dataframe['year_pin_last_changed'], errors='coerce').dt.year
Dataframe['account_age'] = pd.to_datetime('today') - Dataframe['acct_open_date']
Dataframe['account_age'] = Dataframe['account_age'].dt.days / 365  # Convert to years

sns.scatterplot(x='account_age', y='year_pin_last_changed', data=Dataframe)
plt.title("Account Age vs Last PIN Change Year")
plt.xlabel("Account Age (Years)")
plt.ylabel("Year PIN Last Changed")
plt.show()
