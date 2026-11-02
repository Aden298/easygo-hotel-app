import streamlit as st
from datetime import datetime, date
import os
from PIL import Image

# ==========================================
# PAGE SETUP & ALIGNED HEADER
# ==========================================
st.set_page_config(page_title="EasyGo Hotel Booking", page_icon="🏨", layout="centered")

# Create two columns for the header: small one for the logo, large one for the title text
header_left, header_right = st.columns([1, 4])

logo_filename = "logo.jpeg"  
if os.path.exists(logo_filename):
    try:
        logo_img = Image.open(logo_filename)
        with header_left:
            # Drop the logo in the left column
            st.image(logo_img, width=120) 
    except Exception:
        pass

with header_right:
    # Place the main title text in the right column next to it
    st.title("EasyGo Hotel Booking System")
    st.write("Welcome to EasyGo Hotel Booking System!")

st.divider()

# ==========================================
# PHASE 2: CUSTOMER INFORMATION
# ==========================================
st.header("Customer Information")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Please enter your name:")
with col2:
    ic_number = st.text_input("Please enter your IC number:")

# ==========================================
# PHASE 2.5: STAY ITINERARY ARRANGEMENT
# ==========================================
st.header("📅 Stay Itinerary Arrangement")
col3, col4 = st.columns(2)

with col3:
    check_in_date = st.date_input("Check-in Date", min_value=date.today())
with col4:
    check_out_date = st.date_input("Check-out Date", min_value=check_in_date)

check_in_time = st.text_input("Please enter your estimated arrival time (e.g., 2:00 PM):")

# Calculate nights automatically
number_of_nights = (check_out_date - check_in_date).days

if number_of_nights <= 0:
    st.error("❌ Check-out date must be AFTER the check-in date.")
    st.stop()
else:
    st.success(f"Total Duration Automatically Calculated: **{number_of_nights} Night(s)**")

st.divider()

# ==========================================
# PHASE 3: ROOM & OPTIONS SELECTION
# ==========================================
st.header("🛏️ Room Selection")

room_options = {
    "single": 80,
    "double": 120,
    "family": 250,
    "suite": 300
}

type_of_room = st.selectbox("Please select the type of room you want to book:", list(room_options.keys()))
price_per_room = room_options[type_of_room]

number_of_rooms = st.number_input("Please enter the number of rooms you want to book:", min_value=1, step=1, value=1)

# Breakfast section
breakfast_input = st.radio("Do you want to add RM50 for breakfast?", ("yes", "no"), index=1)
breakfast_price = 50 if breakfast_input == "yes" else 0

# Base calculations before coupon
cart_total = (price_per_room * number_of_nights * number_of_rooms) + breakfast_price

# ==========================================
# PHASE 4: DISCOUNT COUPON SYSTEM
# ==========================================
st.header("🎟️ Discount Code")
coupons_db = {
    "SAVE10": {"type": "percentage", "value": 10},
    "SAVE20": {"type": "percentage", "value": 20},
}

discount_code = st.text_input("Please enter your discount code (Optional):").strip().upper()
discount_amount = 0.0

if discount_code:
    if discount_code in coupons_db:
        discount_info = coupons_db[discount_code]
        if discount_info["type"] == "percentage":
            discount_amount = cart_total * (discount_info["value"] / 100)
            st.success(f"🎉 Code applied! {discount_info['value']}% off (-RM{discount_amount:.2f})")
    else:
        st.error(f"❌ Invalid discount code: '{discount_code}'")

final_total = max(0.0, cart_total - discount_amount)

# ==========================================
# PHASE 5: PAYMENT METHOD & RECEIPT TRIGGER
# ==========================================
st.header("💳 Checkout & Payment")
payment_method = st.selectbox("Please select your payment method:", ["Select Option", "cash", "credit card"])

if payment_method != "Select Option":
    
    # 1. Handle payment amount input dynamically
    if payment_method == "cash":
        st.info(f"💵 Counter Payment required: RM{final_total:.2f}")
        payment_input = st.number_input("Please enter the amount you want to pay: RM", min_value=float(final_total), value=float(final_total), step=10.0)
    else:
        card_number = st.text_input("Please enter your credit card number:")
        payment_input = st.number_input("Please enter the amount to pay: RM", min_value=float(final_total), value=float(final_total), step=10.0)

    # 2. Calculate balance instantly
    balance = payment_input - final_total
    st.metric(label="Change Balance to Return", value=f"RM{balance:.2f}")

    # 3. Print Receipt Button
    if st.button("Complete Booking & Print Receipt"):
        if payment_method == "credit card" and not card_number:
            st.error("❌ Please enter your credit card number to process payment.")
        else:
            st.success("🎉 Transaction Completed Successfully!")
            st.divider()
            st.subheader("🧾 Generated Receipt Output")
            
            try:
                # Import your local printing function module
                from receipt import print_receipt
                
                # Capture the receipt output by calling your module function
                # Note: If your receipt function prints directly to the terminal, look below to capture it on screen!
                receipt_output = print_receipt(
                    name, 
                    ic_number, 
                    type_of_room, 
                    price_per_room, 
                    breakfast_input, 
                    final_total, 
                    payment_input, 
                    balance, 
                    number_of_rooms, 
                    number_of_nights, 
                    payment_method
                )
                
                # If your print_receipt returns a string, this displays it beautifully on the webpage:
                if receipt_output:
                    st.text(receipt_output)
                else:
                    st.info("👋 Receipt sent successfully! Check your VS Code terminal window to view/print it.")
                    
            except Exception as e:
                st.error(f"⚠️ App structure completed, but receipt execution ran into a script error: {e}")
