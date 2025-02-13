
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from datetime import date
from db import get_data
from langchain.llms import Ollama

llm = Ollama(model='llama3.2:latest')
import pandas as pd


table_schema = '''
student_id 
1001
INTEGER
 
name 
Alice Smith
TEXT
 
date_of_birth 
2002-07-15
TEXT
 
gender 
Female
TEXT
 
phone_number 
304-555-1212
TEXT
 
result_of_semester_1 
3.8
REAL
 
result_of_semester_2 
3.9
REAL
 
result_of_semester_3 
4
REAL
 
result_of_semester_4 
3.7
REAL
 
result_of_semester_5 
3.9
REAL
 
result_of_semester_6 
4
REAL
 
attendance_percentage_semester_1 
92
INTEGER
 
attendance_percentage_semester_2 
95
INTEGER
 
attendance_percentage_semester_3 
90
INTEGER
 
attendance_percentage_semester_4 
88
INTEGER
 
attendance_percentage_semester_5 
93
INTEGER
 
attendance_percentage_semester_6 
96
INTEGER
 
age 
22
INTEGER
 
college_name 
Sunway College
TEXT
 
college_details 
Sunway College Kathmandu is working in academic partnership with Birmingham City University, UK offering specialized undergraduate course in data science and artificial intelligence, BSc(Hons) Computer Science with Artificial Intelligence. The university ranks 601-800 as per Times Higher Education World Rankings 2024.
TEXT
**SCHEMA ENDS** 


Use the below example as refrense only:

**Example**

User Question:
    List all students who have an attendance percentage above 90% in the first semester.
SQL Query:
    SELECT student_id, name, attendance_percentage_semester_1
    FROM students
    WHERE attendance_percentage_semester_1 > 90;

User Question:
    Get the average GPA for each student across all six semesters.
SQL Query:
    SELECT student_id, name,
        (result_of_semester_1 + result_of_semester_2 + result_of_semester_3 + 
            result_of_semester_4 + result_of_semester_5 + result_of_semester_6) / 6 AS average_gpa
    FROM students;

User Question:
    Find the students who are older than 22.
SQL Query:
    SELECT student_id, name, age, college_name, college_details
    FROM students
    WHERE age > 22;

User Question:
    List all female students with a GPA above 3.8 in the 5th semester.
SQL Query:
    SELECT student_id, name, gender, result_of_semester_5
    FROM students
    WHERE gender = 'Female' AND result_of_semester_5 > 3.8;



User Question:
    Retrieve the names of students who have attended every semester with an attendance percentage over 90%.
SQL Query:
    SELECT student_id, name
    FROM students
    WHERE attendance_percentage_semester_1 > 90
    AND attendance_percentage_semister_2 > 90
    AND attendance_percentage_semister_3 > 90
    AND attendance_percentage_semister_4 > 90
    AND attendance_percentage_semister_5 > 90
    AND attendance_percentage_semister_6 > 90;

User Question:
    Get the details of students who have a GPA above 3.5 in the 4th semester.
SQL Query:
    SELECT student_id, name, result_of_semister_4
    FROM students
    WHERE result_of_semister_4 > 3.5;

User Question:
    List students who have a GPA above 3.5 in all semesters.
SQL Query:
    SELECT student_id, name, college_name
    FROM students
    WHERE result_of_semester_1 > 3.5
    AND result_of_semester_2 > 3.5
    AND result_of_semester_3 > 3.5
    AND result_of_semester_4 > 3.5
    AND result_of_semester_5 > 3.5
    AND result_of_semester_6 > 3.5;

User Question:
    Find the highest GPA in the 2nd semester across all students.
SQL Query:
    SELECT MAX(result_of_semester_2) AS highest_gpa_semester_2
    FROM students;

User Question:
    Find the highest GPA in the 4th semester across all students and get the details of those students.
SQL Query:
    SELECT student_id, name, result_of_semester_4, college_name, college_details, age, gender, phone_number
    FROM students
    WHERE result_of_semester_2 = (SELECT MAX(result_of_semester_2) FROM students);

User Question: 
    Get the names of students with the lowest attendance percentage in the 6th semester.
SQL Query:
    SELECT student_id, name, attendance_percentage_semester_6
    FROM students
    WHERE attendance_percentage_semester_6 = (SELECT MIN(attendance_percentage_semester_6) FROM students);

User Question: 
    Show the names of students who consistently improved their results (GPA) from semester 1 to semester 6.
SQL Query:
    SELECT name
    FROM students
    WHERE result_of_semester_1 < result_of_semester_2
    AND result_of_semester_2 < result_of_semester_3
    AND result_of_semester_3 < result_of_semester_4
    AND result_of_semester_4 < result_of_semester_5
    AND result_of_semester_5 < result_of_semester_6;

USER QUESTION:
- Give me the detail of student `dummpy name`. OR detail of `dummy name` OR who is `xyg`
OUTPUT: 
SELECT student_id, name, date_of_birth, gender, phone_number, 
       result_of_semester_1, result_of_semester_2, result_of_semester_3, 
       result_of_semester_4, result_of_semester_5, result_of_semester_6,
       attendance_percentage_semester_1, attendance_percentage_semester_2, 
       attendance_percentage_semester_3, attendance_percentage_semester_4, 
       attendance_percentage_semester_5, attendance_percentage_semester_6,
       age
FROM students
WHERE name = 'given name';

USER QUESTION:
- Give me the detail of college. OR detail of college OR name of college Or what is your college name.
OUTPUT: 
SELECT college_name ,college_details FROM students limit 1


'''

# You are an expert SQL query generator, responsible for accurately converting natural language instructions into SQL queries and provide SQL query only.You need to work in single database sinlge table so you don't need to perform join operations. Its schema is described as follows:


def get_prompt()->PromptTemplate:

    prompt = PromptTemplate(
        template=""" 
You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than 5 rows. Its schema is described as follows:

{table_schema}

Always table name students



## Rules: 
 -Generate sql query only.
 - Only read at max 10 records at a time

The conversation history is given below consider this to understand quenstions asked by user to manage the context of convesation:
**Chat History**
{history}
Always look the history before crafting the final output.

Make sure you only answer the quetion asked dont try create things out.
Only the sql output is accepted as the output.Generate relavent sql query for the following question.
**USER QUESTION**: {question}
**SQL OUTPUT**: 

""")
    return prompt
    



# These are the example for your refrence: 
#         If user question was- hello. you should reply `True`.
#         If user question was - "Good morning." reply-> `True`.
#         If user question was - "How are you." reply-> `True`.
#         If user question was - "student with higest mark." reply-> `False`
# classify user input
    # You are class Teacher of the students details provided below so answer the users question as responsible Teacher.You are in a parent teacher meeting.

def classify_user_query(question,schema,history):
    prompt = f'''
    Classify the following user query as either 'Small Talk' or 'Table-Related Question'.
    If the query is about general conversation or casual chit-chat, label it as `True`.
    If the query is related to tables, such as features, sizes, or specifications, label it as `False`.
    

    Rule:
        - Reply only True or False. No resoning and No explanation.
        - Only boolen output is accepted: `True` for chit-chat or `False` for Table Related Question

    **Example of chit chat**
        “How’s your day going?”
        “What’s the weather like today?”
        “How are you doing?”
        “Got any plans for the weekend?”
        “What’s your favorite movie?”
        “Is it a good time to chat?”
        “Do you like coffee or tea?”
        “How was your morning?”
        “What’s new with you?”
        “Did you catch the game last night?”
        “I’m so tired today, how about you?”
        “How are things going in your world?”
        “Do you have a favorite book?”
        “What’s your favorite holiday?”
        “What do you like to do for fun?”
        "weather today"

        
    **Questions related to this table schema are not  chit-chat or small talk classify as `False`**
        ## My table schema:
        {schema}


    Conversation Histiory is related to out database table useually if not small talks.
    **History**
    {history}
    **History Ends**

    
    **Classify this user question to True (small talk) or False **
      {question}

    You answer True if its is smalltalk not. False if it can be answered from this database table data. Table contain data realted to students only
    Make 100 percentage sure the answer is only `True` or `False`. Can be used in if satement to specify the route.

    **Your Final Answer(True or False)** '''
    return llm.invoke(prompt)
    

def rewite_question(question,history,schema):
    prompt= f'''You are project manager who knows about database with schema below and who craft asked by user to software engineer so that they can generate sql from the question you rewrote.
    You  task is to rewite the question looking at the history of convesation with user so that we can maintain the chain of conversation, context undersataing.
    Only rewrite the question do not overdo to create answer its okay to reply same question.
    The scheam of my sql table looks like: 
    {schema}
    
    The conversation Histiry with user is:
    {history}

    The recent question asked by user is:
    {question}

    ## Rule: 
        - Just rewrite the question asked. Don't need to provide the reason.
        - Should be single line.
        - If history is not proved do not worry.


    You have to rewite this recent question so that we can generate the sql for that question. Make it sort concise and correct. 
    ## Rewitten question: 
    '''
    return llm.invoke(prompt)

def transform_response(question,answer):
    prompt = f'''
    Follow the rule to achive the goal. No more than that.
    # Rule:
      - Translate the following JSON data into a clear and simple human-readable summary.
      - If given data's lenght is longer than 5 show in the tabular form using markdown.
      - If user question was chit chat or small talk like hello hi,how are you, etc. but there is some json output provided, ignore that json and answer that users question in chit chat way.   I want you to act smart 

    # Goal
      - The goal is to explain the information in the JSON in plain language, highlighting the key details in a conversational manner.
    Just given answer based on json only no salutation and greeting required.
    **Original human question was:** 
        {question}
    **Output JSON:**
        {answer}

   If the asked question is not answered by in given answer give your own output. Do not output none sense output.
    '''
    return llm.invoke(prompt)

def sql_generater(question,history): 
    if len(question.split(" ")) < 2:
        return "",llm.invoke(question)
    is_smalltalk = str(classify_user_query(question,history,table_schema))
    # if is_smalltalk:
    #     print(is_smalltalk)
    if 'true' in is_smalltalk.lower() and 'false' not in is_smalltalk.lower():
        return "",llm.invoke(question)
    
    
    
    
    question = rewite_question(question,history,table_schema)
    prompt  = get_prompt()
    today_date = date.today().strftime("%d-%m-%Y")

    _chain = prompt | llm 

    out = _chain.invoke({"table_schema":table_schema,"history":history,"question":question})

    for i in range(3):
        print(f"from agent file Try {i} \n llm out: {out}")
        if out.lower().startswith("select"):
            #output from database.
            df = get_data(out)
            if isinstance(df, pd.DataFrame):
               if len(out)==0:
                   return out,transform_response(question,"response was empty so say can not found result for this question")
               else:
                    return out,transform_response(question,df.to_json(orient='records', lines=False))
               
            out = _chain.invoke({"table_schema":table_schema,"history":history,"question":question +"\n" + out})

        else:
            print("The string does not start with 'select'")
            out = _chain.invoke({"table_schema":table_schema,"history":history,"question":question +"\n" + out + " Your response must be sql query starting with select. Fix this error and give the sql only. Dont give reason just give only one SQL query."})
    
    
    out = llm.invoke(question)
    return "",out
    #from here save to db





'''
user question: 
 - Find the Student with the Highest GPA in Each Grade Level
SQL OUTPUT: 
 - SELECT grade_level, first_name, last_name, gpa
FROM students_details s
WHERE gpa = (
    SELECT MAX(gpa)
    FROM Students
    WHERE grade_level = s.grade_level
)
ORDER BY grade_level;

user question: 
-Retrieve the Top 3 Students by Class Rank for Each Major/Program of Study
OUTPUT: 
 - WITH RankedStudents AS (
    SELECT student_id, first_name, last_name, major_program_of_study, class_rank,
           ROW_NUMBER() OVER (PARTITION BY major_program_of_study ORDER BY class_rank) AS rank
    FROM students_details
)
SELECT student_id, first_name, last_name, major_program_of_study, class_rank
FROM RankedStudents
WHERE rank <= 3
ORDER BY major_program_of_study, class_rank;

USER QUESTION:
- Give me the detail of student fname lname. 
OUTPUT: 
- Select * from students where first_name='fname' and last_name = 'lname'
'''
    




