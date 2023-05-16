# Diss_Detecting_Provider_Bias
This code repository consists of analytic software related to Drew Walker's doctoral dissertation, "Using natural language processing to detect stigmatizing provider language and evaluate associations with opioid analgesic pain management outcomes". 


The repository will be organized according to the following outline:

# Aim 1 
Develop, test, and evaluate an ensemble of natural language processing models built to detect the presence of biased linguistic features in clinical charts for patients with chronic illnesses.

## Doubt Markers
1. Data Prep
2. Annotation
3. Model Training
## Scare Quotes
1. Data Prep
2. Annotation
3. Model Training
## Stigmatizing Labels 
1. Data Prep
2. Annotation
3. Model Training
# Aim 2
Assess distribution and growth of detected provider bias in clinical notes as it is clustered across levels of temporality, patient, provider, and admission levels across disease populations and demographic variables.

1. Predictions from model on entire dataset
2. Transforming any data to patient/note level from sentence level  
3. EDA on Linguistic Bias Distributions
4. Multilevel Models  

# Aim 3
Assess the relationships between detected provider bias and patient care outcomes of opioid analgesic prescription rates, and self-directed discharge across disease population and demographic variables.

1. Data wrangling/transformations-- patient level outcomes of daily avg opioid analgesic prescription rate, experience of self-directed discharge
2. EDA on Opioid prescriptions, self-directed discharge 
3. Patient-level generalized linear models 

# MIMIC-III Data
Not included in GitHub, this folder hosts the .csv.gz files hosted on Physionet. 
