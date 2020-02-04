/* Type these commands to install the "estout" package: 

ssc install estout

Also: Note you can type help [command] into Stata to get help on any command. 
*/


// NOTES TO SELF
//ls = pwd, cd = cd
//clear gets rid of data in local storage
//data button in stata helpful to see a visual representation (similar to excel)




* Read in data: 
//insheet using Ai-Experiment-Data.csv, comma names clear
//insheet using ResearchMethods-Repository/ModelAssignment/Ai-Experiment-Data.csv, comma names clear
//insheet using ResearchMethods-Repository/HW1/assignment1-research-methods.csv
import delimited using ResearchMethods-Repository/HW1/assignment1-research-methods

* Label your variables
//label variable readethicsarticle "Read Ethics Article"
//label variable recommendsaiadoption "Recommends AI"
label variable candidateid "Candidate ID"
label variable calledback "Called back"
label variable recruiteriswhite "Recruiter is white"
label variable recruiterismale "Recruiter is male"
// Despite uppercase in .csv, variables referenced as lowercase
label variable malecandidate "Male candidate"
label variable eliteschoolcandidate "Elite school candidate"
label variable bigcompanycandidate "Big company candidate"


* Run regression: 
//reg recommendsaiadoption readethicsarticle
reg calledback eliteschoolcandidate

* Store regression
eststo regression_one 

**********************************
* FOR PEOPLE USING LaTeX: 
* Create output options. The below defaults are common and can be customized. 
//global tableoptions "bf(%15.2gc) sfmt(%15.2gc) prehead(\begin{tabular}{l*{14}{c}}) postfoot(\end{tabular}) se label noisily noeqlines nonumbers varlabels(_cons Constant, end("" ) nolast)  starlevels(* 0.1 ** 0.05 *** 0.01) replace r2"
//esttab regression_one using Ai-Experiment-Table.tex, $tableoptions keep(readethicsarticle) 


**********************************
* FOR PEOPLE USING MICROSOFT (AKA "WORD"):
global tableoptions "bf(%15.2gc) sfmt(%15.2gc) se label noisily noeqlines nonumbers varlabels(_cons Constant, end("" ) nolast)  starlevels(* 0.1 ** 0.05 *** 0.01) replace r2"
esttab regression_one using Candidate-call-back-table.rtf, $tableoptions keep(eliteschoolcandidate)

//2+ variables? (regression works, table syntax in the future...)
//reg calledback eliteschoolcandidate malecandidate bigcompanycandidate
//eststo regression_two 
//global tableoptions "bf(%15.2gc) sfmt(%15.2gc) se label noisily noeqlines nonumbers varlabels(_cons Constant, end("" ) nolast)  starlevels(* 0.1 ** 0.05 *** 0.01) replace r2"
//esttab regression_two using Candidate-call-back-table-multiple-iv.rtf, $tableoptions keep(eliteschoolcandidate malecandidate bigcompanycandidate)



