import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(url)

# Initial exploration
print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nMissing values:\n", df.isnull().sum().sort_values(ascending=False)[:10])
# Filter countries and handle missing values
countries = ['Kenya', 'United States', 'India', 'Brazil', 'Germany']
covid_df = df[df['location'].isin(countries)].copy()

# Convert date column
covid_df['date'] = pd.to_datetime(covid_df['date'])

# Handle missing values
cols_to_fill = ['total_cases', 'total_deaths', 'total_vaccinations']
covid_df[cols_to_fill] = covid_df[cols_to_fill].fillna(0)

# Remove rows with missing dates
covid_df = covid_df.dropna(subset=['date'])
# Time trends for total cases
plt.figure(figsize=(12,6))
sns.lineplot(data=covid_df, x='date', y='total_cases', hue='location')
plt.title('COVID-19 Total Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.show()

# Death rate calculation
covid_df['death_rate'] = (covid_df['total_deaths'] / covid_df['total_cases']).fillna(0)

# Death rate visualization
plt.figure(figsize=(10,6))
sns.barplot(data=covid_df.groupby('location')['death_rate'].max().reset_index(),
            x='location', y='death_rate')
plt.title('Maximum Observed Death Rate by Country')
plt.xticks(rotation=45)
plt.show()
# Vaccination progress
plt.figure(figsize=(12,6))
sns.lineplot(data=covid_df, x='date', y='people_vaccinated_per_hundred', hue='location')
plt.title('Vaccination Progress (% Population)')
plt.xlabel('Date')
plt.ylabel('Vaccinated (%)')
plt.show()
# latest data for mapping
latest_data = df[df['date'] == df['date'].max()]
fig = px.choropleth(latest_data,
                    locations="iso_code",
                    color="total_cases_per_million",
                    hover_name="location",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Global COVID-19 Case Density")
fig.show()