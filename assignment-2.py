
#### [0] Environment setup
# Set up virtual environment: virtualenv -p python3 venv3
# Turn on virtual environment: source venv3/bin/activate
# Clone data: git clone https://github.com/bocowgill-collaborations/ResearchMethods-Repository.git
# Install linearmodels: pip3 install linearmodels, plotly
# [probably should just add a read.me and requirements.txt]

#### [1] Read in & setup data
csvFileName = 'ResearchMethods-Repository/HW2/vaping-ban-panel.csv'
csvdataRows = readCSV(csvFileName)
csvdataRowsNumericalCategorical = [csvdataRows[0]] + [[int(row[i]) if i in [1,3] else row[i] for i in range(len(row))] for row in csvdataRows[1:]]
import numpy as np
import pandas as pd
dict = {'State.Id':'State_Id', 'Year':'Year', 'Vaping.Ban':'Vaping_Ban', 'Lung.Hospitalizations':'Lung_Hospitalizations'}
df = pd.DataFrame(csvdataRowsNumericalCategorical[1:],columns=[dict[element] for element in csvdataRowsNumericalCategorical[0]])

#### [2] Regression to evaluate the "parallel trends" requirement of a difference-in-difference("DnD") estimate
## [a] Separate out states that eventually ban and states that never ban
years = list(set(row[csvdataRowsNumericalCategorical[0].index('Year')] for row in csvdataRowsNumericalCategorical[1:]))
states_that_ban = list(set([row[0] for row in csvdataRowsNumericalCategorical[1:] if row[csvdataRowsNumericalCategorical[0].index('Vaping.Ban')] == '1']))
states_that_dont_ban = list(set([row[0] for row in csvdataRowsNumericalCategorical[1:]]) - set(states_that_ban))
from statistics import mean
average_lung_hospitalizations_by_year_with_ban_dict = {year:mean([row[csvdataRowsNumericalCategorical[0].index('Lung.Hospitalizations')] for row in csvdataRowsNumericalCategorical[1:] if row[csvdataRowsNumericalCategorical[0].index('State.Id')] in states_that_ban and row[csvdataRowsNumericalCategorical[0].index('Year')]==year]) for year in years}
average_lung_hospitalizations_by_year_no_ban_dict = {year:mean([row[csvdataRowsNumericalCategorical[0].index('Lung.Hospitalizations')] for row in csvdataRowsNumericalCategorical[1:] if row[csvdataRowsNumericalCategorical[0].index('State.Id')] in states_that_dont_ban and row[csvdataRowsNumericalCategorical[0].index('Year')]==year]) for year in years}
average_lung_hospitalizations = [[year, average_lung_hospitalizations_by_year_with_ban_dict[year], 1] for year in years] + [[year, average_lung_hospitalizations_by_year_no_ban_dict[year], 0] for year in years]
df2 = pd.DataFrame(average_lung_hospitalizations, columns=['Year', 'Average_lung_hospitalizations', 'Implement_ban'])
## [b] Regress average_lung_hospitalizations for years
average_lung_hospitalizations_states_with_ban_pre_ban_years = [row for row in average_lung_hospitalizations if row[0] < 2021 and row[2] == 1]
average_lung_hospitalizations_states_without_ban_pre_ban_years = [row for row in average_lung_hospitalizations if row[0] < 2021 and row[2] == 0]
df3 = pd.DataFrame(average_lung_hospitalizations_states_with_ban_pre_ban_years, columns = ['Year', 'Average_lung_hospitalizations', 'Implement_ban'])
df4 = pd.DataFrame(average_lung_hospitalizations_states_without_ban_pre_ban_years, columns = ['Year', 'Average_lung_hospitalizations', 'Implement_ban'])
import statsmodels.formula.api as sm
FE_ols_ban = sm.ols(formula='Average_lung_hospitalizations ~ Year - 1',data=df3).fit()
print(FE_ols_ban.summary())#coefficient = 55.5853
FE_ols_no_ban = sm.ols(formula='Average_lung_hospitalizations ~ Year - 1',data=df4).fit()
print(FE_ols_no_ban.summary())#coefficient = 56.7940
# Coefficients very close, looks good re parallel


#### Confirmation that this is the same as categorical variables in OLS
#FE_ols = sm.ols(formula='Lung_Hospitalizations ~ Vaping_Ban + C(Year) - 1',data=df).fit()#YES - same R^2, coefficients etc. as run in R
#print(FE_ols.summary())

#### [3] Create the canonical DnD line graph (average_lung_hospitalizations(states no ban) vs. average_lung_hospitalizations(states with ban) x year)
# Examples - https://plot.ly/python/plotly-express/
import plotly.express as px
fig = px.scatter(df2, x="Year", y="Average_lung_hospitalizations", color="Implement_ban", color_continuous_scale='Bluered_r')
fig.show()

#### [4] Fixed effects in statsmodels
# Example - http://aeturrell.com/2018/02/20/econometrics-in-python-partII-fixed-effects/
import statsmodels.formula.api as sm
# Changing vaping_ban to a numerical variable allows us to get its average_effect holding state and year constant in the regression output table (last row)
csvdataRowsNumericalCategorical2 = [csvdataRows[0]] + [[int(row[i]) if i in [1,2,3] else row[i] for i in range(len(row))] for row in csvdataRows[1:]]
df2 = pd.DataFrame(csvdataRowsNumericalCategorical2[1:],columns=[dict[element] for element in csvdataRowsNumericalCategorical2[0]])
FE_ols = sm.ols(formula='Lung_Hospitalizations ~ Vaping_Ban + C(State_Id) + C(Year) - 1',data=df2).fit()
#FE_ols = sm.ols(formula="Lung_Hospitalizations ~ C(Vaping_Ban, Treatment(reference='0')) + C(State_Id) + C(Year) - 1",data=df).fit()
print(FE_ols.summary())

def build_basic_regression_outputs(OLSResults):
    # How to get model attributes - https://stackoverflow.com/questions/48522609/retrieve-model-estimates-from-statsmodels
    number_of_observations = str(int(OLSResults.nobs))
    r_squared = str(round(OLSResults.rsquared,3))
    variables = [key for key,value in OLSResults.params.iteritems()]
    coefficients = OLSResults.params
    standard_error = OLSResults.bse
    p_values = OLSResults.pvalues
    rows = [[variables[i], coefficients[i], standard_error[i], p_values[i]] for i in range(len(coefficients))]
    def statistical_significance_ify(coefficient, p_value):
        if p_value < 0.01:
            return str(round(coefficient,3))+'***'
        elif p_value < 0.05:
            return str(round(coefficient,3))+'**'
        elif p_value < 0.1:
            return str(round(coefficient,3))+'*'
        else:
            return str(round(coefficient,3))
    rows_statistical_significance = [[row[0], statistical_significance_ify(row[1], row[3]), '('+str(round(row[2],3))+')'] for row in rows]
    return rows_statistical_significance, number_of_observations, r_squared

#### [5] Build table + save in word/rtf
import PyRTF
#from PyRTF.Elements import Document
from PyRTF.Renderer import Renderer
#from build_table import build_table_3
from build_table import basic_table_with_input
#doc3 = build_table_3()
dependent_variable_name = 'Lung hospitalizations'
rows_statistical_significance, number_of_observations, r_squared = build_basic_regression_outputs(FE_ols)
doc = basic_table_with_input(dependent_variable_name, rows_statistical_significance, number_of_observations, r_squared)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')

#DR.Write(doc, OpenFile('10'))

# [Save #2]
dependent_variable_name_1 = 'Average lung hospitalizations - states that ban in 2021'
dependent_variable_name_2 = 'Average lung hospitalizations - states that never ban'
independent_variable_name = 'Year'
rows_statistical_significance_1, number_of_observations_1, r_squared_1 = build_basic_regression_outputs(FE_ols_ban)
rows_statistical_significance_2, number_of_observations_2, r_squared_2 = build_basic_regression_outputs(FE_ols_no_ban)
doc = basic_table_two_columnsbasic_table_two_columns(dependent_variable_name_1, dependent_variable_name_2, independent_variable_name, rows_statistical_significance_1, number_of_observations_1, r_squared_1, rows_statistical_significance_2, number_of_observations_2, r_squared_2)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')

DR.Write(doc, OpenFile('11'))



#### [6] Answer questions
## [a] How many state-level fixed effects are there?
## 49
## [b] What is the interpretation of the coefficient for each state-level fixed effect?
## Moving from the base case (state 1?) to that given state, the average lung_Hospitalizations increases by the given state's coefficient (e.g., moving from state 1 to state 2 the average lung hopsitalizations increases by ~633)
## [c] Can you reject the hypothesis that state fixed effects are all zero?
## No (technically depends on what confidence you desire, but at 0.05, from the base case no for State 2 and State 3)


#### NEXT STEPS ####
## [a] Standardize basic_table for any number of columns/rows (write a function that dynamically creates appropriate setup)
## [b] Clean up formatting (font, sizes, superscript, etc.)


################ Background functions ################
def readCSV(csvFileName):
    import csv, sys
    csvdataRows = []
    with open(csvFileName) as csvfile:
        spamreader = csv.reader(csvfile)
        #for line in data:
        for row in spamreader:
            csvdataRows.append(row)
    ## Return rows #
    return csvdataRows

def writeToCSV(csvFileName, csvdataRows):
    import csv, sys
    if sys.version_info >= (3,0,0):
        csvfile = open(csvFileName, 'w', newline='')
    else:
        csvfile = open(csvFileName, 'wb')
    spamwriter = csv.writer(csvfile)
    for row in csvdataRows:
        try:
            spamwriter.writerow(row)
        except:
            print("Failed at " + str(row))
    return
