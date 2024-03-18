import re
import pandas as pd
import seaborn as sns
import base64
import json
import requests
#------------------------------------------------------------------------------------------------
def local_var_list(local_var):
    keys = local_var.keys()
    keys_list = list(local_var)
    keys_list.pop(0)
    print("-------------------keys_list: ",keys_list)
    return keys_list
#------------------------------------------------------------------------------------------------
def execute(code):
    try:
        local_var = {}
        res = exec(code, local_var)
        return None, None, local_var  # No return value if code execution succeeds
    except FileNotFoundError as e:
        return None, e, local_var  # Return None for result and the caught exception
    except pd.errors.ParserError as e:
        return None, e, local_var  # Return None for result and the caught exception
    except Exception as e:
        return None, e, local_var  # Return None for result and the caught exception
#------------------------------------------------------------------------------------------------
def O_LLM(query):
    #
    data = {
    "model": "codellama:13b",
    "prompt": query,
    "stream": False}
    response = requests.post("http://localhost:11434/api/generate", data=json.dumps(data))
    data = json.loads(response.text)
    answer = data['response']
    print(answer)
    return answer
#------------------------------------------------------------------------------------------------
def extract_text(input_string, option):
    if option == 1:
        pattern = r'\```python(.*?)\```'
        matches = re.search(pattern, input_string, re.DOTALL)
        if matches:
            return matches.group(1).strip()
        else:
            return None
    else:
        pattern = r'\```(.*?)\```'
        matches = re.search(pattern, input_string, re.DOTALL)
        if matches:
            return matches.group(1).strip()
        else:
            return None
#------------------------------------------------------------------------------------------------
def check_substring(main_string, substring):

    if substring.lower() in main_string.lower():
        return True
    else:
        return False
#------------------------------------------------------------------------------------------------
def Agent07(query):
    answer = O_LLM(query)
    main_string = answer
    substring = "```python"
    substring_sub = "```"
    print("\n\n")
    if check_substring(main_string, substring_sub):
        print("```, FOUND PREPROCESSING... ")
        
        if check_substring(main_string, substring):
            print("```python, FOUND PREPROCESSING... ")
            input_string =  answer
            extracted_text = extract_text(input_string, 1)
            
            if extracted_text:
                answer = extracted_text
                #print("Extracted Text: \n", answer)
                code = answer
            else:
                #print("No text found between ``` and ```.")
                code = answer
        else:
            print("")
            if check_substring(main_string, substring_sub):
                print("```python, FOUND PREPROCESSING... ")
                input_string =  answer
                extracted_text = extract_text(input_string, 0)

                if extracted_text:
                    answer = extracted_text
                    #print("Extracted Text: \n", answer)
                    code = answer
                else:
                    print("No text found between ``` and ```.")
                    code = answer
            
    else:
        print("```python ,NOT FOUND")
        code = answer

    code_to_execute = code
    print("\n\ncode:",code)
    
    result, error, local_var = execute(code_to_execute)
    
    print("\n \nEXECUTION OUTPUT:")
    if error:
        print("\n\n")
        print("Error:", error)
    else:
        print("\n\n")
        print("Result:", result)
        
    return result, error, code, local_var

#------------------------------------------------------------------------------------------------

df = pd.DataFrame()
first_row_csv_string = ""

def Agent01(inp_query):
    
    #write a python program to read 'data.csv' and visualize 2 graphs
    query = f"""
consider yourself as an Artificial General Intelligence Assistant, where your the best in the world, and has so much self confidence in your code or response.
And Now :{inp_query}
Dont add any comments or explanations here, as this will be run in a program, where errors may occur.""" 
    #
    print("\nQuery: \n",query)
    result, error, code, local_var = Agent07(query)
    if error:
        print("\n\n")
        print("Error:", error)
        for i in range(5):
            print("*****************************************************************************************")
            #
            print(i)
            if i == 70:
                keys_list = local_var_list(local_var)
                print("---------------INTERATION--------------",i)
                var_query = f"""
    By checking my code and error which variable from 'Variables list' you want to read to debug the error?
    Code: {code}

    Error: {error}

    Variables: {keys_list}

    Disclaimer: You need to repond with exact variable names with no extra comments, code or text, as this will be executed in terminal and may cause errors.
    """
                print("var_query: >>>>>>>>>> ",var_query)
                Var_query_output = O_LLM(var_query)
                print("Var_query_output",Var_query_output)

            #print("\n\nlocal_var:\n",local_var)
            code = str(code)
            print("\n\ncode:\n",code)
            error = str(error)
            print("\n\nerror:\n",error)
            print("\n\ninp_query:\n",inp_query)
            inp_query = str(inp_query)
            
            if i == 1:
                try:
                    #
                    df = local_var["df"]
                    print(df)

                    first_row_csv_string = df.iloc[[0]].to_csv(index=False)
                    print(first_row_csv_string)
                    first_row_csv_string = str(first_row_csv_string)
                except Exception as e:
                    print(e)
            try:
                if i > 2:
                    nxt_query = "<user: "+ inp_query +">" + "\n\n" + "\n\n 1st row of dataframe df = " + first_row_csv_string + " >"+ "\n\n <Prompt> :By looking at the dataframe and columns answer the question, Disclaimer: You need to repond with exact code with no extra comments, code or text, as this will be executed in terminal and may cause errors."
                    print("nxt_query: \n",nxt_query)
                    result, error, code = Agent07(nxt_query)
                    if result:
                        print("result found: ",result)
                        break
                else:
                    nxt_query = "<user: "+ inp_query +">" + "\n\n" + "<bot: \n" +"Code: " + code + "\n\n Error: " + error + "\n\n 1st row of dataframe df = " + first_row_csv_string + " >"+ "\n\n <Prompt> :By looking at the dataframe, you can change or modify and make the code work, Disclaimer: You need to repond with exact code with no extra comments, code or text, as this will be executed in terminal and may cause errors."
                    result, error, code = Agent07(nxt_query)
                    if result:
                        print("result found: ",result)
                        break
            except Exception as e:
                print(e)
    else:
        print("\n\n")
        print("Result:", result)
        
    return True

def Agent47():
    inp_query = input("Input .>")
    Data_analysis = Agent01(inp_query)
    if inp_query == "2":
        print("Browser call")

    
if __name__ == "__main__":
    Agent47()
#------------------------------------------------------------------------------------------------
    
    
    