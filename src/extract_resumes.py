from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import requests
#from jose import jwt
import webbrowser
import base64
import json
from fastapi import Query

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Read credentials from the file
with open(r'C:\Job\Hushh\Projects\HushHire\src\credentials_webapp.json', 'r') as file:
    credentials = json.load(file)

# Extract values from the 'web' dictionary
web_credentials = credentials.get("web", {})
GOOGLE_CLIENT_ID = web_credentials.get("client_id")
GOOGLE_CLIENT_SECRET = web_credentials.get("client_secret")
GOOGLE_REDIRECT_URI = web_credentials.get("redirect_uris", [])[0]  # Assuming the list has at least one element


@app.get("/login/google")
async def login_google():
    # oauth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    
    #Below is the URL to prompt the user to login to his specified gmail account and also give a readonly access to his gmail
    oauth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email%20https://www.googleapis.com/auth/gmail.readonly&access_type=offline"

    webbrowser.open(oauth_url)
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@app.get("/auth/google")
async def auth_google(code: str):
    #This code is basically the authorization code and this authorization code helps us to get the access token with the required scopes that we have set .
    #We require the gmail.readonly scopes that requires verification of our application and all.
    token_url = "https://accounts.google.com/o/oauth2/token"
    print(code)
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    print(response.json())
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    #You can change this job query to get the specific documents 
    #jobs_query = "subject:new application:iOS Developer has:attachment after:2023/11/01 "
    jobs_query = "subject:new application:iOS Developer has:attachment after:2023/11/01 before:2023/12/14"
    #jobs_query= custom_parameter
    gmail_url = f"https://www.googleapis.com/gmail/v1/users/me/messages?q={jobs_query}&maxResults=1"
    gmail_response = requests.get(gmail_url, headers={"Authorization": f"Bearer {access_token}"})
    messages = gmail_response.json().get("messages", [])
    print(messages)
    print("Printing gmail response")
    print(gmail_response.json())
    # Fetch attachments from the first message
    attachments = []
    for i,message in enumerate(messages) :
        print(i)
        print(message)

        if message:
            message_id = message.get("id")
            print(message_id)
            if message_id:
                message_url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}"
                message_response = requests.get(message_url, headers={"Authorization": f"Bearer {access_token}"})
                message_data = message_response.json()

                # Check for parts in the message payload
                if "payload" in message_data and "parts" in message_data["payload"]:
                    for part in message_data["payload"]["parts"]:
                        if "body" in part and "attachmentId" in part["body"]:
                            attachment_id = part["body"]["attachmentId"]
                            attachment_url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/attachments/{attachment_id}"
                            attachment_response = requests.get(attachment_url, headers={"Authorization": f"Bearer {access_token}"})
                            attachment_data = attachment_response.json()
                            data = attachment_data.get("data")
                            filename = part.get("filename", "untitled.txt")
                            print(filename)
                            print(data[:10])



                            if data:
                                # Decode base64-encoded attachment data
                                attachment_content = base64.urlsafe_b64decode(data.encode("UTF-8"))

                                # Save the attachment to a file
                                
                                save_path = f"/Users/katoch/Documents/hushh/resumes/{filename}"
                                with open(save_path, "wb") as file:
                        
                                    file.write(attachment_content)

                                attachments.append(save_path)

    print(attachments)
    print(len(attachments))
    return user_info.json()

# @app.get("/token")
# async def get_token(token: str = Depends(oauth2_scheme)):
#     return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)