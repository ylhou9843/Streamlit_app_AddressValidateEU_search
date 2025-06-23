import streamlit as st
import requests

# Replace with your actual API key
EASYPOST_API_KEY = "EZTK1bdc79ebc5044ca8a44cd56fa7c34d0eakqM9V1LNtDI6RfbpA49wQ"

# Function to validate address
def validate_address_easypost(address):
    url = "https://api.easypost.com/v2/addresses/verify"
    headers = {"Authorization": f"Bearer {EASYPOST_API_KEY}"}
    payload = {
        "address": {
            "street1": address["Address Line 1"].upper(),
            "street2": address.get("Address Line 2", "").upper(),
            "city": address["City"].upper(),
            "zip": address["Postal Code"].upper(),
            "country": address["Country"].upper()
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if "address" in response_json:
        verifications = response_json["address"].get("verifications", {})
        delivery_status = verifications.get("delivery", {}).get("success", False)
        confidence = "High Confidence" if delivery_status else "Low Confidence !!!NEED CHECK!!!"
    else:
        confidence = "Low Confidence !!!NEED CHECK!!!"

    return response_json, confidence

# Function to format the verified address
def format_address_easypost(response):
    if "address" in response:
        addr = response["address"]
        formatted = f"{addr.get('street1', '')}, {addr.get('street2', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip', '')}, {addr.get('country', '')}"
        return formatted.strip(", ")
    else:
        return "Invalid address or could not be verified"

# Streamlit UI
st.set_page_config(
    page_title="EasyPost Address Validator",
    page_icon="📦"
)
st.title("📦 EasyPost Address Validator")

with st.form("address_form"):
    address1 = st.text_input("Address Line 1", "")
    address2 = st.text_input("Address Line 2 (Optional)", "")
    city = st.text_input("City", "")
    postal_code = st.text_input("Postal Code", "")
    country = st.text_input("Country", "")

    submitted = st.form_submit_button("Validate Address")

if submitted:
    user_address = {
        "Address Line 1": address1,
        "Address Line 2": address2,
        "City": city,
        "Postal Code": postal_code,
        "Country": country
    }

    with st.spinner("Validating address..."):
        try:
            result, confidence = validate_address_easypost(user_address)
            formatted_address = format_address_easypost(result)

            st.success("Address validated!")
            st.markdown(f"**Formatted Address:** {formatted_address}")
            st.markdown(f"**Confidence:** {confidence}")
            # st.json(result)  # Show raw API result if needed
        except Exception as e:
            st.error(f"Error during address validation: {str(e)}")
