import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# Streamlit App: Rogue Option Target Simulator

st.set_page_config(page_title="Rogue Option Target Simulator", layout="centered")

st.title("🎯 Rogue Option Buyer Target Simulator")
st.markdown("Enter your option data below to simulate a realistic price target and stop loss range using Greeks.")

# Input fields
stock_name = st.text_input("Stock Name", value="ZydusLife")
option_type = st.selectbox("Option Type", ["Call", "Put"])
spot = st.number_input("Current Spot Price", value=960.0)
strike = st.number_input("Strike Price", value=960.0)
option_ltp = st.number_input("Current Option LTP", value=23.1)
delta = st.number_input("Delta", value=0.55)
gamma = st.number_input("Gamma", value=0.0074)
theta = st.number_input("Theta (per day)", value=-0.53)
vega = st.number_input("Vega", value=0.9)
days = st.number_input("Holding Period (Days)", value=2)
iv = st.number_input("Implied Volatility (IV %)", value=17.0)

# Adjust delta/gamma direction for puts
sign = 1 if option_type == "Call" else -1

# Auto-calculate expected spot move using SD formula
expected_spot_move = spot * (iv / 100) * math.sqrt(days / 365)

# Calculation logic
delta_gain = expected_spot_move * delta
gamma_boost = expected_spot_move * gamma * 100  # magnified impact (heuristic)
theta_loss = abs(theta) * days

estimated_target = option_ltp + sign * delta_gain + abs(gamma_boost) - theta_loss
suggested_sl = option_ltp - (theta_loss + abs(gamma_boost))  # risk threshold

# Checklist evaluation
delta_ok = 0.4 <= abs(delta) <= 0.65
gamma_ok = gamma >= 0.005
theta_ok = abs(theta) <= 0.20
vega_ok = vega <= 0.75

# Display results
st.subheader("📈 Simulated Outcome")
st.markdown(f"**Expected Spot Move (Auto):** ₹{expected_spot_move:.2f}")
st.markdown(f"**Estimated Target Premium:** ₹{estimated_target:.2f}")
st.markdown(f"**Suggested Stop Loss:** ₹{suggested_sl:.2f}")
st.markdown(f"**Reward Range:** ₹{estimated_target - option_ltp:.2f}")
st.markdown(f"**Risk Range:** ₹{option_ltp - suggested_sl:.2f}")
st.markdown("---")

# Checklist assessment
st.subheader("✅ Rogue Option Buyer Checklist")
st.markdown(f"**Delta (0.4–0.65):** {'✅' if delta_ok else '❌'}")
st.markdown(f"**Gamma (> 0.005):** {'✅' if gamma_ok else '❌'}")
st.markdown(f"**Theta (<= 0.20):** {'✅' if theta_ok else '❌'}")
st.markdown(f"**Vega (<= 0.75):** {'✅' if vega_ok else '❌'}")

# Final verdict
st.subheader(f"🔍 Rogue Verdict for {stock_name.upper()} {option_type.upper()} Option")
if delta_ok and gamma_ok and theta_ok and vega_ok:
    st.success(f"✔️ {stock_name} {option_type.upper()} is a strong candidate for a directional buy!")
elif delta_ok and gamma_ok:
    st.warning(f"⚠️ {stock_name} {option_type.upper()} has directional potential, but theta/vega risk is elevated.")
else:
    st.error(f"❌ {stock_name} {option_type.upper()} doesn't meet the Rogue Buyer standards.")

st.caption("Note: Spot move is now automatically calculated using the IV-based SD formula. Use this as a tactical edge, not gospel.")

# Premium Projection Graph
st.subheader("📊 Premium Projection vs Spot Price")
spot_range = np.linspace(spot - expected_spot_move*2, spot + expected_spot_move*2, 50)
premium_range = option_ltp + sign * (spot_range - spot) * delta + (spot_range - spot)**2 * gamma * 10 - theta_loss

fig, ax = plt.subplots()
ax.plot(spot_range, premium_range)
ax.axhline(option_ltp, color='gray', linestyle='--', label='Entry Price')
ax.axvline(spot, color='red', linestyle='--', label='Current Spot')
ax.set_xlabel("Spot Price")
ax.set_ylabel("Estimated Option Premium")
ax.set_title(f"{stock_name.upper()} {option_type.upper()} Premium Simulation")
ax.legend()
st.pyplot(fig)

# Break-even Calculator
st.subheader("📌 Break-even Spot Level")
if delta != 0:
    break_even_move = option_ltp / abs(delta)
    if option_type == "Call":
        break_even = spot + break_even_move
        st.markdown(f"Break-even (Upside) = ₹{break_even:.2f}")
    else:
        break_even = spot - break_even_move
        st.markdown(f"Break-even (Downside) = ₹{break_even:.2f}")
else:
    st.markdown("Delta is zero; break-even calculation is not possible.")

# What-If Simulator
st.subheader("🔮 What-If Simulator")
custom_move = st.slider("Simulate Spot Move (₹)", -10.0, 10.0, 2.0)
custom_iv_change = st.slider("IV Change (%)", -10.0, 10.0, 0.0)
custom_days = st.slider("Holding Days Simulated", 1, 10, 1)

simulated_theta = abs(theta) * custom_days
simulated_vega = vega * (custom_iv_change / 100)
simulated_delta_gain = custom_move * delta
simulated_gamma = custom_move * gamma * 100
simulated_price = option_ltp + sign * simulated_delta_gain + abs(simulated_gamma) + simulated_vega - simulated_theta

st.markdown(f"**Simulated Premium:** ₹{simulated_price:.2f} after {custom_days} day(s) with ₹{custom_move} move and {custom_iv_change}% IV change") 