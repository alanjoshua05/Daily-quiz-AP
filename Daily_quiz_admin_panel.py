import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

# Google Sheets authentication
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('data-419313-295934c65ef4.json', scopes)
client = gspread.authorize(credentials)

# Open the desired sheet
sheet = client.open("FirstSheet").sheet1

# Read data from the sheet
data = sheet.get_all_values()

# Convert to DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Display DataFrame using Streamlit
st.title('Daily Quiz admit panel 🧑‍💼')
st.subheader('Entire record')
st.dataframe(df)
st.subheader('Desire day report')
a = st.date_input('Select the date you want to see the report')

# Execute the SQL-like query on the DataFrame
result_df = df.query(f"Timestamp == '{str(a)}'")
st.write("Query Result:")
st.dataframe(result_df)

# Extract email addresses
dat = set(str(email)[:-14].upper() for email in result_df["Email Address"])

# Read data from the Excel file
df1 = pd.read_excel("Csbs.xlsx")

# Extract roll numbers
dat1 = set(str(roll_no) for roll_no in df1["Roll No"])

# Determine missing elements
mis = dat1 - dat

# Create DataFrame from missing elements with status (Submitted or Missing)
missing_data = [{"Status": "Submitted", "Count": len(dat)}, {"Status": "Missing", "Count": len(mis)}]
mis_df = pd.DataFrame(missing_data)

# Display bar chart comparing lengths of submitted and missing sets
st.write('Students performance graph')
st.bar_chart(mis_df.set_index("Status"))

# Display DataFrame of missing elements with student names
mi_df = pd.DataFrame({"Roll No": list(mis)})
mi_df = mi_df.merge(df1[['Roll No', 'Student Name']], on='Roll No', how='left')
st.write('Non submitted students')
st.dataframe(mi_df)
