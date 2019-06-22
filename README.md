# markets-monitor

A dashboard monitor for financial and economic markets data

## Overview

This dashboard is meant to provide a **high level** synopsis of activity in domestic (U.S.) and foreign markets. It
seeks to aggregate data across a variety of sources from stock prices to headline news into a single interactive 
platform.

Currently under development.

## Usage

> **Note:** Running this dashboard locally requires docker.

| Objective | Windows | UNIX |
|:---:|:---:|:---:|
| Development | `./run/dev.bat` | `./run/dev.sh` |
| Deployment | `./run/run-app.bat` | `./run/run-app.sh` |
 
 Execute the command above from the project's root directory in your terminal of choice.

## Functionality

- Stock Market Data Feed
    - Visualizations
        - Intraday Plot [X]
        - Historical Plot [X]
    - Data
        - Intraday data [X]
        - Historical data [X]
        - Quarterly reporting data
- Market Headlines
    - Visualizations
        - Textual RSS Feed [X]
        - Wordcloud or sentiment indicators?
    - Data
        - WSJ RSS Feeds [X]
        - FRED RSS Feeds
        - Others?
- U.S. Economic Data
    - Visualizations
        - Time Series Plots
        - YoY/QoQ Changes
    - Data
        - Quandl/FRED
- Global Economic Data
    - Visualizations
        - Time Series Plots
        - YoY/QoQ Changes
    - Data
        - ?