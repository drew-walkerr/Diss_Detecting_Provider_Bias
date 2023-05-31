import sklearn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import os
import re
import sys
import scipy

# ICDs is a table of all the patients and their assigned ICD-9 codes. Seq number is the number in which its listed in the chart-- need to investigate this
ICDs = pd.read_csv(r"\Users\awalk55\OneDrive - Emory University\Desktop\Diss_Detecting_Provider_Bias\MIMIC-III Data\DIAGNOSES_ICD.csv.gz", compression='gzip',
    header=0, sep=',', quotechar='"')
peek_ICDs = ICDs.head()
print(peek_ICDs)
ICDs.info()
#Filter for ICD codes for 282.60-282.69, referring to sickle cell types w/wo crisis
#2824 for thalassemia w + w/o crisis (282.41-282.42)
#SCD: 2826,2824
#Chronic Pain 3382
#Opioid dependencies: 3040,3047 (combo),
#HIV/AIDS ^042$

icds_of_interest = ICDs[ICDs['ICD9_CODE'].str.contains('2826|2824|3040|3047|3382|^042$', na=False)]

print(icds_of_interest.head())

icds_of_interest.info()

#patients_unique = icds_of_interest['SUBJECT_ID'].drop_duplicates()

NOTES = pd.read_csv(r"\Users\awalk55\OneDrive - Emory University\Desktop\Diss_Detecting_Provider_Bias\MIMIC-III Data\NOTEEVENTS.csv.gz", compression='gzip',
    header=0, sep=',', quotechar='"')

# Patients Dataframe-- DOB, gender, deceased
PATIENTS = pd.read_csv(r"\Users\awalk55\OneDrive - Emory University\Desktop\Diss_Detecting_Provider_Bias\MIMIC-III Data\PATIENTS.csv.gz", compression='gzip',
    header=0, sep=',', quotechar='"')

peek_patients = PATIENTS.head()
print(peek_patients)

# Admissions-- race

ADMISSIONS = pd.read_csv(r"\Users\awalk55\OneDrive - Emory University\Desktop\Diss_Detecting_Provider_Bias\MIMIC-III Data\ADMISSIONS.csv.gz", compression='gzip',
    header=0, sep=',', quotechar='"')

peek_admissions = ADMISSIONS.head()
print(peek_admissions)
