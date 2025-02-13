import sqlite3
import pandas as pd
import os 

def get_data(query):
    try:
        cwd = os.getcwd()
        conn = sqlite3.connect(f"{cwd}/college.db")
        result = pd.read_sql(query,conn)
        print("printing from-db.py",result)
        return result
    except Exception as e:
        print(e)
        return f"For the given question. Generated query: \n {query} \n Error: {e} \n Fix this error and give the sql only. Dont give reason just give only one SQL query."



if __name__=='__main__':
    cwd = os.getcwd()

    df = pd.read_csv(f"{cwd}/data2.csv")
    df['college_name'] = 'Sunway College'
    df['college_details'] = '''
    Sunway College Kathmandu is working in academic partnership with Birmingham City University, UK offering specialized undergraduate course in data science and artificial intelligence, BSc(Hons) Computer Science with Artificial Intelligence. The university ranks 601-800 as per Times Higher Education World Rankings 2024.

    Birmingham City University (BCU) is a leading UK university renowned for its strong industry links and focus on practical learning. Ranked 601-800 in the Times Higher Education World Rankings 2024, BCU boasts a diverse student body of over 31,000 individuals from more than 100 countries. Located in the heart of Birmingham, a vibrant and dynamic city, BCU offers a unique learning environment that blends academic excellence with real-world experience.

    With over 31,000 students from over 100 countries, BCU is a large and diverse university set in the heart of Birmingham with a focus on practice-based learning. BCU puts students at the heart of everything they do, giving them the best opportunities for future success.'''

    df.to_sql(name="students", con=conn, if_exists="replace",index=False) 


