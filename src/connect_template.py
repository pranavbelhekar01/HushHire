prompt_template = """


Question: {question}\
The response must ONLY contain the code snippet and NOTHING else.
The response must be one single line which contains only the query and must not be assigned to a variable. 

Make sure you follow the instructions/thought process below. 
Return a pandas DF query based on the question and CSV file schema below. 

Instructions: 
Make sure that the pandas query always accounts for positions which are very similar to the one asked in the question.


Example 1: 
Question: People who work at Google
df[df['Company'].str.contains('Google', case=False, na=False)]

Example 2:
Question: People from Pune
df[df['location'].str.contains('Pune',case=False, na=False)]

Example 3:
Question: people with an MBA degree and more than 2 years of experience
df[(df['degree'].str.contains('MBA',case=False,na=False)) & (df['experience']>2)]

CSV file schema: 

You also have access to a candidate data CSV which has the name, email,phone,location,degree,college,skills,companies,roles,degree_year,experience of the candidate.

"""

#You have access to a LinkedIn connections CSV file which has the First Name, Last Name, URL, Company, Position, and Connected On as columns. 

# Example 1: 
# Question: Product Managers
# df[df['Position'].str.contains('Product Manager', case=False, na=False)]
