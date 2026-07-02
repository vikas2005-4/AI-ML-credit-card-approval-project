import pandas as pd
import numpy as np
import os
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'dataset'), exist_ok=True)
N=500
np.random.seed(42)
Gender = np.random.choice(['Male','Female'], N)
Age = np.random.randint(21,70,N)
Income_Type = np.random.choice(['Salaried','Self-Employed','Business','Unemployed'], N, p=[0.6,0.2,0.15,0.05])
Annual_Income = np.round(np.random.normal(60000,25000,N),2)
Employment_Duration = np.random.randint(0,40,N)
Education_Level = np.random.choice(['High School','Bachelors','Masters','PhD'], N, p=[0.2,0.5,0.25,0.05])
Marital_Status = np.random.choice(['Single','Married','Divorced','Widowed'], N)
Occupation = np.random.choice(['Clerk','Manager','Executive','Technician','Other'], N)
Housing_Type = np.random.choice(['Owned','Rented','Mortgage'], N)
Family_Members = np.random.randint(0,6,N)
Credit_Score = np.clip(np.random.normal(650,70,N).astype(int),300,850)
Existing_Loans = np.random.randint(0,5,N)
Loan_Amount = np.round(np.random.normal(15000,8000,N),2)
Payment_History = np.random.choice(['Good','Average','Bad'], N, p=[0.7,0.2,0.1])
# compute approval probability
score = (Annual_Income/1000)*0.3 + (Credit_Score-300)/5 - Existing_Loans*10 - (Loan_Amount/1000)*0.2 + (Payment_History=='Good')*30
prob = 1/(1+np.exp(-(score-50)/10))
Approval_Status = np.where(prob>0.5,'Approved','Rejected')

df = pd.DataFrame({
 'Gender':Gender,
 'Age':Age,
 'Income_Type':Income_Type,
 'Annual_Income':Annual_Income,
 'Employment_Duration':Employment_Duration,
 'Education_Level':Education_Level,
 'Marital_Status':Marital_Status,
 'Occupation':Occupation,
 'Housing_Type':Housing_Type,
 'Family_Members':Family_Members,
 'Credit_Score':Credit_Score,
 'Existing_Loans':Existing_Loans,
 'Loan_Amount':Loan_Amount,
 'Payment_History':Payment_History,
 'Approval_Status':Approval_Status
})

out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset', 'credit_card.csv'))
df.to_csv(out, index=False)
print('SYNTHETIC_DATASET_CREATED:', out)
