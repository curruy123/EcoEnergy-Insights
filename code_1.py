import pandas as pd
import sqlite3
import numpy as np
from matplotlib import cm
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy.stats as sp 
import stats_tests as sts
import seaborn as sns




feature_columns = ["Country", "Total_Outall", "Avg_Energy_Per_Capita", "Cumulative_co2", "GDP"]
MAX_CLUSTERS = 10
cmap = cm.get_cmap('tab10', MAX_CLUSTERS)


def sk_learn_cluster(X, K):
    """
    Performs k-means clustering using library functions (scikit-learn). You can
    experiment with different initialization settings, but please initialize
    without any optional arguments (other than n_clusters) before submitting.

    :param X: 2D np array containing features of the songs
    :param K: number of clusters
    :return: a tuple of (cluster centroids, indices for each data point)
    """
    kmeans = KMeans(n_clusters=K)
    kmeans.fit(X)
    cluster_indices = kmeans.predict(X)
    centroids = kmeans.cluster_centers_
    return centroids, cluster_indices



def visualize_clusters(data, centroids=None, centroid_indices=None,
                             is_lib_kmean=False):
    """
    Visualizes the song data points and (optionally) the calculated k-means
    cluster centers.
    Points with the same color are considered to be in the same cluster.

    Optionally providing centroid locations and centroid indices will color the
    data points to match their respective cluster and plot the given centroids.
    Otherwise, only the raw data points will be plotted.

    :param data: 2D numpy array of song data
    :param centroids: 2D numpy array of centroid locations
    :param centroid_indices: 1D numpy array of centroid indices for each data point in data
    :return:
    """
    def plot_countries(fig, color_map=None):
        if data.shape[1] == 3:
            x, y, z = np.hsplit(data, 3)
        else:
            x, y, z = data[:, 0], data[:, 6], data[:, 8]
        fig.scatter(x, y, z, c=color_map)

    def plot_clusters(fig):
        if centroids.shape[1] == 3:
            x, y, z = np.hsplit(centroids, 3)
        else:
            x, y, z = centroids[:, 0], centroids[:, 1], centroids[:, 2]
        fig

    plt.clf()
    cluster_plot = centroids is not None and centroid_indices is not None

    ax = plt.figure(num=1).add_subplot(111, projection='3d')
    colors_s = None

    if cluster_plot:
        if max(centroid_indices) + 1 > MAX_CLUSTERS:
            print(f"Error: Too many clusters. Please limit to fewer than {MAX_CLUSTERS}.")
            exit(1)
        colors_s = [cmap(l / MAX_CLUSTERS) for l in centroid_indices]
        plot_clusters(ax)

    plot_countries(ax, colors_s)

    ax.set_xlabel(feature_columns[1])
    ax.set_ylabel(feature_columns[2])
    ax.set_zlabel(feature_columns[3])

    plot_name = "KMeans Clustering Results"

    ax.set_title(plot_name)
    
    # Helps visualize clusters
    plt.gca().invert_xaxis()
    # plt.savefig(output_dir + plot_name + ".png")
    plt.show()


def min_max_scale(data):
    """
    Pre-processes the data by performing MinMax scaling.

    MinMax scaling prevents different scales of the data features from
    influencing distance calculations.

    MinMax scaling is performed by
        X_new = (X - X_min) / (X_max - X_min),

    where X_new is the newly scaled value, X_min is the minimum and X_max is the
    maximum along a single feature column.

    :param data: 2D numpy array of raw data
    :return: preprocessed data
    """
    min_vals = data.min(axis=0)
    max_vals = data.max(axis=0)
    return (data - min_vals) / (max_vals - min_vals)


def drop_incomplete_rows(df):
    """
    Input:
        - df: Pandas DataFrame
    Output:
        - a Pandas DataFrame where all rows no longer
        contain null values or empty strings
    """
    columns = df.columns
    def row_complete(row):
        for col in columns:
            val = row[col]
            nan = pd.isnull(val)
            str_empty = type(val) == str and val.strip() == ""
            if nan or str_empty:
                return False
        return True
    return df[df.apply(lambda x: row_complete(x), axis=1)]



def cluster_countries(country_data, max_iters = 300):

    

    centroids_sklearn = None
    idx_sklearn = None
    numerical_data = country_data.drop(columns=['Country'])
    numerical_data = drop_incomplete_rows(numerical_data)
    numerical_data_array = numerical_data.to_numpy()
    scaled_data = min_max_scale(numerical_data_array)

    distortions = []
    K = range(1, 10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k,n_init=1)
        kmeanModel.fit(scaled_data)
        distortions.append(kmeanModel.inertia_)

    plt.figure(figsize=(16,8))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('Optimal k')
    plt.show()

    visualize_clusters(scaled_data)

    centroids_sklearn, idx_sklearn = sk_learn_cluster(scaled_data, 3)

    visualize_clusters(scaled_data,centroids_sklearn,idx_sklearn)

    return centroids_sklearn, idx_sklearn


    

# ------------------------------------------------------------------------------------------------

# ALL FUNCTIONS USED FOR VISUALIZING DATA VIA K-MEANS AND CLEANING

#reads the excel sheet in the wide format - this is the international tfp production of agriculture from 1961-2021
tfp_df = pd.read_excel('data/AgTFPInternational2021_long.xlsx', sheet_name= 'Wide format data')
tfp_df = drop_incomplete_rows(tfp_df)
co2_df = pd.read_csv('data/owid-co2-data.csv')
energy_df = pd.read_csv('data/owid-energy-data.csv')


tfp_df = tfp_df.rename(columns={'Country/territory': 'Country'})
energy_df = energy_df.rename(columns={'country': 'Country'})
co2_df = co2_df.rename(columns={'country': 'Country'})



# cleaning 
# CWANA = North Africa, Central Asia, West Asia
# Sort it out through sub regions via key words 'Asia' and 'AFRICA'
# Filters out data from CWANA to get information from Africa and Asia 
tfp_df.loc[tfp_df['Region'].isin(['SSA']), 'Region'] = 'AFRICA'
tfp_df.loc[tfp_df['Sub-Region'].str.contains('Asia'), 'Region'] = 'ASIA'
tfp_df.loc[tfp_df['Sub-Region'].str.contains('Africa'), 'Region'] = 'AFRICA'
tfp_df['Country'] = tfp_df['Country'].str.upper()
# we do not need this data
tfp_df = tfp_df.loc[tfp_df['Region'] != 'Former Soviet Union']


# we are only looking at data from 1993-2021

co2_df['Country'] = co2_df['Country'].str.upper()
co2_df = co2_df[['Country','year','energy_per_capita', 'cumulative_co2']]
co2_df = co2_df.loc[co2_df['year'] >= 1993]
co2_df = co2_df.loc[co2_df['year'] <= 2021]
co2_df = drop_incomplete_rows(co2_df)



# rename the tables to all contain the same 'Country' column, and also make them uniform in style

# keep countries/rows that are only present in the TFP table
energy_df['Country'] = energy_df['Country'].str.upper() 
co2_df = co2_df[co2_df['Country'].isin(tfp_df['Country'])]
energy_df = energy_df[energy_df['Country'].isin(tfp_df['Country'])]


# make all continent data uniform 

energy_df = energy_df[['Country','year','fossil_fuel_consumption', 'gdp', 'energy_per_capita']]
energy_df = energy_df.loc[energy_df['year'] >= 1993]
energy_df = energy_df.loc[energy_df['year'] <= 2021]





# creates a connection to a database for the tfp data for when  we need to query

conn = sqlite3.connect('data.db')
c = conn.cursor()
tfp_df.to_sql('tfp_table', con=conn, if_exists='replace', index=False)
co2_df.to_sql('co2_table',  con=conn, if_exists='replace', index=False)
energy_df.to_sql('energy_table',  con=conn, if_exists='replace', index=False)

# ALL CODE ABOVE THIS LINE IS FOR CLEANING


country_to_year = '''SELECT 
    Country AS Country,
    Year,
    SUM(Outall_Index) AS Total_Outall
FROM tfp_table
WHERE Year BETWEEN 1993 AND 2021
GROUP BY Country, Year;'''

c.execute(country_to_year)
cont_to_year_query = c.fetchall()
country_to_year_df = pd.DataFrame(cont_to_year_query,columns = ['Country','Year','Total_Outall'])

country_summary = '''SELECT 
    tfp_table.Country,
    SUM(tfp_table.Sum_Total_Outall) AS Total_Outall,
    AVG(tfp_table.Avg_TFP_Index) AS Avg_TFP_Index,
    AVG(tfp_table.Avg_Land_Index) AS Avg_Land_Index,
    AVG(tfp_table.Avg_Labor_Index) AS Avg_Labor_Index,
    AVG(tfp_table.Avg_Capital_Index) AS Avg_Capital_Index,
    AVG(tfp_table.Avg_Materials_Index) AS Avg_Materials_Index,
    AVG(CO2.energy_per_capita) AS Avg_Energy_Per_Capita,
    SUM(Energy.gdp) AS Total_GDP,
    SUM(CO2.cumulative_co2) AS Total_Cumulative_CO2
FROM (
    SELECT 
        Country,
        Year,
        AVG(TFP_Index) AS Avg_TFP_Index,
        SUM(Outall_Index) AS Sum_Total_Outall,
        AVG(Land_Index) AS Avg_Land_Index,
        AVG(Labor_Index) AS Avg_Labor_Index,
        AVG(Capital_Index) AS Avg_Capital_Index,
        AVG(Materials_Index) AS Avg_Materials_Index
    FROM tfp_table
    WHERE Year BETWEEN 1993 AND 2021
    GROUP BY Country, Year
) AS tfp_table
LEFT JOIN co2_table CO2 ON tfp_table.Country = CO2.Country AND tfp_table.Year = CO2.Year
LEFT JOIN energy_table Energy ON tfp_table.Country = Energy.Country AND tfp_table.Year = Energy.Year
GROUP BY tfp_table.Country
ORDER BY tfp_table.Country;'''

c.execute(country_summary)
summary_query = c.fetchall()
summary_df = pd.DataFrame(summary_query,columns = ['Country','Total_Outall','Avg_TFP_Index','Avg_Land_Index',
                                                   ' Avg_Labor_Index',' Avg_Capital_Index', 'Avg_Materials_Index',
                                                   'Avg_Energy_Per_Capita','GDP','Cumulative_CO2'])
print(summary_df)


correlation_query = '''SELECT 
    tfp_table.Country,
    tfp_table.Year,
    tfp_table.Total_Outall,
    tfp_table.TFP_Index,
    tfp_table.Land_Index,
    tfp_table.Labor_Index,
    tfp_table.Capital_Index,
    tfp_table.Materials_Index,
    CO2.energy_per_capita,
    Energy.gdp,
    CO2.cumulative_co2
FROM (
    SELECT 
        Country,
        Year,
        TFP_Index AS TFP_Index,
        Outall_Index AS Total_Outall,
        Land_Index AS Land_Index,
        Labor_Index AS Labor_Index,
        Capital_Index AS Capital_Index,
        Materials_Index AS Materials_Index
    FROM tfp_table
    WHERE Year BETWEEN 1993 AND 2021
) AS tfp_table
LEFT JOIN co2_table CO2 ON tfp_table.Country = CO2.Country AND tfp_table.Year = CO2.Year
LEFT JOIN energy_table Energy ON tfp_table.Country = Energy.Country AND tfp_table.Year = Energy.Year
ORDER BY tfp_table.Country, tfp_table.Year;'''

c.execute(correlation_query)
correlate_query = c.fetchall()
correlation_df = pd.DataFrame(correlate_query,columns = ['Country','Year','Total_Outall','TFP_Index','Land_Index',
                                                   'Labor_Index','Capital_Index', 'Materials_Index',
                                                   'Energy_Per_Capita','GDP','Cumulative_CO2'])


c.close()
conn.close
# ---------------------------------------------------------------------------------------------------------------
# Stats TESTS DONE HERE: 
#Paired T Test for Hypothesis 1:
tfp_data_10 = country_to_year_df.loc[country_to_year_df['Year'] == 2010][['Country','Total_Outall']]
tfp_data_21 = country_to_year_df.loc[country_to_year_df['Year'] == 2021][['Country','Total_Outall']]


# to make sure the length of both datasets are the same. contexualize the fact we may have
# countries whos data is undocumented for certain years. 3 countries were removed
tfp_data_21 = tfp_data_21[tfp_data_21['Country'].isin(tfp_data_10['Country'])]


sts.paired_ttest(tfp_data_10['Total_Outall'],tfp_data_21['Total_Outall'])

# Two Sample T-Test for Hypothesis 2:
us_energy_yearly = energy_df.loc[energy_df['Country'] == 'UNITED STATES'][['Country','energy_per_capita']]
china_energy_yearly = energy_df.loc[energy_df['Country'] == 'CHINA'][['Country','energy_per_capita']]


sts.two_sample_ttest(us_energy_yearly['energy_per_capita'],china_energy_yearly['energy_per_capita'])

#Paired T Test for Hypothesis 3:
co2_data_18 = co2_df.loc[co2_df['year'] == 2018]
co2_data_21 = co2_df.loc[co2_df['year'] == 2021]

# to make sure the length of both datasets are the same. contexualize the fact we may have
# countries whos data is undocumented for certain years. 1 country removed
co2_data_21 = co2_data_21[co2_data_21['Country'].isin(co2_data_18['Country'])]


sts.paired_ttest(co2_data_18['cumulative_co2'],co2_data_21['cumulative_co2'])

# ---------------------------------------------------------------------------------------------------------------
# Machine Learning:

# 1. KMEANS
cluster_countries(summary_df, max_iters=300)
# 2. Linear Regression
regression_df = drop_incomplete_rows(summary_df)
# contexualize undocumented countries cumulative CO2
regression_df = regression_df.dropna(subset=['Total_Outall', 'Cumulative_CO2'])
print(regression_df[:10])
sts.regression(regression_df['Cumulative_CO2'],regression_df['Total_Outall'])


def plot_correllogram():
    
    # Plot
    plt.figure(figsize=(12,10), dpi= 80)
    df = correlation_df[['Total_Outall','TFP_Index','Land_Index',
                                                   'Labor_Index','Capital_Index', 'Materials_Index',
                                                   'Energy_Per_Capita','GDP','Cumulative_CO2']]
    sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True, annot_kws={"size":9})

    # Decorations
    plt.title('Correlogram of Country Variables', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()

# Visualization 1 for Data:
plot_correllogram()




