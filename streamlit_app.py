import streamlit as st
from bot import check_trade

st.title("Paper Trading Dashboard 📈")

symbol = st.text_input("Enter stock symbol", "AAPL")

if st.button("Check Trade Setup"):
    result = check_trade(symbol)
    if result is None:
        st.write("Not enough data yet.")
    else:
        st.metric("Current Price", f"${result['price']:.2f}")
        st.metric("Support", f"${result['support']:.2f}")
        st.metric("Resistance", f"${result['resistance']:.2f}")
        st.metric("RSI", f"{result['RSI']:.2f}")
        st.write("Trend Up:", result['trend_up'])
        st.write("Signals:", ", ".join(result['signals']) if result['signals'] else "No signal")
