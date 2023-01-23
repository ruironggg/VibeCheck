# VibeCheck

## Credits
This repository would not have been possible without [@justintanyf](https://github.com/justintanyf), [@ruironggg](https://github.com/ruironggg), and [@seancze](https://github.com/seancze)

## Inspiration
Do you feel that your managers sometimes just don't get you?

As a team of 3 student interns, we have personally experienced many instances of our text messages getting lost in translation when conversing with our colleagues. Unfortunately, we are not alone. In a 2021 study conducted with over 2,000 office workers, [over 70% experienced some form of unclear communication](https://hbr.org/2021/05/did-you-get-my-slack-email-text) from their colleagues. Due to the lack of experience in navigating the workplace environment, a disproportionately high number of interns suffer from this inability to communicate effectively, with [60% of employers](https://www.digett.com/insights/what-every-intern-should-know-about-business-communication) saying that applicants lack communication and interpersonal skills.

As the world shifts towards remote work, this issue has been further exacerbated. To combat this problem, we have developed VibeCheck, a Slack bot that enables mentors to better understand how their interns are feeling and provides suggested prompts to help interns through their trying periods, especially the initial onboarding process.

Check out our demo video [here](https://youtu.be/VK1LYrRQ8Ss)! :)

## What it does
VibeCheck has 3 core features:
1. Perform sentiment analysis to better understand how the interns are feeling
![Sentiment Analysis And Prompt](assets/images/sentiment-analysis-and-prompt.png)
2. Give recommendations on how to respond in the scenario where mentees seem to be expressing negative sentiments
3. Provide an analysis of results to the mentor at the end of each week
![Wordcloud](assets/images/visualisation-of-results.png)

### Bonus feature
Additionally, our bot enables you to customise your classification labels according to your needs.

**New label**

![New Label](assets/images/new-label.png)

**Classifying by new label**

![New Label Results](assets/images/new-label-results.png)

## How to deploy
1. `pip install -r requirements.txt`
2. Create your own Slack Bot by following the instructions [here](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace)
3. Create a `.env` file with the following environment variables
   1. `MONGO_URL` = Connection string to mongodb
   2. `MONGO_DB`= Name of your database
   3. `SLACK_BOT_TOKEN`
   4. `SLACK_SIGNING_SECRET`
   5. `OPENAI_API_KEY`
4. Install ngrok
5. Start an ngrok server pointing to port 8000 via `ngrok http 8000`
6. Point your Slack Bot towards the URL provided to you by ngrok
7. Deploy the bot via `python app.py`

## Create venv using pip
````
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
````


## Create conda enviroment
`conda env create -f environment.yml`


## How to run
run using `flask run`, it runs on port 5000
## How we built it
We used Hugging Face's transformers to perform sentiment analysis on the messages from mentees, allowing mentors to better understand the emotional and mental state of mentees at a quick glance. 
We chose Flask as our backend as most of the installed libraries were designed for easy integration with Python.
We chose MongoDB as our no-SQL database, given it's reliable and offers a large variety of integrations

## Challenges we ran into
We initially wanted to integrate with Microsoft Teams until we realized just how unfamiliar and time-consuming the process would be. Additionally, we experienced tremendous difficulty finding the appropriate AI models to use as this was our first time working on Natural Language Processing (NLP) and sentiment analysis.

## Accomplishments that we're proud of

1. Leveraged several AI algorithms to conduct sentiment analysis and recommend ways to help an intern through tough times
2. Successfully created a functioning Slack Bot using their documentation, capable of fulfilling the features we had set out to create.
3. Generated recommendations using conversational AI on the best responses for any given prompt. 

## What we learned

1. The sheer potential of transformers
2. Digital solutions can be used as tools to encourage better work culture
3. The importance of delegating work
4. A deeper understanding of how remote work has impacted work culture adversely
5. How to build a Slack Bot using Python
6. How to use Flask
7. How to use MongoDB
8. The applications of `zero-shot-classification` models

## What's next for VibeCheck (Future Work)

We intend to move onto removing the friction of coordinating meetings in a natural and seamless way to improve asynchronous work styles championed by hybrid/remote work. 

Future development for our bot includes:
1. **Weekly prompts** asking interns how they are feeling for the week
2. **“Thumbs Up” or “Thumbs Down”** feedback system to the suggested prompts provided
3. An AI model capable with "text-to-sql" capabilities to enable the mentor to extract deeper insights from the data collected
4. A greater diversity of visualising data collected, including the use of bar and pie charts