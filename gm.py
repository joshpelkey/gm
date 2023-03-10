# Import the necessary package
import random
import psutil
import time
import datetime
import openai
import math
import re
import subprocess
from slack_sdk.webhook import WebhookClient

# my api keys and stuff, hidden from git
import keys

# Authenticate with OpenAI using your API key
openai.api_key = keys.openai_api_key

# Create a Slack client
client = WebhookClient(
    "https://hooks.slack.com/services/" + keys.slack_me_key
)

# ChatGPT temp
temp = 0.9

# get some cpu stats
memory_percent = psutil.virtual_memory().percent
cpu_percent = psutil.cpu_percent(interval=2)

uptime = time.time() - psutil.boot_time()
uptime_days = math.floor(uptime // (24 * 3600))
uptime = uptime % (24 * 3600)
uptime_hours = math.floor(uptime // 3600)
uptime %= 3600
uptime_minutes = math.floor(uptime // 60)
uptime %= 60
uptime_seconds = math.floor(uptime)

disk_usage = psutil.disk_usage("/")

# disk health
percentage_used = 100
nvme_file = open(keys.home_dir + "nvme.log", "r")
for line in nvme_file:
    if re.search ("percentage_used", line):
        percentage_used = re.findall(r'[0-9]+', line)

disk_health = 100 - int(percentage_used[0])

# some topics to choose from for topline quote
quote_topics = [
    "motivation",
    "leadership",
    "parenthood",
    "perserverance",
    "curiousity",
    "love",
    "life",
    "relationships",
    "family",
    "happiness",
    "friendship",
    "success",
    "courage",
    "inspiration",
    "happiness",
    "gratitude",
    "hope",
    "change",
    "beauty",
    "resilience",
    "kindness",
]

# pick a random quote topic
quote_topic = random.choice(quote_topics)
quote = "Share a random quote about " + quote_topic + " and attribute its author"
quote_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "user", "content": quote}
    ], 
    temperature=temp, 
    max_tokens=1024
)

# List of topics for daily
topics = [
    "Artificial intelligence",
    "Robotics",
    "Quantum computing",
    "Biotechnology",
    "Nanotechnology",
    "Genetics",
    "Data science",
    "Machine learning",
    "Energy technology",
    "Space exploration",
    "Solar power",
    "Renewable energy",
    "Environmental science",
    "Climate change",
    "Agriculture technology",
    "Medical technology",
    "Health informatics",
    "Drug discovery and development",
    "Neuroscience",
    "Cancer research",
    "Psychology",
    "Geology",
    "Meteorology",
    "Astronomy",
    "Astrophysics",
    "Particle physics",
    "Atomic physics",
    "Chemistry",
    "Materials science",
    "Geochemistry",
    "Oceanography",
    "Environmental engineering",
    "Electrical engineering",
    "Mechanical engineering",
    "Computer science",
    "Cybersecurity",
    "Internet of Things",
    "Blockchain technology",
    "Virtual reality",
    "Augmented reality",
    "3D printing",
    "Transportation technology",
    "Telecommunication",
    "Drones",
    "Television and video technology",
    "Music technology",
    "Video game technology",
    "Film and movie technology",
    "Photography technology",
    "Design and architecture technology",
]


# let's do something different each day of the week
day = datetime.datetime.now().weekday()

if day == 0:
    # monday's are hard
    question = "you are a college professor. tell me about a topic from the area of Aritifical Intelligence. Explain it to me at a college level."
    poem = "create a short poem about artificial intelligence"

elif day == 1:
    # tuesday's are for getting shit done
    # let's learn about science and tech
    science_topic = random.choice(topics)
    question = (
        "you are a college professor. pick a complex topic from the area of "
        + science_topic
        + " and tell me about it at a college level in 250 words."
    )
    poem = (
        "create a short poem about science and technology, particularly in the area of "
        + science_topic
    )

elif day == 2:
    # wednesday's ... keep going baby
    # how about we do a little money talk
    question = "You are a college professor. Pick a topic from the area of finacne. Explain it to me at a college level."
    poem = "create a short poem about money"
    
elif day == 3:
    # thursday's we see the light
    # let's get some fun stuff going
    question = "Pick a random book chapter from the Wheel of Time series. Provide an epic summary of the chapter, in the style of Robert Jordan."
    poem = "create a short poem about fantasy or sci-fi"

elif day == 4:
    # friday baby
    # let's talk music
    question = "You are a court jester. Tell me an interesting fact about music, something that would impress a young lady."
    poem = "create a short poem poem about music"

elif day == 5:
    # saturday --?? 
    question = "You are a historian. Tell me an interesting fact about a world landmark"
    poem = "create a short poem about travelling"

elif day == 6:
    # sunday -- a day of rest
    question = "You are a historian. Tell me about a pivotal moment in history in the voice of morgan freeman"
    poem = "create a short poem about history"

else:
    poem_response = "error yo"
    question_response = "error yo"

# Ask ChatGPT your question
poem_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "user", "content": poem}
    ],
    temperature=temp, 
    max_tokens=512
)

# Ask ChatGPT your question
question_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "user", "content": question}
    ],
    temperature=temp, 
    max_tokens=1024
)


# Send the response to the incoming Slack webhook
slack_response = client.send(
    text="good morning mr. pelkey...",
    blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":robot_face: :game_die:  Good Morning Mr. Pelkey  :game_die: :robot_face:",
            },
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": quote_response["choices"][0]["message"].get("content")}
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": question_response["choices"][0]["message"].get("content")},
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {"text": poem_response["choices"][0]["message"].get("content"), "type": "mrkdwn"}
            ],
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {
                    "text": "_Up "
                    + str(uptime_days)
                    + " days, "
                    + str(uptime_hours)
                    + " hours, "
                    + str(uptime_minutes)
                    + " minutes, and "
                    + str(uptime_seconds)
                    + " seconds || "
                    + str(cpu_percent)
                    + "% cpu || "
                    + str(memory_percent)
                    + "% ram || "
                    + str(disk_usage.percent)
                    + "% du || "
                    + str(disk_health)
                    + "% dh_",
                    "type": "mrkdwn",
                }
            ],
        },
    ],
)
