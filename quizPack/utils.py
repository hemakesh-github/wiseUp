from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import time
import os
import traceback
N = 5
class Quiz(BaseModel):
    question: str = Field(description="Question and also program if needed.")
    opt1: str = Field(description="1st option")
    opt2: str = Field(description="2st option")
    opt3: str = Field(description="3st option")
    opt4: str = Field(description="4st option")
    answer: str = Field(description="answer to the generated question only allowed values are one of 'opt1, opt2, opt3, opt4'.")
    explanation: str = Field(description="This is the explanation for the answer to the question.")

class LLMConfig():
    def __init__(self) :
        self.api_key = os.environ.get('GOOGLE_AI_API')
        self.llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=self.api_key)
        

class Question(LLMConfig):
    def __init__(self):
        super().__init__()
        self.finalResult = {}
    
    def getQuestion(self, topic, current_Questions = {}, n = N, diffLevel = 1):
        q = rf'''Generate a unique question in the  in the following topics. topics: {topic} and the difficulty level is {diffLevel} out of 5 the following should be the structure for each question:
        {{'question': question, 'opt1':  option 1, 'opt2': option 2, 'opt3': option 3 'opt4': option 4, 'answer': correct option}}
        every question should be unique question and have all four options along with answer and explanation of why the the answer is correct and also why other options are incorect.
        each question has only single correct answer. Be sure to make sure that the options contain answer and ensure that the answer is correct.
        and be extremely sure the question, options, and answer are correct, unique and relevant to the topic also makes sense along with correct explanation for the answer.
        Check the question and answer before submitting. Reduce mistakes and errors.the answer should be given in the form of opt1, opt2, opt3, opt4 NOT as the answer itself the answer should always be any one of 
        opt1, opt2, opt3, opt4.
        here are some examples of the question and answer:
        {{'question': 'What is the output of the following code?\n\npython\nx = "hello"\nprint(x[1:3])\n', 'opt1': 'el', 'opt2': 'lo', 'opt3': 'hel', 'opt4': 'e', 'answer': 'opt1', 'explanation': 'Slicing in Python is zero-based, so x[1:3] extracts characters from index 1 to index 2, not including 3. Therefore, the output is "el".'}}
        {{'question': 'Which of the following statements is true about Python?', 'opt1': 'Python is a statically typed language.', 'opt2': 'Python code must be compiled before execution.', 'opt3': 'Python uses curly braces to define code blocks.', 'opt4': 'Python is an interpreted language.', 'answer': 'opt4', 'explanation': 'Python is an interpreted language, which means that Python code is executed line by line, without the need for a separate compilation step.'}}
        the following questions are already gnerated and should not be repeated:
        {current_Questions}
        remember that you are beeing used as a plugin in a program so be sure to return the output in the correct format as there are many errors of Invalid JSON format avoid that
        some problems from previous generations are that the answer is not in the form of opt1, opt2, opt3, opt4 so be sure to return the answer in the correct format.
        and for some questions the options are wrong or contain multiple answers and also for some the explanation is wrong and facts are not correct so be sure to check the question and answer before submitting.
        some of the questions you have generated previously makes no sense or are incorrect and does not contain whole contex. CHECK BEFORE SUBMITTING.
        '''
        parser = JsonOutputParser(pydantic_object=Quiz)
        
        for i in range(N):
            try:
                prompt = PromptTemplate(
                    template="Answer the user query.\n{format_instructions}\n{query}\n",
                    input_variables=["query"],
                    partial_variables={"format_instructions": parser.get_format_instructions()},
                )
                chain = prompt | self.llm | parser
                r = chain.invoke({"query": q})
                # print(r)
                # print(r.keys())
                if self.outputCheck(r):
                    print('f')
                    print(len(self.finalResult))
                    self.finalResult['question'+str(i+1)] = dict(r)
                    if len(self.finalResult) == N:
                        break
                else:
                    self.getQuestion(topic, self.finalResult, N-len(self.finalResult))
            except Exception as e:
                print(e)
                traceback.print_exc()
                new_prompt =rf'''The previous question raised {e} so please generate a new question'''
                self.getQuestion(topic,str(self.finalResult) + new_prompt, N-len(self.finalResult))
        return self.finalResult
            
    def outputCheck(self,r):
        if r['answer'] not in ['opt1', 'opt2', 'opt3', 'opt4']:
            print(r['answer'])
            # time.sleep(2)
            return False
        return True
        

class FlashQuestion(BaseModel):
    question: str = Field(description="Question and also program if needed.")
    answer: str = Field(description="The answer to the question and also the explanation for the answer it can be of any length.")

class FlashCards(LLMConfig):
    def __int__(self):
        super().__init__()
        self.finalResult = {}
        
        
        
    def getFlashCard(self, context, difLevel = 1):
        q = rf'''
You are a teacher and you are preparing flashcards for your students. You want to create flashcards from the 
text given and you should NOT USE ANY KNOWLEDGE OUTSIDE THE PROVIDED TEXT.  text: {context} and the difficulty
level of {difLevel} out of 5. The following should be the structure for each flashcard:
{{'question': question, 'answer': answer}}
BE SURE NOT TO USE ANY KNOWLEDGE OUTSIDE THE PROVIDED TEXT. The answer should be the correct answer along with 
the explanation. The answer can be of any length. Be sure to make sure that the question and answer are correct, 
unique and one can answer from reading the text, also makes sense along with correct explanation for the answer.
Check the question and answer before submitting. Reduce mistakes and errors. Be sure to make sure that the 
question and answer are correct, unique and relevant to the topic also makes sense along with correct 
explanation for the answer. Check the question and answer before submitting. Reduce mistakes and errors.
Generate maximum number of questions WITHIN context of the GIVEN TEXT and NOT ANYOTHER KNOWLEDGE ACQUIRED
flashcard WITHOUT ANY REPEATED QUESTIONS following the above instructions.'''
        try:
            parser = JsonOutputParser(pydantic_object=FlashQuestion)
            prompt = PromptTemplate(
                    template="Answer the user query.\n{format_instructions}\n{query}\n",
                    input_variables=["query"],
                    partial_variables={"format_instructions": parser.get_format_instructions()},
                )
            chain = prompt | self.llm | parser
            r = chain.invoke({"query": q})
            print(r)
            return r
        except Exception as e:
            print(e)
            self.getFlashCard(context, difLevel)
    
        
# Q = Question()
# print(Q.getQuestion('python programming'))
# f = FlashCards()
# x = f.getFlashCard('Python is a high-level, interpreted programming language. It is known for its simplicity and readability, making it an excellent choice for beginners. Python is versatile and can be used for a wide range of applications, including web development, data analysis, artificial intelligence, and scientific computing. Python uses an elegant syntax that allows developers to write clear and concise code. It also has a large standard library that provides ready-to-use modules and packages for common tasks. Python is an open-source language, which means that it is free to use and distribute. It is supported by a large and active community of developers who contribute to its growth and development. Python is a popular choice for both professional developers and hobbyists due to its ease of use and flexibility.', 1)
# for i in x:
#     print(i['question'])
#     print(i['answer'])
# x ={}
# y = {'hell': 'opt1'}
# for i in range(5):
#     x['question'+str(i)] = y
# print(x)