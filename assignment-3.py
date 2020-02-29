
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
# Install linearmodels: pip3 install linearmodels  plotly  requests PyRTF3
# [probably should just add a read.me and requirements.txt]

#### [1] Read in & setup data
csvFileName = 'sports-and-education.csv'
csvdataRows = readCSV(csvFileName)
csvdataRowsNumericalCategorical = [csvdataRows[0]] + [[float(row[i]) if i in [1,2,5] else int(row[i]) for i in range(len(row))] for row in csvdataRows[1:]]

#### [2] Balance table
treatment_indexes = [i for i in range(len(csvdataRowsNumericalCategorical)) if csvdataRowsNumericalCategorical[i][4] == 1]
control_indexes = [i for i in range(len(csvdataRowsNumericalCategorical)) if csvdataRowsNumericalCategorical[i][4] == 0]
from statistics import mean
treatment_averages = {'Academic.Quality':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Academic.Quality')] for i in treatment_indexes]), 'Athletic.Quality':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Athletic.Quality')] for i in treatment_indexes]), 'Near.Big.Market':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Near.Big.Market')] for i in treatment_indexes])}
# {'Academic.Quality': 0.46648231938015666, 'Athletic.Quality': 0.551013805498369, 'Near.Big.Market': 0.7}
control_averages = {'Academic.Quality':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Academic.Quality')] for i in control_indexes]), 'Athletic.Quality':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Athletic.Quality')] for i in control_indexes]), 'Near.Big.Market':mean([csvdataRowsNumericalCategorical[i][csvdataRowsNumericalCategorical[0].index('Near.Big.Market')] for i in control_indexes])}
# {'Academic.Quality': 0.51531599403359, 'Athletic.Quality': 0.42417061525397, 'Near.Big.Market': 0.36}
import PyRTF
from PyRTF.Renderer import Renderer
from build_table_2 import balance_table
rows = [['Academic.Quality', str(round(control_averages['Academic.Quality'],3)), str(round(treatment_averages['Academic.Quality'],3))], ['Athletic.Quality', str(round(control_averages['Athletic.Quality'],3)), str(round(treatment_averages['Athletic.Quality'],3))], ['Near.Big.Market', str(round(control_averages['Near.Big.Market'],3)), str(round(treatment_averages['Near.Big.Market'],3))]]
number_of_observations_1, number_of_observations_2 = str(len(control_indexes)), str(len(treatment_indexes))
doc = balance_table(rows, number_of_observations_1, number_of_observations_2)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')
DR.Write(doc, OpenFile('balance_table'))

#### [3] Comments on balance table (averages of non-treatment elements)
# If random assignment is truly random, then a balance table for a large enough n should be fairly close in average effect among control and treatment. I believe that the fact that it is not implies that either [a] treatment, control were not randomly assigned (i.e., real life vs. experiment) or [b] this is random chance (very unlikely, especially as n grows). Alternatively, if researchers assigned randomly within a matching scheme, we may not be able to recreate this intra-match randomness without knowning how the researchers created said matches. Finally, perhaps there were many variables that the researchers had, and random assignment actually did a great job at distributing average effect among the majority, but the few we have happened to have a large spread. It is hard to know what the case is if we cannot see the original variables the original researchers had access to.

#### [4] Propensity score model
import statsmodels.api as sm
import pandas as pd
from patsy import dmatrices#will do categorical variables etc. automatically
import numpy as np
# Following https://www.statsmodels.org/dev/gettingstarted.html
dict = {'College.Id':'College_Id', 'Academic.Quality':'Academic_Quality', 'Athletic.Quality':'Athletic_Quality', 'Near.Big.Market':'Near_Big_Market', 'Ranked.2017':'Ranked_2017', 'Alumni.Donations.2018':'Alumni_Donations_2018'}
csvdataRows_ols = [csvdataRows[0]] + [[str(row[0]), float(row[1]), float(row[2]), str(row[3]), int(row[4]), float(row[5])] for row in csvdataRows[1:]]
df = pd.DataFrame(csvdataRows_ols[1:],columns=[dict[element] for element in csvdataRows_ols[0]])
#vars = [dict[element] for element in ['Ranked.2017', 'Academic.Quality', 'Athletic.Quality', 'Near.Big.Market', 'Near.Big.Market']]
#df = df[vars]
y, X = dmatrices('Ranked_2017 ~ Academic_Quality + Athletic_Quality + Near_Big_Market', data=df, return_type='dataframe')
mod = sm.OLS(y, X)
res = mod.fit()
print(res.summary())
#toPredict = {'Intercept':[1.0, 1.0], 'Near_Big_Market[T.1]':[0.0, 0.0], 'Academic_Quality':[0.234, 0.234], 'Athletic_Quality':[0.234, 0.897]}
toPredict = {'Intercept':[1.0 for i in range(len(csvdataRowsNumericalCategorical[1:]))], 'Near_Big_Market[T.1]':[1.0 if i[3]==1 else 0.0 for i in csvdataRowsNumericalCategorical[1:]], 'Academic_Quality':[i[1] for i in csvdataRowsNumericalCategorical[1:]], 'Athletic_Quality':[i[2] for i in csvdataRowsNumericalCategorical[1:]]}
predictions = res.get_prediction(pd.DataFrame(toPredict))
predicted_means = predictions.predicted_mean#https://stackoverflow.com/questions/49476848/read-data-frame-from-get-prediction-function-of-statsmodels-library
#predictions.summary_frame(alpha=0.05)

#### [5] Graph (stacked histograms)
import plotly.graph_objects as go
import numpy as np

control_predictions = [predicted_means[i-1] for i in control_indexes]
treatment_predictions = [predicted_means[i-1] for i in treatment_indexes]

fig = go.Figure()
fig.add_trace(go.Histogram(x=control_predictions, name='control', opacity=0.75))
fig.add_trace(go.Histogram(x=treatment_predictions, name='treatment', opacity=0.75))
fig.update_layout(barmode='overlay')
fig.show()

#### [6] Blocking on propensity score - https://medium.com/@bmiroglio/introducing-the-pymatch-package-6a8c020e2009 (didn't use but looks helpful: https://www.med.uio.no/studier/sensur/euhem-og-hepma/heval5140/2018/heart-propensity-score-matching.pdf)
csvdataRowsNumericalCategorical_with_propensity_scores = [csvdataRowsNumericalCategorical[0]+['Propensity_Score']] + [csvdataRowsNumericalCategorical[1:][i]+[predicted_means[i]] for i in range(len(csvdataRowsNumericalCategorical[1:]))]
csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only = [csvdataRowsNumericalCategorical_with_propensity_scores[0]] + [row for row in csvdataRowsNumericalCategorical_with_propensity_scores[1:] if (row[6] >= 0.15) and (row[6] <= 0.8)]#90 samples

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
data = pd.DataFrame(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[1:], columns=[el.replace('.', '_') for el in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[0]])
treatment = pd.DataFrame([row for row in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[1:] if row[4]==1],  columns=[el.replace('.', '_') for el in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[0]])
control = pd.DataFrame([row for row in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[1:] if row[4]==0], columns=[el.replace('.', '_') for el in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[0]])

def brute_force_sequential_replacement_matching(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only):
    # [0] Separate into treatment and control
    csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_positive = [csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[0]] + [row for row in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[1:] if row[4]==1]
    csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_negative = [csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[0]] + [row for row in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[1:] if row[4]==0]
    # [1] Determine minority (fewer subjects)
    minority = csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_positive[1:] if len(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_positive) < len(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_negative) else csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_negative[1:]
    majority = csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_positive[1:] if len(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_positive) >= len(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_negative) else csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_negative[1:]
    # [2] For each element in minority, find element in majority that best matches it, removing as we find
    minority_index_to_majority_index_match_dict = {i:'' for i in range(len(minority))}#{minority_index:majority_index}
    for i in range(len(minority)):
        best_match_index = 0
        best_match_distance = 1
        # [a] Find best match
        for j in range(len(majority)):
            if (abs(majority[j][6] - minority[i][6]) < best_match_distance) and (j not in list(minority_index_to_majority_index_match_dict.values())):
                best_match_index = j
                best_match_distance = abs(majority[j][6] - minority[i][6])
        # [b] Remove min distance majority element
        minority_index_to_majority_index_match_dict[i] = best_match_index
    # [3] Remove all matches greater than a threshold in distance (say = 0.05)
    minority_index_to_majority_index_match_dict_threshold = {}
    for i in list(minority_index_to_majority_index_match_dict.keys()):
        if (abs(majority[minority_index_to_majority_index_match_dict[i]][6] - minority[i][6]) <= 0.05):
            minority_index_to_majority_index_match_dict_threshold[i] = minority_index_to_majority_index_match_dict[i]
    # [4] Return matches in new column
    csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched = [csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only[0]+['Match']]
    inv_map = {v: k for k, v in minority_index_to_majority_index_match_dict_threshold.items()}
    csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched += [minority[i]+[i] for i in list(minority_index_to_majority_index_match_dict_threshold.keys())]
    csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched += [majority[i]+[inv_map[i]] for i in list(inv_map.keys())]
    #[el for el in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched if el[7] == 29]
    return csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched

#### [7] Model controlling for blocks
import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
df2 = pd.DataFrame(csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched[1:],columns=[element.replace('.', '_') for element in csvdataRowsNumericalCategorical_with_propensity_scores_overlap_only_matched[0]])
FE_ols = sm.ols(formula='Alumni_Donations_2018 ~ Ranked_2017 + C(Match) - 1',data=df2).fit()
#FE_ols = sm.ols(formula="Lung_Hospitalizations ~ C(Vaping_Ban, Treatment(reference='0')) + C(State_Id) + C(Year) - 1",data=df).fit()
print(FE_ols.summary())
# Super correlated - statistically significant at 0.001 and being ranked increases alumni donations by ~$509,000 in 2018 (to be fair this still seems low, but perhaps the time value of money or this is just illustrative)

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

rows_statistical_significance, number_of_observations, r_squared = build_basic_regression_outputs(FE_ols)
rows_of_interest = [rows_statistical_significance[len(rows_statistical_significance)-1]]
rows_of_interest = [[i.replace('_',' ') for i in el]for el in rows_of_interest]

import PyRTF
from PyRTF.Renderer import Renderer
from build_table_2 import basic_table_with_input
dependent_variable_name = 'Alumni Donations 2018'
doc = basic_table_with_input(dependent_variable_name, rows_of_interest, number_of_observations, r_squared)
DR = Renderer()
def OpenFile(name):
    return open('%s.rtf' % name, 'w')
DR.Write(doc, OpenFile('alumni_donations_2018_vs_ranked_2017'))

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
