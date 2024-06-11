prompt_template = """

Question: {question}\
The response must ONLY contain the code snippet and NOTHING else.
The response must be one single line which contains only the query and must not be assigned to a variable. 

Make sure you follow the instructions/thought process below. 
Return a pandas DF query based on the question and CSV file schema below. 

Instructions: 
Make sure that the pandas query always accounts for search results which are very similar to the one asked in the question.

Example 1: 
Question: Candidates who have worked at a bank
df[df['companies'].str.contains('bank', case=False, na=False)]

Example 2: 
Question: Candidates from Gurgaon
df[df['location'].str.contains('Gurgaon', case=False, na=False)]

CSV file schema: 
You have access to a resume candidates CSV file which has the name, email, location, degree, college, skills, companies, roles, degree_year, and experience as columns. 

"""