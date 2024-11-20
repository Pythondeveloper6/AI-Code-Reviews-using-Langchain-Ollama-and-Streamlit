# handle AI functions (langchain + ollama) : llama3.2:1b
import mlflow
from langchain.chains import LLMChain  # chains : conversation
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import json 

# setup mlflow --> using autolog (log chains --> )
# openAI + mlflow --> show more details 
# connect code + mlflow (fix data not showing in mlflow)
# miflow ui should run first before our code 

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment('langchain_code_reviewer')
mlflow.langchain.autolog(log_models=True , log_input_examples=True)



def generate_prompt_template():
    input_variables = ["question", "programming_language"]
    template = """
        You are an expert software engineer reviewing {programming_language} code. Analyze the following code and provide:
        - Code quality score from 1 to 10.
        - Code pros.
        - Code cons.
        - Code security check.
        - A better version of the code.
        - Explain the better version and why it is better.

        Code:
        ```
        {question}
        ```

        Return the data as markdown , like 
        ## Code quality score  : score
        - explanation of this score 

        <br>

        ## Code pros
        - explanation 

        <br>

        ## Code Cons
        - explanation 
        
        <br>

        ## Code security check
        - explanation 

        <br>

        ## A better version of the code 
        - explanation 

        <br>

        ## Explain the better version and why it is better
        - explanation 
        
    """
    return PromptTemplate(input_variables=input_variables, template=template)




def perform_code_review_with_ollama(question,programming_language):
    llm = OllamaLLM(model="llama3.2:1b")
    prompt_template = generate_prompt_template()

    # create langchain pipline
      # 1 : create chain
    chain = LLMChain(prompt=prompt_template , llm=llm)

      # run chain with vairables 
    result = chain.run({"question":question , "programming_language": programming_language})

    # print(f"result : {result}")

    # review_data = json.loads(result)
    # print(f'review_data : {review_data}')
    return result