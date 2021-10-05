import pandas as pd

dataset=pd.read_excel("/Data - Survey Monkey Output Edited.xlsx", "Edited_Data")
dataset

dataset_modified=dataset.copy()
dataset_modified

dataset_modified.columns

dataset_modified=dataset_modified.drop(columns=['Start Date', 'End Date', 'Email Address', 'First Name', 'Last Name', 'Custom Data 1'])
dataset_modified.columns

dataset_modified

id_vars=list(dataset_modified.columns)[:8]
id_vars

value_vars=list(dataset_modified.columns)[8:]
value_vars

dataset_melted=dataset_modified.melt(id_vars=id_vars, value_vars=value_vars, var_name="Question + Subquestion", value_name="Answer")
dataset_melted

questions_import=pd.read_excel("/Data - Survey Monkey Output Edited.xlsx", "Question")
questions_import

questions=questions_import.drop(columns=['Raw Question', 'Raw Subquestion', 'Subquestion'])
questions

dataset_merged=pd.merge(left=dataset_melted, right=questions, how="left", left_on="Question + Subquestion", right_on="Question + Subquestion")
print("Original Data", len(dataset_melted))
print("Merged Data", len(dataset_merged))
dataset_merged

respondents=dataset_merged[dataset_merged["Answer"].notna()]
respondents=respondents.groupby("Question")["Respondent ID"].nunique().reset_index()
respondents.rename(columns={"Respondent ID":"Respondents"}, inplace=True)
respondents

dataset_merged_two=pd.merge(left=dataset_merged, right=respondents, how="left", left_on="Question", right_on="Question")
print("Original Data", len(dataset_merged))
print("Merged Data", len(dataset_merged_two))
dataset_merged_two

same_answer=dataset_merged
same_answer=same_answer.groupby(["Question + Subquestion", "Answer"])["Respondent ID"].nunique().reset_index()
same_answer.rename(columns={"Respondent ID":"Same Answer"}, inplace=True)
same_answer

dataset_merged_three=pd.merge(left=dataset_merged_two, right=same_answer, how="left", left_on=["Question + Subquestion", "Answer"], right_on=["Question + Subquestion", "Answer"])
dataset_merged_three["Same Answer"].fillna(0, inplace=True)
print("Original Data", len(dataset_merged_two))
print("Merged Data", len(dataset_merged_three))
dataset_merged_three

dataset_merged_three.columns

output=dataset_merged_three
output.rename(columns={'Identify which division you work in. - Response':'Division Primary', 'Identify which division you work in. - Other (please specify)':'Division Secondary', 'Which of the following best describes your position level? - Response':'Position', 'Which generation are you apart of? - Response':'Generation', 'Please select the gender in which you identify. - Response':'Gender', 'Which duration range best aligns with your tenure at your company? - Response':'Tenure', 'Which of the following best describes your employment type? - Response':'Employment Type'}, inplace=True)
output

output.to_excel("/Output.xlsx", index=False)
