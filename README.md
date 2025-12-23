✈️ Flights Analytics Dashboard

The Flights Analytics Dashboard is an end-to-end data analytics and visualization project designed to analyze flight pricing patterns and travel trends using a large real-world flight dataset.
The dashboard enables users to search flights, compare prices, apply filters, and explore insightful analytics that help understand airline pricing strategies, route demand, and booking behavior.

The project focuses on business-oriented insights, not just visualizations, and demonstrates a complete pipeline from data processing → cloud database → interactive web app.

📊 Dataset Overview

Records: 300,000+ flight entries

Coverage: Major Indian cities

Key Attributes:

Airline

Source & Destination cities

Departure & Arrival times

Number of stops

Travel class (Economy / Business)

Days left to departure

Ticket price

The dataset represents real-world flight pricing behavior and is suitable for analytics and future ML extensions.

🚀 Features
🔍 Flight Search

Search flights by Source & Destination

Display flight details such as:

Airline

Departure & Arrival time

Stops

Class

Duration

Days left

Price

🎯 Filters

Filter by:

Number of stops (Non-stop / 1 stop / 2+ stops)

Class (Economy / Business)

Validations:

Prevents same source & destination selection

Results shown only after clicking Search

📈 Analytics & Insights

The dashboard includes multiple interactive analytics:

Airline Frequency Analysis
Distribution of flights across airlines (Pie chart)

Busiest Airports / Cities
Identifies cities with the highest incoming & outgoing traffic

Average Price by Airline
Comparison of average ticket prices across airlines

Average Ticket Price vs Days Left to Departure
Shows how prices change as departure date approaches

Average Price by Number of Stops (Economy Class)
Analyzes how stops impact pricing

All charts are interactive, allowing better exploration and storytelling.

🛠️ Tech Stack Used

Python – Core application logic & backend processing

AWS RDS (MySQL) – Cloud-hosted relational database

SQL (Advanced) – Joins, aggregations, subqueries, window functions

Pandas – Data cleaning, transformation, and preparation

Streamlit – Interactive web dashboard & UI

☁️ Architecture Overview
CSV Dataset
     ↓
Pandas (Data Cleaning & Processing)
     ↓
AWS RDS (MySQL)
     ↓
SQL Queries & Analytics
     ↓
Streamlit Dashboard (Deployed)

🔐 Security & Best Practices

No credentials are hardcoded

Database credentials managed using Streamlit Secrets

.env and secrets.toml excluded via .gitignore

Cloud database access handled via AWS security groups

📌 How to Run Locally

Clone the repository

git clone https://github.com/<your-username>/flights-analytics-dashboard.git


Install dependencies

pip install -r requirements.txt


Add secrets locally
Create .streamlit/secrets.toml:

DB_HOST = "your_aws_endpoint"
DB_PORT = "3306"
DB_USER = "admin"
DB_PASSWORD = "your_password"
DB_NAME = "flights_db"


Run the app

streamlit run app.py

🌐 Deployment

Frontend: Streamlit Cloud

Database: AWS RDS (MySQL)

The application is deployed with a live cloud database, enabling real-time querying and analytics.

🧠 Future Enhancements

Price prediction using Machine Learning

Route-wise demand forecasting

User-selectable date ranges

Downloadable reports

Performance optimization with caching

👤 Author

Rajesh Kumar

🔗 LinkedIn: https://www.linkedin.com/in/rajeshkumar-datascience/

💻 GitHub: https://github.com/rajeshxdatascience

⭐ If you like this project, feel free to star the repository and explore the code!
Plotly – Interactive charts & visual analytics

Streamlit Secrets – Secure credential management for cloud deployment

Note - Initially, this project used AWS RDS (MySQL) to simulate a real-world cloud database workflow, including secure credential management, remote connectivity, and advanced SQL querying.

After deployment and validation, the backend was optimized to SQLite, a lightweight file-based relational database, to:

Eliminate unnecessary cloud costs

Improve deployment reliability

Keep the application fully self-contained

The core SQL logic, schema, window functions, and analytics remain unchanged.
This demonstrates flexibility in adapting the same analytical backend across different database environments.