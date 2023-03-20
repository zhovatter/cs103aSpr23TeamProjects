'''
gptwebapp shows how to create a web app which ask the user for a prompt
and then sends it to openai's GPT API to get a response. You can use this
as your own GPT interface and not have to go through openai's web pages. 

We assume that the APIKEY has been put into the shell environment.
Run this server as follows:

On Mac
% pip3 install openai
% pip3 install flask
% export APIKEY="......."  # in bash
% python3 gptwebapp.py

On Windows:
% pip install openai
% pip install flask
% $env:APIKEY="....." # in powershell
% python gptwebapp.py
'''
from flask import request,redirect,url_for,Flask
from gpt import GPT
import os
import openai

app = Flask(__name__)
gptAPI = GPT(os.environ.get('APIKEY'))
openai.api_key = "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"

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q789789uioujkkljkl...8z\n\xec]/'

@app.route('/')
# intro homepage to our web app
def home():
    return '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>GPT Demo</title>
            </head>
            <body style="background-color: #f2f2f2;">
                <h1>Welcome to the world, little one. Your journey has begun...˗ˏˋ ♡ ˎˊ˗</h1>
                <pre style="background-color: CornflowerBlue;">Take time to breathe, to be present, and to connect with yourself. ♡❀˖⁺. ༶ ⋆˙⊹❀♡ <3 </pre>
                <pre style="background-color: pink;">Reflect on what's important in your life and prioritize self-care. ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆</pre>
                <p>Our team program has a special focus on mental health, and is designed to help users reflect on their thoughts and feelings in a safe and non-judgmental environment.</p>
                <p>We used GPT Demo to generate text based on user input.</p>
                <p>Whether you're looking for inspiration, support, or simply a way to express yourself, our program would help you generate a personal customized poem, motivation quote, and terminology </p>
                
                
                <p>To get started, go to the <a href="/form">form page</a> and input your thoughts. ❤️‍🩹 🧘</p>
                <p>Curious about our team members, go to the <a href="/team">team page</a> and check it out.</p>
                <p>More detail, go to <a href="/index">index page</a> :) •⩊• </p>
                <p>I hope you enjoy exploring your journey (๑ > ᴗ < ๑)</p>
                <p>✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩ ✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧ ೃ༄*ੈ✩✧</p>
                <hr>
             
            </body>
        </html>
    '''

# Each team member which ask the user for some input,
# Then calls the appropriate GPT method to get the response, which it sends back to the browser.


@app.route('/form')
def form():
    ''' display a link to the general query page '''
    print('processing / route')
    return f'''
        <h1>˖⁺‧₊˚♡˚₊‧⁺˖ Welcome to form page, which one would you like to explore first?</h1>
        <p>Interested in Poem: <a href="/poem">poem page</a></p>
        <p>Want some inspirations: <a href="/motivation">motivation page</a></p>
        <p>Ask me anything: <a href="/dictionary">dictionary page</a></p>
        <p><a href="/">home</a></p>
        <hr>
    '''

@app.route('/index')
def index():
    ''' displays links to each team-members page '''
    print('processing / route')
    return f'''
        <h1>˖⁺‧₊˚♡˚₊‧⁺˖ Welcome to the index page, which team member's contribution would you like to view first?</h1>
        <p>Zach's Poem Generator: <a href="/poem">poem page</a></p>
        <p>Christina's Motivational Quote Generator: <a href="/motivation">motivation page</a></p>
        <p>Andy's Dictionary: <a href="/dictionary">dictionary page</a></p>
        <p><a href="/">home</a></p>
        <hr>
    '''


@app.route('/poem', methods=['GET', 'POST'])
def poem():
    # handle a get request by sending a form 
    # and a post request by returning the GPT response
    if request.method == 'GET':
        return '''
        <h1>Make your own poem</h1>
        <hr>
        Enter your keyword below
        <form method="post">
            <textarea name="keyword"></textarea>
            <p><input type=submit value="get poem">
        </form>
        '''
    elif request.method == 'POST':
        keyword = request.form['keyword']
        prompt = f"Generate an original 7 line poem about this keyword: '{keyword}'"
        response = gptAPI.getResponse(prompt)
        return f'''
        <h1>Make your own poem</h1>
        <hr>
        Here is the response in text mode:
        <div style="border:thin solid black">{response}</div>
        <hr>
        Here is the response in "pre" mode:
        <pre style="border:thin solid black">{response}</pre>
        <a href={url_for('form')}> make another query</a>
        '''
    
@app.route('/motivation', methods=['GET', 'POST'])
def motivation():
    # handle a get request by sending a form 
    # and a post request by returning the GPT response
    if request.method == 'GET':
        return '''
        <h1>Motivation</h1>
        <hr>
        Enter your keyword below
        <form method="post">
            <textarea name="keyword"></textarea>
            <p><input type=submit value="get motivation quote">
        </form>
        '''
    elif request.method == 'POST':
        keyword = request.form['keyword']
        prompt = f"Generate a life motivation quote using the keyword '{keyword}'."
        response = gptAPI.getResponse(prompt)
        return f'''
        <h1>Motivation</h1>
        <hr>
        Here is the response in text mode:
        <div style="border:thin solid black">{response}</div>
        <hr>
        Here is the response in "pre" mode:
        <pre style="border:thin solid black">{response}</pre>
        <a href={url_for('form')}> make another query</a>
        '''
    
@app.route('/dictionary', methods=['GET', 'POST'])
def dictionary():
    # handle a get request by sending a form 
    # and a post request by returning the GPT response
    if request.method == 'GET':
        return '''
        <h1>Ask me anything</h1>
        <hr>
        Enter your keyword below
        <form method="post">
            <textarea name="keyword"></textarea>
            <p><input type=submit value="get definition">
        </form>
        '''
    elif request.method == 'POST':
        keyword = request.form['keyword']
        prompt = f"Give me the dictionary definition of {keyword} in English"
        response = gptAPI.getResponse(prompt)
        return f'''
        <h1>Ask me anything</h1>
        <hr>
        Here is the response in text mode:
        <div style="border:thin solid black">{response}</div>
        <hr>
        Here is the response in "pre" mode:
        <pre style="border:thin solid black">{response}</pre>
        <a href={url_for('form')}> make another query</a>
        '''


@app.route('/about')
def about():
    ''' display a link to the general query page '''
    print('processing / route')
    return f'''
        <h1>GPT Demo</h1>
        <a href="{url_for('gptdemo')}">Ask questions to GPT</a>
    '''

# @app.route('/index')
# def index():
#     ''' display a link to the general query page '''
#     print('processing / route')
#     return f'''
#         <h1>GPT Demo</h1>
#         <a href="{url_for('gptdemo')}">Ask questions to GPT</a>
#     '''


@app.route('/gptdemo', methods=['GET', 'POST'])
def gptdemo():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = gptAPI.getResponse(prompt)
        return f'''
        <h1>GPT Demo</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the response in text mode:
        <div style="border:thin solid black">{response}</div>
        Here is the response in "pre" mode:
        <pre style="border:thin solid black">{response}</pre>
        <a href={url_for('gptdemo')}> make another query</a>
        '''
    else:
        return '''
        <h1>GPT Demo App</h1>
        Enter your query below
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''
    


if __name__=='__main__':
    # run the code on port 5001, MacOS uses port 5000 for its own service :(
    app.run(debug=True,port=5001)
