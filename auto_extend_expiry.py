date = "1010-10-10"

import os
import requests
from time import sleep
from datetime import datetime


username = "yourusername"
password = "yourpassword"


def update_file(date_string):
    with open(__file__, "+r", encoding="utf-8") as file:
        content = file.read()
        file.seek(0)
        new_content = content.replace(file.readlines()[0], f'date = "{date_string}"\n')
        file.seek(0)
        file.write(new_content)


def create_error_log(extra_data=""):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, "error_log.txt")

    with open(file_path, 'w') as file:
        file.write(f"An error occured at {__file__}\n{extra_data}")


date_obj = datetime.strptime(date, "%Y-%m-%d")
today = datetime.now().date()
difference = (date_obj.date() - today).days

if difference <= 5:
    # Create a session
    session = requests.Session()

    # Define headers
    headers = {
        "Referer": "https://www.pythonanywhere.com/login/"
    }

    # Make the GET request to get the dynamic data
    response = session.get("https://www.pythonanywhere.com/login/", headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract csrfmiddlewaretoken from the response content
        csrf_token = response.text.split('name="csrfmiddlewaretoken" value="', 1)[1].split('"', 1)[0]

        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(response.content, "html.parser")
        # csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        # Define POST data with dynamic csrf token
        data = {
            "csrfmiddlewaretoken": csrf_token,
            "auth-username": username,
            "auth-password": password,
            "login_view-current_step": "auth"
        }

        # Make the POST request
        response = session.post("https://www.pythonanywhere.com/login/", headers=headers, data=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract csrf token from cookies
            csrf_token = session.cookies.get('csrftoken')

            # Make the schedule request
            schedule_response = session.get(f"https://www.pythonanywhere.com/api/v0/user/{username}/schedule/")

            # Check if the schedule request was successful (status code 200)
            if schedule_response.status_code == 200:
                task_data = schedule_response.json()[0]
                expiry_date = task_data["expiry"]
                task_id = task_data["id"]

                # Make the POST request to extend task
                extend_headers = {
                    "origin": "https://www.pythonanywhere.com",
                    "referer": f"https://www.pythonanywhere.com/user/{username}/tasks_tab/",
                    "x-csrftoken": csrf_token  # Include CSRF token in the headers
                }
                extend_response = session.post(
                    f"https://www.pythonanywhere.com/user/{username}/schedule/task/{task_id}/extend",
                    headers=extend_headers)

                # Check if the extend request was successful
                if extend_response.status_code == 200:
                    print("Task extended successfully!")
                    print(extend_response.content)

                    # Make the schedule request
                    schedule_response = session.get(f"https://www.pythonanywhere.com/api/v0/user/{username}/schedule/")

                    # Check if the schedule request after extending was successful (status code 200)
                    if schedule_response.status_code == 200:
                        task_data = schedule_response.json()[0]
                        expiry_date = task_data["expiry"]

                        update_file(expiry_date)
                    else:
                        create_error_log("Failed to retrieve the second schedule data.")

                else:
                    create_error_log("Failed to extend task.")
            else:
                create_error_log("Failed to retrieve the schedule data.")
        else:
            create_error_log("Failed to retrieve the page after POST request.")
    else:
        create_error_log("Failed to retrieve the page.")

