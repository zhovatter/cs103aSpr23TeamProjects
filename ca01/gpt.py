'''
Demo code for interacting with GPT-3 in Python.

To run this you need to 
* first visit openai.com and get an APIkey, 
* which you export into the environment as shown in the shell code below.
* next create a folder and put this file in the folder as gpt.py
* finally run the following commands in that folder

On Mac
% pip3 install openai
% export APIKEY="......."  # in bash
% python3 gpt.py

On Windows:
% pip install openai
% $env:APIKEY="....." # in powershell
% python gpt.py
'''
import openai


class GPT():
    ''' make queries to gpt from a given API '''

    def __init__(self, apikey):
        ''' store the apikey in an instance variable '''
        self.apikey = apikey
        # Set up the OpenAI API client
        openai.api_key = apikey  # os.environ.get('APIKEY')

        # Set up the model and prompt
        self.model_engine = "text-davinci-003"

    def ZachQuery(self, input):
        prompt = f"Generate a 7 line poem about this topic: '{input}'"
        return self.getResponse(prompt)

    def ChristinaQuery(self, input):
        prompt = f"Generate a life motivation quote using this keyword '{input}'."
        return self.getResponse(prompt)

    def AndyQuery(self, input):
        prompt = f"Please give the definition of '{input}'."
        return self.getResponse(prompt)

    def getResponse(self, prompt):
        ''' Generate a GPT response '''
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
        )
        response = completion.choices[0].text
        return response


if __name__ == '__main__':
    '''
    '''
    import os
    g = GPT(os.environ.get("APIKEY"))
    query_decision = input(
        'enter name of persons query you want to use, Andy, Christina, or Zach: ')

    if query_decision == 'Andy':
        input = input("Enter a terminology that you would like explanation: ")
        print(g.AndyQuery(input))

    elif query_decision == 'Christina':
        input = input("Enter a keyword: ")
        print(g.ChristinaQuery(input))

    else:
        input = input("Enter the topic of your poem: ")
        print(g.ZachQuery(input))
