# VibeCheck

## Inspiration
Do you feel that your managers sometimes just don't get you?

As a team of 3 student interns, we have personally experienced many instances of our text messages getting lost in translation when conversing with our colleagues. Unfortunately, we are not alone. In a 2021 study conducted with over 2,000 office workers, [over 70% experienced some form of unclear communication](https://hbr.org/2021/05/did-you-get-my-slack-email-text) from their colleagues. Due to the lack of experience in navigating the workplace environment, a disproportionately high number of interns suffer from this inability to communicate effectively, with [60% of employers](https://www.digett.com/insights/what-every-intern-should-know-about-business-communication) saying that applicants lack communication and interpersonal skills.

As the world shifts towards remote work, this issue has been further exacerbated. To combat this problem, we have developed VibeCheck, a Slack bot that enables mentors to better understand how their interns are feeling and provides suggested prompts to help interns through their trying periods, especially the initial onboarding process.

## What it does
VibeCheck has 3 core features:
1. Perform sentiment analysis to better understand how the interns are feeling
2. Give recommendations on how to respond in the scenario where mentees seem to be expressing negative sentiments
3. Provide an analysis of results to the mentor at the end of each week

By equipping our mentors with the ability to better understand how the interns are feeling, 


Our solution, VibeCheck, allows mentors to better read between the lines and understand what mentees might be struggling with.  
Equipping mentors with the ability to make informed decisions in real-time on how to best help mentees.
Mentors are better equipped to understand their mentees, and how they are feeling.
Finally, we believe that we encourage a sense of understanding and belonging to the greater community, while solving problems like imposter syndrome, a common symptom of new employees, especially interns.

In summary:



## How we built it
We used Hugging Face's transformers to perform sentiment analysis on the messages from mentees, allowing mentors to better understand the emotional and mental state of mentees at a quick glance. 
We chose Flask as our backend as most of the installed libraries were designed for easy integration with Python.
We chose MongoDB as our SQL backend, given it's reliable and large customer support.

## Challenges we ran into
We initially wanted to integrate with Microsoft Teams until we realized just how unfamiliar and time-consuming the process would be.

## Accomplishments that we're proud of

1. Made use of Hugging Face to perform sentiment analysis effectively
2. Successfully created a functioning slack bot using their documentation, capable of fulfilling the features we had set out to create.
3. Generated recommendations using conversational AI on the best responses for any given prompt. 

## What we learned

1. The sheer potential of transformers
2. Digital solutions can be used as tools to encourage better work culture

## What's next for VibeCheck

We intend to move onto removing the friction of coordinating meetings in a natural and seamless way to improve asynchronous work styles championed by hybrid/remote work.