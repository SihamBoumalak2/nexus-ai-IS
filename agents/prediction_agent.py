# """
# prediction_agent.py

# This module defines the AttendancePredictionAgent class, which analyzes a student’s
# attendance history in a specific class and uses both heuristic pattern detection 
# and GPT to predict whether the student is at risk of being absent in the future.
# """

# # === Standard Library ===
# from datetime import datetime, timedelta  # For analyzing recent attendance patterns
# import sqlite3                            # For database access
# import os                                 # For accessing environment variables

# # === Third-Party Libraries ===
# import numpy as np                        # Optional for stats or expansion
# from openai import OpenAI                 # For natural language generation using GPT
# from dotenv import load_dotenv           # To load API key from .env

# # === Local Module ===
# from database import connect_db           # Helper to connect to the SQLite database

# # === Load API Key from Environment ===
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Stored securely in .env file


# class AttendancePredictionAgent:
#     """
#     This agent analyzes a student's attendance history and generates
#     a prediction or summary using both heuristics and GPT.
#     """

#     def __init__(self):
#         # Initialize GPT client
#         self.client = OpenAI(api_key="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")

#     def predict_absenteeism(self, student_id, class_name):
#         """
#         Main method to predict whether a student is at risk of future absenteeism.
#         It uses both pattern recognition (heuristics) and GPT to generate a human-readable summary.
#         """

#         with connect_db() as conn:
#             cursor = conn.cursor()

#             # Get class ID from name
#             cursor.execute("SELECT id FROM classrooms WHERE class_name = ?;", (class_name,))
#             result = cursor.fetchone()

#             # If no such class exists, notify the user
#             if not result:
#                 return f"❌ Class '{class_name}' not found."

#             class_id = result[0]

#             # Get all attendance records for this student in the given class
#             cursor.execute("""
#                 SELECT date, status FROM attendance
#                 WHERE enrollment = ? AND class_id = ?
#                 ORDER BY date ASC;
#             """, (student_id, class_id))

#             records = cursor.fetchall()

#             # If the student hasn't attended any sessions, we can't analyze anything
#             if not records or len(records) < 1:
#                 return "❌ Not enough attendance data to make a prediction."

#             # Analyze Attendance patterns
#             total = len(records)
            
#             # Count how many were marked as "Absent"
#             absences = sum(1 for r in records if r[1] == "Absent")

#             # Attendance rate: ((Present sessions) / Total sessions) * 100
#             attendance_rate = round((total - absences) / total * 100, 1)

#             # Check how many classes the student missed in the last 3 sessions
#             recent = records[-3:]
#             recent_absent_count = sum(1 for r in recent if r[1] == "Absent")

#             # Look for recurring absence patterns on the same weekday (e.g., always absent on Mondays)
#             weekday_counter = {}
#             for r in records:
#                 if r[1] == "Absent":

#                     # Convert the date string to a weekday (e.g., "2024-02-01" → "Thursday")
#                     weekday = datetime.strptime(r[0], "%Y-%m-%d").strftime("%A")
#                     weekday_counter[weekday] = weekday_counter.get(weekday, 0) + 1

#             # Identify which day of the week was missed the most
#             top_day = max(weekday_counter, key=weekday_counter.get) if weekday_counter else None

#             # Use GPT to generate a natural language summary of the findings
#             prompt = f"""
# You are an academic assistant AI. A student with ID {student_id} has attended the class {class_name}.

# - Total classes held: {total}
# - Total absences: {absences}
# - Attendance rate: {attendance_rate}%
# - Recent attendance (last 3 classes): {recent_absent_count} absences
# - Most missed day of the week: {top_day if top_day else 'N/A'}

# Write a short, personalized summary (2–3 sentences) of this student’s attendance pattern.
# If risk is high, suggest action. Be kind but informative.
# """

#             try:
#                 # Send the prompt to GPT and generate a response
#                 response = self.client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful academic advisor."},
#                         {"role": "user", "content": prompt}
#                     ]
#                 )

#                 # Return the AI-generated text summary
#                 return response.choices[0].message.content.strip()

#             except Exception as e:
#                 return f"⚠️ Could not generate summary: {str(e)}"
"""
prediction_agent.py

This file defines the AttendancePredictionAgent class, which analyzes a student's
attendance records for a specific class. It calculates their attendance rate, checks
if they have been absent frequently (especially recently or on specific days),
and generates a natural-language explanation using GPT.

The goal is to help students understand if their current attendance behavior
may put them at risk of being absent again in the future.
"""

# === Standard Python Libraries ===
from datetime import datetime             # For converting date strings into weekday names
import os                                 # To read environment variables securely
import sqlite3                            # For accessing and reading data from the database

# === Third-Party Libraries ===
import numpy as np                        # Used for numerical operations (not used in this file yet)
from openai import OpenAI                 # To generate natural-language summaries using GPT
from dotenv import load_dotenv            # To load the API key from the .env file

# === Project-Specific Import ===
from database import connect_db           # Function to connect to the SQLite database

# === Environment Variable Setup ===
load_dotenv()                             # Load variables from the .env file into the system environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Read the OpenAI key securely (do NOT hardcode it)

class AttendancePredictionAgent:
    """
    This class checks a student's attendance pattern for a specific class and
    creates a summary that explains whether their attendance behavior suggests
    a risk of missing more classes in the future.
    """

    def __init__(self):
        """
        Initializes the GPT client by providing the OpenAI API key from the environment.
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def predict_absenteeism(self, student_id, class_name):
        """
        Analyzes the student's attendance in a specific class. It calculates:
        - Total number of classes attended and missed
        - Attendance percentage
        - Number of absences in the last 3 classes
        - Whether the student frequently misses the same weekday (like Mondays)

        Then it sends this information to GPT, which writes a short summary message
        to help the student understand their current attendance status.

        Parameters:
            student_id (str): The student's enrollment number.
            class_name (str): The name of the class to check.

        Returns:
            str: A summary message describing the student's attendance status.
        """
        # Connect to the database
        with connect_db() as conn:
            cursor = conn.cursor()

            # Step 1: Find the class ID that matches the given class name
            cursor.execute("SELECT id FROM classrooms WHERE class_name = ?;", (class_name,))
            result = cursor.fetchone()

            if not result:
                return f"❌ Class '{class_name}' not found in the system."

            class_id = result[0]

            # Step 2: Get all attendance records for this student in the selected class
            cursor.execute("""
                SELECT date, status FROM attendance
                WHERE enrollment = ? AND class_id = ?
                ORDER BY date ASC;
            """, (student_id, class_id))

            records = cursor.fetchall()

            # If no attendance records are found, we cannot analyze the student's behavior
            if not records:
                return "❌ No attendance data available for this class."

            total_sessions = len(records)  # Total number of class sessions
            absences = sum(1 for r in records if r[1] == "Absent")  # Count number of absences
            attendance_rate = round((total_sessions - absences) / total_sessions * 100, 1)  # Calculate %

            # Step 3: Count how many of the last 3 classes were missed
            recent_records = records[-3:]  # Get the most recent 3 classes
            recent_absences = sum(1 for r in recent_records if r[1] == "Absent")

            # Step 4: Check if the student often misses a specific day of the week
            # For example, if they missed many Mondays
            day_absence_count = {}  # Dictionary to store how often each weekday was missed

            for record in records:
                date_string, status = record
                if status == "Absent":
                    weekday = datetime.strptime(date_string, "%Y-%m-%d").strftime("%A")
                    day_absence_count[weekday] = day_absence_count.get(weekday, 0) + 1

            # Find the weekday that was missed the most
            if day_absence_count:
                most_missed_day = max(day_absence_count, key=day_absence_count.get)
            else:
                most_missed_day = "N/A"

            # Step 5: Prepare a message to send to GPT to generate a summary
            prompt = f"""
You are an academic assistant AI. A student with ID {student_id} has attended the class '{class_name}'.

Here is a summary of their attendance:
- Total number of class sessions: {total_sessions}
- Number of absences: {absences}
- Attendance percentage: {attendance_rate}%
- Number of missed classes in the last 3 sessions: {recent_absences}
- Most frequently missed day of the week: {most_missed_day}

Write a short summary (2–3 sentences) to help the student understand their attendance situation.
If their attendance seems risky or low, kindly suggest that they should be more careful.
Avoid being harsh. Be clear and helpful.
"""

            # Step 6: Send the prompt to GPT and return the generated summary
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful academic advisor."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content.strip()

            except Exception as e:
                return f"⚠️ Could not generate summary because of an error: {str(e)}"
