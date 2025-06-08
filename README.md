# Rogue Option Target Simulator

A Streamlit application that helps option traders simulate realistic price targets and stop loss ranges using option Greeks.

## Features

- Input option Greeks (Delta, Gamma, Theta, Vega)
- Calculate estimated target premium based on expected spot price movement
- Suggest stop loss levels based on risk parameters
- Evaluate option suitability using the Rogue Option Buyer Checklist

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Rogue-Options-Checklist.git
cd Rogue-Options-Checklist
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The app will open in your default web browser, where you can input your option data and view the simulated targets.

## How It Works

The simulator uses option Greeks to calculate:
- Delta-based price movement
- Gamma acceleration effects
- Theta decay over time

The checklist evaluates if an option meets the criteria for a "Rogue Option Buyer" trade:
- Delta between 0.4 and 0.65
- Gamma greater than 0.005
- Theta less than or equal to 0.20
- Vega less than or equal to 0.75 