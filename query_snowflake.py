import os
import requests
import snowflake.connector

def get_azure_oauth_token():
    
    tenant_id = os.environ["AZURE_TOKEN_ENDPOINT"]
    url = os.environ["AZURE_TOKEN_ENDPOINT"]

    payload = {
        'client_id': '{AZURE_CLIENT_ID}',
        'client_secret': '{AZURE_CLIENT_SECRET}',
        'grant_type': 'client_credentials',
        'scope': '{APPLICATION_ID}/.default'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
    print("🚨 Azure OAuth Error:", response.status_code)
    print("🔧 Response body:", response.text)
    response.raise_for_status()
 
    
    # Extract and print access token
    token = response.json().get('access_token')
    # print("Access Token:", token)

def query_snowflake(token):
    ctx = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        authenticator="oauth",
        token=token,
        role=os.environ.get("SNOWFLAKE_ROLE"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
        database=os.environ.get("SNOWFLAKE_DATABASE"),
        schema=os.environ.get("SNOWFLAKE_SCHEMA")
    )

    cs = ctx.cursor()
    try:
        cs.execute("SELECT CURRENT_TIMESTAMP();")
        for row in cs:
            print("Result:", row)
    finally:
        cs.close()
        ctx.close()

if __name__ == "__main__":
    token = get_azure_oauth_token()
    query_snowflake(token)
