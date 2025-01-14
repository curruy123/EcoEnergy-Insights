import numpy as np
import pandas as pd
import random
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel, chi2_contingency
import statsmodels.api as sm
from statsmodels.tools import eval_measures
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

RANDOM_SEED = 0
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def train_test_split(df, train_pct=0.75):
    """
    Input:
        - df: Pandas DataFrame
        - train_pct: optional, float
    Output:
        - train dataframe: Pandas DataFrame
        - test dataframe: Pandas DataFrame
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    msk = np.random.rand(len(df)) < train_pct
    return df[msk], df[~msk]

def regression(X, Y):
    """
    Implement Linear Regression using StatsModel.
    inputs:
        - X: a numpy array containing all the X values
        - Y: a numpy array containing all the Y values
    
    outputs:
        - mse_train: the mean-squared error of the model (trained on the training
                    data), evaluated on the training dataset (float)
        - mse_test: the mean-squared error of the model (trained on the training
                    data), evaluated on the testing dataset (float)
        - rsquared_val: the r-squared value of the model (trained on the training
                    data), evaluated on the testing dataset (float)
    """
    df = pd.DataFrame({'X': X, 'Y': Y})
    
    # Split the data into training and testing sets
    df_training, df_test = train_test_split(df)

    X_train = sm.add_constant(df_training['X'])
    Y_train = df_training['Y']
    X_test = sm.add_constant(df_test['X'])
    Y_test = df_test['Y']

    # Fit a linear regression model to the training dataset
    model = sm.RLM(Y_train, X_train).fit()

    Y_train_pred = model.predict(X_train)
    Y_test_pred = model.predict(X_test)

    

    # Calculate Mean-squared Error and R-squared value
    mse_train = eval_measures.mse(Y_train, Y_train_pred)
    mse_test = eval_measures.mse(Y_test, Y_test_pred)
    rsquared_val = r2_score(Y_test, Y_test_pred)

    plt.scatter(X_test.iloc[:, 1], Y_test, color='black') 
    plt.title("Regression on Cumulative CO2 and Total Agriculture Output")
    plt.ylabel("Total Agriculture Output Index")
    plt.xlabel("Cumulative CO2")
    plt.plot(X_test.iloc[:, 1], Y_test_pred, color='blue', linewidth=2)

    plt.show() # ensure to plot without the constant)
    print(model.summary())

    return mse_train, mse_test, rsquared_val



def one_sample_ttest(values, population_mean):
    # to get the t-statistic and the p-value.
     tstats, pvalue = ttest_1samp(values,population_mean)


    # prints out t-statistic and values
     print(f"One Sample T Statistic:{tstats}")
     print(f"One Sample P Value:{pvalue}")
    
    
    # and then we'll return tstats and pvalue
     return tstats, pvalue


def two_sample_ttest(values_a, values_b):
     tstats, pvalue = ttest_ind(values_a,values_b)

    

    # prints out t-statistic and values
     print(f"Two Sample T Statistic:{tstats}")
     print(f"Two Sample P Value:{pvalue}")
     
    
    # and then we'll return tstats and pvalue
     return tstats, pvalue


def paired_ttest(values_a, values_b):
     tstats, pvalue = ttest_rel(values_a,values_b)


    # prints out t-statistic and values
     print(f"Paired T Statistic:{tstats}")
     print(f"Paired T P Value:{pvalue}")
     

    # and then we'll return tstats and pvalue
     return tstats, pvalue


def chisquared_independence_test(df, column_a_name, column_b_name):
    ## Stencil: Error check input - do not modify this part
    assert all_variable_names_in_df([column_a_name, column_b_name], df)

    # a cross table between the two columns a and b
    cross_table =  pd.crosstab(df[column_a_name],df[column_b_name])
    print(cross_table)
    tstats, pvalue, degrees_of_freedom, expected = chi2_contingency(cross_table)

     # prints out t-statistic and values
    print(f"Chi Squared T Statistic:{tstats}")
    print(f"Chi Squared P Value:{pvalue}")
     

    # and then we'll return tstats and pvalue
    return tstats, pvalue
