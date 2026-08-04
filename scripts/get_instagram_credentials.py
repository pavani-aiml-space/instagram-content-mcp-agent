"""
Script to help get Instagram Account ID and test credentials
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_instagram_account_id(facebook_page_id: str, access_token: str) -> str:
    """
    Get Instagram Business Account ID from Facebook Page ID
    
    Args:
        facebook_page_id: Facebook Page ID
        access_token: Instagram Access Token
    
    Returns:
        Instagram Business Account ID
    """
    url = f"https://graph.facebook.com/v18.0/{facebook_page_id}"
    
    params = {
        "fields": "instagram_business_account",
        "access_token": access_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        error_data = response.json()
        error_msg = error_data.get("error", {}).get("message", "Unknown error")
        raise Exception(f"Failed to get Instagram account ID: {error_msg}")
    
    data = response.json()
    instagram_account = data.get("instagram_business_account", {})
    
    if not instagram_account or "id" not in instagram_account:
        raise Exception("No Instagram Business Account linked to this Facebook Page")
    
    return instagram_account["id"]


def verify_access_token(access_token: str, account_id: str = None) -> dict:
    """
    Verify that the access token is valid
    
    Args:
        access_token: Instagram Access Token
        account_id: Optional Instagram Account ID to verify
    
    Returns:
        Dictionary with verification results
    """
    if account_id:
        # Verify token with account
        url = f"https://graph.facebook.com/v18.0/{account_id}"
        params = {
            "fields": "username,account_type",
            "access_token": access_token
        }
    else:
        # Just verify token
        url = "https://graph.facebook.com/v18.0/me"
        params = {"access_token": access_token}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "valid": True,
            "data": data,
            "message": "✅ Access token is valid!"
        }
    else:
        error_data = response.json()
        return {
            "valid": False,
            "error": error_data.get("error", {}),
            "message": "❌ Access token is invalid or expired"
        }


def main():
    """Main function to help user get Instagram credentials"""
    
    print("=" * 60)
    print("Instagram Credentials Setup Helper")
    print("=" * 60)
    print()
    
    # Check if access token is set
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    if not access_token:
        print("❌ INSTAGRAM_ACCESS_TOKEN not found in .env file")
        print()
        print("To get an access token:")
        print("1. Go to https://developers.facebook.com/tools/explorer/")
        print("2. Select your app")
        print("3. Generate access token with permissions:")
        print("   - instagram_basic")
        print("   - instagram_content_publish")
        print("   - pages_show_list")
        print("4. Add to .env: INSTAGRAM_ACCESS_TOKEN=your_token_here")
        return
    
    print("✅ Found INSTAGRAM_ACCESS_TOKEN")
    print()
    
    # Verify access token
    print("Verifying access token...")
    verification = verify_access_token(access_token)
    print(verification["message"])
    
    if not verification["valid"]:
        print(f"Error: {verification.get('error', {})}")
        return
    
    print()
    
    # Check if account ID is already set
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    if account_id:
        print(f"✅ Found INSTAGRAM_ACCOUNT_ID: {account_id}")
        print()
        print("Verifying account ID...")
        account_verification = verify_access_token(access_token, account_id)
        print(account_verification["message"])
        if account_verification["valid"]:
            print(f"Username: {account_verification['data'].get('username', 'N/A')}")
            print(f"Account Type: {account_verification['data'].get('account_type', 'N/A')}")
        return
    
    # Help user get account ID
    print("❌ INSTAGRAM_ACCOUNT_ID not found in .env file")
    print()
    print("To get your Instagram Account ID, you need your Facebook Page ID.")
    print()
    
    facebook_page_id = input("Enter your Facebook Page ID (or press Enter to skip): ").strip()
    
    if not facebook_page_id:
        print()
        print("To find your Facebook Page ID:")
        print("1. Go to your Facebook Page")
        print("2. Click 'About'")
        print("3. Scroll down to find 'Page ID'")
        print()
        print("Or use this script again with your Facebook Page ID")
        return
    
    try:
        print()
        print("Getting Instagram Account ID...")
        instagram_account_id = get_instagram_account_id(facebook_page_id, access_token)
        
        print()
        print("=" * 60)
        print("✅ Success! Add this to your .env file:")
        print("=" * 60)
        print(f"INSTAGRAM_ACCOUNT_ID={instagram_account_id}")
        print("=" * 60)
        print()
        
        # Verify the account ID
        print("Verifying account ID...")
        account_verification = verify_access_token(access_token, instagram_account_id)
        print(account_verification["message"])
        if account_verification["valid"]:
            print(f"Username: {account_verification['data'].get('username', 'N/A')}")
            print(f"Account Type: {account_verification['data'].get('account_type', 'N/A')}")
        
    except Exception as e:
        print()
        print(f"❌ Error: {e}")
        print()
        print("Make sure:")
        print("1. Your Instagram account is a Business account")
        print("2. Your Instagram is linked to the Facebook Page")
        print("3. You're using the correct Facebook Page ID")
        print("4. Your access token has the required permissions")


if __name__ == "__main__":
    main()

