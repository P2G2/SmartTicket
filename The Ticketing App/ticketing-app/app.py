import streamlit as st
from web3 import Web3
import json
import datetime


# Load the Ticketing.json file
with open("build/contracts/Ticketing.json") as f:
    ticketing_json = json.load(f)
# Connect to the local Ethereum network using Web3
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Load the Ticketing smart contract ABI and address
# Replace 'ABI' and 'ADDRESS' with the actual values
# Extract the ABI from the loaded JSON object
ticketing_abi = ticketing_json['abi']
ticketing_address = '0xd97dB1529e156fb56E8b499201F50cD042b9A965'
ticketing_contract = web3.eth.contract(address=ticketing_address, abi=ticketing_abi)

# Function to mint a new ticket
def mint_ticket():
    # Get user input
    recipient = st.text_input("Enter the recipient's address:")
    event_name = st.text_input("Enter the event name:")
    event_date = st.date_input("Enter the event date:")
    venue = st.text_input("Enter the venue:")
    price = st.number_input("Enter the ticket price:", min_value=0)

    if st.button("Mint Ticket"):
        # Convert datetime.date object to Unix timestamp
        event_date_unix = int(datetime.datetime(event_date.year, event_date.month, event_date.day).timestamp())

        # Replace '0' with the address of the account executing the transaction
        tx_hash = ticketing_contract.functions.mintTicket(
            recipient, event_name, event_date_unix, venue, price
        ).transact({"from": web3.eth.accounts[0]})
        st.write(f"Ticket minted! Transaction hash: {tx_hash.hex()}")


# Function to transfer a ticket
def transfer_ticket():
    # Get user input
    from_address = st.text_input("Enter the sender's address:")
    to_address = st.text_input("Enter the recipient's address:")
    ticket_id = st.number_input("Enter the ticket ID:", min_value=1)

    if st.button("Transfer Ticket"):
        tx_hash = ticketing_contract.functions.transferFrom(
            from_address, to_address, ticket_id
        ).transact({"from": web3.eth.accounts[0]})
        st.write(f"Ticket transferred! Transaction hash: {tx_hash.hex()}")

# Function to display ticket information
def display_ticket_info():
    # Get user input
    ticket_id = st.number_input("Enter the ticket ID:", min_value=1)

    if st.button("Get Ticket Info"):
        owner = ticketing_contract.functions.ownerOf(ticket_id).call()
        event_name, event_date, venue, price = ticketing_contract.functions.getTicketInfo(ticket_id).call()
        st.write(f"Owner of ticket {ticket_id}: {owner}")
        st.write(f"Event Name: {event_name}")
        st.write(f"Event Date: {event_date}")
        st.write(f"Venue: {venue}")
        st.write(f"Price: {price}")

# Create the Streamlit app title
st.title("Blockchain Ticketing App")

# Create Streamlit sidebar menu
menu = st.sidebar.selectbox("Choose an action:", ("Mint Ticket", "Transfer Ticket", "Display Ticket Info"))

if menu == "Mint Ticket":
    mint_ticket()
elif menu == "Transfer Ticket":
    transfer_ticket()
else:
    display_ticket_info()
