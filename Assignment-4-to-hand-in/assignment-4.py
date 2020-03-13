
#### [0] Environment setup
# Set up virtual environment: virtualenv -p python3 venv3
# Turn on virtual environment: source venv3/bin/activate
# Clone data: git clone https://github.com/bocowgill-collaborations/ResearchMethods-Repository.git
'''
import csv
import requests

url = 'https://raw.githubusercontent.com/bocowgill-collaborations/ResearchMethods-Repository/master/HW3/sports-and-education.csv'
with requests.Session() as s:
    download = s.get(url)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    csv_data_rows = list(cr)
    for row in csv_data_rows:
        print(row)
writeToCSV('sports-and-education.csv', csv_data_rows)
'''
# Install linearmodels: pip3 install linearmodels  plotly  requests PyRTF3 pandas
# [probably should just add a read.me and requirements.txt]

#### [1] Read in & setup data
csvFileName = 'crime-iv.csv'
csvdataRows = readCSV(csvFileName)
import pandas as pd
csvdataRowsNumericalCategorical = [[el.replace('.','_') for el in csvdataRows[0]]] + [[str(row[0]), int(row[1]), int(row[2]), float(row[3]), int(row[4])] for row in csvdataRows[1:]]
df = pd.DataFrame(csvdataRowsNumericalCategorical[1:],columns=csvdataRowsNumericalCategorical[0])

#### [4] Balance table - republican vs. democratic judge and underling statistics
republican_indexes = [i for i in range(len(csvdataRowsNumericalCategorical)) if csvdataRowsNumericalCategorical[i][1] == 1]
democrat_indexes = [i for i in range(len(csvdataRowsNumericalCategorical)) if csvdataRowsNumericalCategorical[i][1] == 0]
from statistics import mean
republican__averages = {'Severity_Of_Crime':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Severity_Of_Crime')] for i in republican_indexes]), 'Months_In_Jail':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Months_In_Jail')] for i in republican_indexes]), 'Recidivates':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Recidivates')] for i in republican_indexes])}
# {'Severity_Of_Crime': 1.9658119658119657, 'Months_In_Jail': 19.428749028749028, 'Recidivates': 0.39937839937839936}
democrat_averages = {'Severity_Of_Crime':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Severity_Of_Crime')] for i in democrat_indexes]), 'Months_In_Jail':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Months_In_Jail')] for i in democrat_indexes]), 'Recidivates':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Recidivates')] for i in democrat_indexes])}
# {'Severity_Of_Crime': 1.9793899422918384, 'Months_In_Jail': 16.453297609233307, 'Recidivates': 0.25927452596867273}
import PyRTF
from PyRTF.Renderer import Renderer
from build_table_2 import balance_table
rows = [['Severity_Of_Crime', str(round(republican__averages['Severity_Of_Crime'],3)), str(round(democrat_averages['Severity_Of_Crime'],3))], ['Months_In_Jail', str(round(republican__averages['Months_In_Jail'],3)), str(round(democrat_averages['Months_In_Jail'],3))], ['Recidivates', str(round(republican__averages['Recidivates'],3)), str(round(democrat_averages['Recidivates'],3))]]
number_of_observations_1, number_of_observations_2 = str(len(republican_indexes)), str(len(democrat_indexes))
doc = balance_table(rows, number_of_observations_1, number_of_observations_2)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')
DR.Write(doc, OpenFile('balance_table'))

#### [5] First stage (Z --> X, w/controls) | (judge assignment --> # months in jail, w/controls=[severity of crime])
import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
#df2 = pd.DataFrame(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched[1:],columns=[element.replace('.', '_') for element in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched[0]])
first_stage_ols = sm.ols(formula='Months_In_Jail ~ Republican_Judge + C(Severity_Of_Crime)',data=df).fit()
first_stage_ols.summary()

rows_statistical_significance, number_of_observations, r_squared = build_basic_regression_outputs(first_stage_ols)
rows_statistical_significance = [rows_statistical_significance[len(rows_statistical_significance)-1]] + rows_statistical_significance[1:len(rows_statistical_significance)-1]
rows_of_interest = [[i.replace('_',' ') for i in el]for el in rows_statistical_significance]
import PyRTF
from PyRTF.Renderer import Renderer
from build_table_2 import basic_table_with_input
dependent_variable_name = 'Months in jail'
doc = basic_table_with_input(dependent_variable_name, rows_of_interest, number_of_observations, r_squared)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')
DR.Write(doc, OpenFile('months_in_jail_vs_republican_judge_first_stage'))

#### [7] Reduced form (Z --> Y, w/controls) | (judge assignment --> recidivism, w/controls=[severity of crime])
reduced_form_ols = sm.ols(formula='Recidivates ~ Republican_Judge + C(Severity_Of_Crime)',data=df).fit()
reduced_form_ols.summary()

rows_statistical_significance, number_of_observations, r_squared = build_basic_regression_outputs(reduced_form_ols)
rows_statistical_significance = [rows_statistical_significance[len(rows_statistical_significance)-1]] + rows_statistical_significance[1:len(rows_statistical_significance)-1]
rows_of_interest = [[i.replace('_',' ') for i in el]for el in rows_statistical_significance]
import PyRTF
from PyRTF.Renderer import Renderer
from build_table_2 import basic_table_with_input
dependent_variable_name = 'Recidivates'
doc = basic_table_with_input(dependent_variable_name, rows_of_interest, number_of_observations, r_squared)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')
DR.Write(doc, OpenFile('recidivates_vs_republican_judge_reduced_form'))

#### [9] IV / 2SLS (Two stage least squares)
import numpy as np
from linearmodels.iv import IV2SLS
# [Attempt 1 - https://bashtage.github.io/linearmodels/doc/iv/introduction.html (DID NOT WORK)]
#dependent = df.Recidivates# o/y (dependent variable)
#exog = df.Severity_Of_Crime# controls
#endog = df.Months_In_Jail# x (independent variable)
#instruments = df.Republican_Judge# z (instrumental variable)
#mod = IV2SLS(dependent, exog, endog, instruments)
#res = mod.fit(cov_type='unadjusted')
#res
# [Attempt 2 - https://bashtage.github.io/linearmodels/doc/iv/methods.html (WORKED/SUCCESS!!)]
#
#mod = IV2SLS.from_formula('dependent_variable ~ C(control_variable) + [independent_variable ~ instrumental_variable]', data=df)
mod = IV2SLS.from_formula('Recidivates ~ C(Severity_Of_Crime) + [Months_In_Jail ~ Republican_Judge]', data=df)
res = mod.fit()
res
rows_statistical_significance, number_of_observations, r_squared = build_basic_regression_outputs_linear_models(res)
rows_statistical_significance = [rows_statistical_significance[len(rows_statistical_significance)-1]] + rows_statistical_significance[1:len(rows_statistical_significance)-1]
rows_of_interest = [[i.replace('_',' ') for i in el]for el in rows_statistical_significance]

import PyRTF
from PyRTF.Renderer import Renderer
from build_table_2 import basic_table_with_input
dependent_variable_name = 'Recidivates'
doc = basic_table_with_input(dependent_variable_name, rows_of_interest, number_of_observations, r_squared)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')
DR.Write(doc, OpenFile('recidivates_vs_months_in_jail_2SLS'))

#### [13] Monotonicity assumption and the possibility of "defiers"
len([row for row in csvdataRowsNumericalCategorical[1:] if row[3] == 0.0 and row[4] == 1])
# 212
monotonicity_assumption_ols = sm.ols(formula='Recidivates ~ Months_In_Jail + C(Severity_Of_Crime)',data=df).fit()
monotonicity_assumption_ols.summary()




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

# Only difference is standard error as .std_errors vs. .bse - should change one function to do both, not two separate functions - tbd
def build_basic_regression_outputs_linear_models(res):
    number_of_observations = str(int(res.nobs))
    r_squared = str(round(res.rsquared,3))
    variables = [key for key,value in res.params.iteritems()]
    coefficients = res.params
    standard_error = res.std_errors#different
    p_values = res.pvalues
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
