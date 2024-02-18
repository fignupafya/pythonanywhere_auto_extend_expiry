# PythonAnywhere Task Expiry Extender

This Python script automates the process of extending the expiry date for a task in PythonAnywhere.
PythonAnywhere's free limited account provides a single task, which needs its expiry date extended periodically to prevent deletion. This script checks if the task's expiry date is within 5 days from the last known expiry and extends the expiry of the task.

## Usage
1. Replace `"yourusername"` and `"yourpassword"` in the script with your PythonAnywhere credentials.
2. Run the script.

## Functionality
- Checks if the task's expiry date is within 5 days.
- If the expiry date is within 5 days:
  - Logs in to PythonAnywhere
  - Retrieves the task's details
  - Extends the task's expiry date
  - Retrieves the new expiry date and updates the `date` variable in the script.

## Important Note
- Ensure that you have the necessary permissions and rights to perform these actions on PythonAnywhere.

## Disclaimer
This script is provided for educational purposes only. Use it responsibly and at your own risk. The developers are not responsible for any issue.
