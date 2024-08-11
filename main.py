import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()

# орепаi.api_key = os.environ.get("OPENAI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI__API_KEY")
# if you saved the key under a different environment variable name,
# client = OpenAI(#
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

# Create Assitant
# personal_trainer_assis = client.beta.assistants.create(
#     name='Personal Trainer',
#     instructions="""You are the best trainer to train a user that how to file a tax return, prepare the data and much more. You also provide suggestions for better tax savings.""",
#     model=model
# )
# print(personal_trainer_assis.id)



# Thread
# thread = client.beta.threads.create(
#     messages=[{
#         'role':'user',
#         'content':'How do I file a tax return?'
#     }]
# )
# thread_id = thread.id
# print(thread_id)

# Run

assistant_id = 'asst_QizQYyRGVX9nYR3pRPZ27ZLZ'
thread_id = 'thread_9ZFNPEx0gWBlDsx6NVk4ZeqK'

# Create a message

message = 'How do I file a tax return?'
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role='user',
    content=message
)

run = client.beta.threads.runs.create(
    assistant_id=assistant_id,
    thread_id=thread_id,
    instructions='Please address the user as Ankit Bansal.'
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id = run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    '%H:%M:%S', time.gmtime(elapsed_time)
                )

                print(f'Run completed in {formatted_elapsed_time}')
                logging.info(f'Run completed in {formatted_elapsed_time}')
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f'Assistant Response: {response}')
                break
        except Exception as e:
            logging.error(f'An error occured while retrieving the run: {e}')
            break
        logging.info('Waiting for the run to complete ... ')
        time.sleep(sleep_interval)

wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)
run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread_id,
    run_id=run.id
)

print(f'Steps ---> {run_steps.data}')