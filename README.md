# Football Match Statistics Analyzer

A beginner-friendly football statistics comparison app built with Python and Streamlit.

## 1. What you need
- A computer with Python 3.10 or newer
- Internet connection for the first installation

## 2. Install
Open Terminal (Mac/Linux) or Command Prompt / PowerShell (Windows), then go to this folder.

Run:
```bash
python -m pip install -r requirements.txt
```

## 3. Run the app
```bash
python -m streamlit run app.py
```
Your browser should open the application. If it does not, copy the local address shown in the terminal (usually http://localhost:8501) into your browser.

## 4. Test data
Try this sample:
- Team A: Real Madrid — goals 2, shots 15, shots on target 7, possession 55, completed passes 480, attempted passes 550
- Team B: Barcelona — goals 1, shots 11, shots on target 4, possession 45, completed passes 390, attempted passes 460

The possession values should add up to 100. Completed passes must not exceed attempted passes, and shots on target must not exceed total shots.

## 5. What to learn from this project
1. Variables and data types
2. Functions
3. If/else conditions
4. Lists and dictionaries
5. Basic calculations and percentages
6. Displaying data with Streamlit
7. Reading a chart and explaining what it means

## Important
This is a learning project. Enter statistics from a match report you trust. The app does not automatically collect live match data and its statistical comparison is not a professional scouting verdict.
