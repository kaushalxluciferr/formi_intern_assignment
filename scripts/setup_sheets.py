# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# import os.path
# import json

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# def setup_sheets():
#     creds = None
    
#     if os.path.exists('token.json'):
#         with open('token.json', 'r') as token:
#             creds = Credentials.from_authorized_user_info(json.load(token))

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
        
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     service = build('sheets', 'v4', credentials=creds)
    
#     spreadsheet = {
#         'properties': {
#             'title': 'Barbeque Nation Conversation Logs'
#         },
#         'sheets': [
#             {
#                 'properties': {
#                     'title': 'Conversations',
#                     'gridProperties': {
#                         'rowCount': 1000,
#                         'columnCount': 9
#                     }
#                 }
#             }
#         ]
#     }
    
#     spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
#     spreadsheet_id = spreadsheet['spreadsheetId']
    
#     range_name = 'Conversations!A1:I1'
#     values = [
#         [
#             'Modality',
#             'Call Time',
#             'Phone Number',
#             'Call Outcome',
#             'Room Name',
#             'Booking Date',
#             'Booking Time',
#             'Number of Guests',
#             'Call Summary'
#         ]
#     ]
    
#     body = {
#         'values': values
#     }
    
#     service.spreadsheets().values().update(
#         spreadsheetId=spreadsheet_id,
#         range=range_name,
#         valueInputOption='RAW',
#         body=body
#     ).execute()
    
#     print(f"Spreadsheet created with ID: {spreadsheet_id}")
#     print("Please update the GOOGLE_SHEETS_ID in your .env file with this ID")

# if _name_ == '_main_':
#     setup_sheets()