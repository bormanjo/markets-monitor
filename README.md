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
        - [X] Intraday Plot
        - [X] Historical Plot 
    - Data
        - [X] Intraday data
        - [X] Historical data
        - [ ] Quarterly reporting data
- Market Headlines
    - Visualizations
        - [X] Textual RSS Feed
        - [ ] Wordcloud or sentiment indicators?
    - Data
        - [X] WSJ RSS Feeds
        - [ ] FRED RSS Feeds
        - Others?
- U.S. Economic Data
    - Visualizations
        - [ ] Time Series Plots
        - [ ] YoY/QoQ Changes
    - Data
        - [ ] Quandl/FRED
- Global Economic Data
    - Visualizations
        - [ ] Time Series Plots
        - [ ] YoY/QoQ Changes
    - Data
        - ?