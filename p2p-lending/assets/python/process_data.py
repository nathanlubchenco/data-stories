import pandas as pd

loans_a = pd.read_csv("../data/LoanStats3a.csv")
loans_b = pd.read_csv("../data/LoanStats3b.csv")
loans_c = pd.read_csv("../data/LoanStats3c.csv")
loans_d = pd.read_csv("../data/LoanStats3d.csv")

loans_a['group'] = 'A'
loans_b['group'] = 'B'
loans_c['group'] = 'C'
loans_d['group'] = 'D'

loans_all = loans_a.append(loans_b).append(loans_c).append(loans_d)

# Only include loans where investors funded greater than 0 dollars in the loan
loans = loans_all[loans_all['funded_amnt_inv'] > 0]

df = loans[['loan_amnt',
            'id',
            'funded_amnt_inv', 
            'funded_amnt', 
            'loan_status',
            'next_pymnt_d',
            'term',
            'int_rate', 
            'installment',
            'total_pymnt', 
            'total_pymnt_inv', 
            'grade', 
            'group', # not sure of the relevance of this, just came from different files, maybe temporal aspect
            'issue_d',
            'home_ownership',
            #'annual_inc',
            #'annual_inc_joint',
            #'last_fico_range_high',
            #'last_fico_range_low',
            #'desc', ## could be some interesting NLP here .... or not...
            'recoveries',
            'out_prncp', 
            'out_prncp_inv', 
            'total_rec_int', 
            'total_rec_late_fee', 
            'total_rec_prncp' ]]

df['length_years'] = df.apply(lambda row: int(row['term'][0:3]) / 12.0 , axis =1)
df['pymnt_inv_minus_fees'] = df.apply(lambda row: row['total_pymnt_inv'] * 0.99, axis =1)
df['prncp_paid'] = df.apply(lambda row: row['funded_amnt_inv'] - row['out_prncp_inv'], axis =1)
# TODO make sure this is correct
#  It is based on actual borrower payments received each month, net of fees, actual charge offs, recoveries, and estimated future losses. To estimate future losses, we apply a loss rate estimate to the outstanding principal of any loans that are past-due but not charged off. The loss rate estimate is based on historical charge off rates by loan status over a 9-month period. 
# https://www.lendingclub.com/public/lendersPerformanceHelpPop.action
# https://www.lendingclub.com/account/investorReturnsAdjustments.action

df['profit'] = df.apply(lambda row: row['pymnt_inv_minus_fees'] - row['prncp_paid'], axis =1)
df['roi'] = df.apply(lambda row: 0 if row['prncp_paid'] == 0 else row['profit'] / row['prncp_paid'], axis =1)
df['APY'] = df.apply(lambda row:  (((row['profit'] +  row['funded_amnt_inv']) / row['funded_amnt_inv']) ** ( 1.0 / row['length_years'] )) -1, axis =1)

df.to_csv("../data/processed_loans.csv", index = False)
