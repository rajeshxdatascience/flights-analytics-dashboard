import streamlit as st
import pandas as pd
from db_helper import DB
import plotly.express as px

db = DB()

st.set_page_config(layout='wide')

st.sidebar.title("✈️ Flights Analytics")
st.sidebar.caption("Search & analyze flight prices")

user_option = st.sidebar.selectbox('Navigation',['Select One','Check Flights','Analytics'])

if user_option == 'Select One':
    st.info("Please choose an option from the sidebar")

if user_option == 'Check Flights':
    st.title('Cheapest Flights for Selected Route')

    st.caption(
    "Showing the lowest available price per flight for the selected source and destination.")

    st.markdown("### ✈️ Flight Details")



    col1,col2 = st.columns(2)
    city = db.fetch_city_names()

    cities = ["-- Select Source --"] + sorted(city)
    destinations = ["-- Select Destination --"] + sorted(city)

    with col1:
        source = st.selectbox('Source',cities)
    with col2:
        destination = st.selectbox('Destination',destinations)

    if "search_clicked" not in st.session_state:
        st.session_state.search_clicked = False

    if st.button('Search'):
            st.session_state.search_clicked = True

    st.subheader("Filters")

    stops_option = st.selectbox(
        "Stops",
        ["All", "Non-stop", "1 Stop", "2+ Stops"])
    
    class_option = st.selectbox(
        "Class",
        ["All", "Economy", "Business"])
    

    if st.session_state.search_clicked:

        if source == '-- Select Source --' or destination == '-- Select Destination --':
            st.warning('Please select both source and destination')


        elif source == destination:
            st.warning('Source and Destination cannot be same')

        else:
            st.caption(
            f"Route: {source} → {destination} | Stops: {stops_option} | Class: {class_option}")

            if class_option == 'Economy':
                columns1 = [
                    "Flight",
                    "Airline",
                    "Departure Time",
                    "Stops",
                    "Arrival Time",
                    "Class",
                    "Duration (hrs)",
                    "Days Left",
                    "Price (₹)"
                    ]
                results = db.economy_class(source,destination)
                df = pd.DataFrame(results, columns=columns1)
                st.dataframe(df,height=500)

                st.success(f"{len(df)} Economy class flights found.")

                if len(df) == 0:
                    st.warning("No Economy class flights available for the selected route.")

                st.info("Change filters or route to update results.")

            elif class_option == 'Business':
                columns1 = [
                    "Flight",
                    "Airline",
                    "Departure Time",
                    "Stops",
                    "Arrival Time",
                    "Class",
                    "Duration (hrs)",
                    "Days Left",
                    "Price (₹)"
                    ]
                results = db.business_class(source,destination)
                df = pd.DataFrame(results, columns=columns1)
                st.dataframe(df,height=500)

                st.success(f"{len(df)} Business class flights found.")

                if len(df) == 0:
                    st.warning("No Business class flights available for the selected route.")

                st.info("Change filters or route to update results.")

            elif stops_option == 'Non-stop':
                columns1 = [
                    "Flight",
                    "Airline",
                    "Departure Time",
                    "Stops",
                    "Arrival Time",
                    "Class",
                    "Duration (hrs)",
                    "Days Left",
                    "Price (₹)"
                    ]
                results = db.non_stops(source,destination)
                df = pd.DataFrame(results, columns=columns1)
                st.dataframe(df,height=500)

                st.success(f"{len(df)} flights found for this route")

                if len(df) == 0:
                    st.warning("No flights available for the selected route")

                st.info("Change filters or route to update results.")

            elif stops_option == '1 Stop':
                columns1 = [
                    "Flight",
                    "Airline",
                    "Departure Time",
                    "Stops",
                    "Arrival Time",
                    "Class",
                    "Duration (hrs)",
                    "Days Left",
                    "Price (₹)"
                    ]
                results = db.one_stops(source,destination)
                df = pd.DataFrame(results, columns=columns1)
                st.dataframe(df,height=500)

                st.success(f"{len(df)} flights found for this route")

                if len(df) == 0:
                    st.warning("No flights available for the selected route")

                st.info("Change filters or route to update results.")

            elif stops_option == '2+ Stops':
                columns1 = [
                    "Flight",
                    "Airline",
                    "Departure Time",
                    "Stops",
                    "Arrival Time",
                    "Class",
                    "Duration (hrs)",
                    "Days Left",
                    "Price (₹)"
                    ]
                results = db.two_stops(source,destination)
                df = pd.DataFrame(results, columns=columns1)
                st.dataframe(df,height=500)

                st.success(f"{len(df)} flights found for this route")

                if len(df) == 0:
                    st.warning("No flights available for the selected route")

                st.info("Change filters or route to update results.")

            else:
                columns = [
                    "Flight", "Airline", "Departure Time", "Stops",
                    "Arrival Time", "Class", "Duration (hrs)",
                    "Days Left", "Price (₹)"
                ]

                results = db.get_flight_details(source, destination)
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df,height=500)

                st.success(f"{len(df)} flights found for this route")

                if len(df) == 0:
                    st.warning("No flights available for the selected route")

                st.info("Change filters or route to update results.")

    
    
elif user_option == 'Analytics':

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✈️ Flight Distribution by Airline")
        st.caption("Total flights in dataset: 300,153")
    
        data = db.fetch_airline_frequency()
        df = pd.DataFrame(data, columns=["Airline", "Frequency"])

        fig = px.pie(df,
        names="Airline",
        values="Frequency",
        hole=0.4)

        fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Flights: %{value}<br>Share: %{percent}")


        st.plotly_chart(fig, use_container_width=True)

        st.info("Vistara and Air India together account for the majority of flights in the dataset.")

    with col2:
        st.subheader("🏙️ Busiest Cities by Flight Traffic")
        st.caption("Based on arrival + departure traffic")

        data = db.busy_airport()
        df = pd.DataFrame(data, columns=["City", "Traffic"])

        fig = px.bar(
            df,
            x="Traffic",
            y="City",
            orientation="h",
            text="Traffic"
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info(
        "Metro cities dominate air traffic, highlighting their role as major aviation hubs.")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Average Ticket Price by Airline")
        st.caption(
            "This chart compares the mean airfare across airlines, "
            "highlighting pricing differences between full-service and low-cost carriers.")

        airlines, prices = zip(*db.avg_price_vs_airline())

        fig = px.bar(
            x=prices,
            y=airlines,
            orientation="h",
            labels={"x": "Average Price (₹)", "y": "Airline"}
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info("✈️ Full-service airlines like Vistara and Air India tend to have higher "
                "average fares, while low-cost carriers remain budget-friendly.")



    with col2:
        
        st.subheader("🛑 Average Ticket Price by Number of Stops (Economy Class)")
        st.caption("Economy-class airfare comparison based on the number of stops")

        stops, prices = zip(*db.avg_price_vs_stops())

        stops = ["Non-stop" if s == 0 else "1 Stop" if s == 1 else "2+ Stops" for s in stops]

        fig = px.bar(
            x=prices,
            y=stops,
            orientation="h",
            labels={"x": "Average Price (₹)", "y": "Stops"}
        )

        st.plotly_chart(fig, use_container_width=True)

        fig.update_layout(yaxis=dict(categoryorder="array", categoryarray=stops))


        st.info("Economy-class flights with more stops tend to be more expensive, "
                "as additional segments increase total travel distance and cost.")


    st.subheader("📈 Average Ticket Price vs Days Left to Departure")
    st.caption("Average airfare trend based on number of days left before departure")

    data = db.avg_price_vs_days_left()

    days_left = [row[0] for row in data]
    avg_price = [row[1] for row in data]

    fig = px.line(
        x=days_left,
        y=avg_price,
        markers=True,
        labels={
            "x": "Days Before Departure",
            "y": "Average Price (₹)"
        }
    )

    fig.update_layout(
        xaxis=dict(autorange="reversed"), 
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.info(
    "📈 Ticket prices generally increase as the departure date approaches. "
    "Booking flights earlier can lead to significant cost savings.")


else:
    st.title("✈️ Flights Analytics Dashboard")

    st.subheader("🧭 How to Use")
    st.markdown("Use the sidebar to navigate between Check Flights and Analytics sections.")

    st.subheader("📌 Project Overview")
    st.markdown("""
                <p style="font-size:16px; line-height:1.6;">
                The Flights Analytics Dashboard is an end-to-end data analytics project designed to analyze flight pricing patterns and 
                travel trends using real-world flight data. It enables users to search flights, compare prices, and derive actionable insights
                related to airline pricing, booking behavior, and route demand. The dashboard is built with a strong focus on business-oriented
                insights rather than just visualization.

                The analysis is based on a large-scale real-world flight dataset containing 300,000+ flight records across major Indian cities, ensuring realistic patterns, meaningful trends, and data-driven decision-making.
                """, unsafe_allow_html = True)
    
    st.divider()
    
    st.subheader("🎯 Key Objectives")
    st.markdown(
    """
    <ul style="font-size:16px; line-height:1.8;">
        <li>Help users find the cheapest flights between selected routes</li>
        <li>Analyze how airlines, stops, and booking time impact ticket prices</li>
        <li>Provide data-driven insights for smarter flight booking decisions</li>
    </ul>
    """,unsafe_allow_html=True)

    st.divider()
    
    st.markdown(
    """
    <p style="font-size:32px; font-weight:600; margin-top:20px;">
    🧭 What’s Inside the Project?
    </p>
    """,unsafe_allow_html=True)

    st.subheader("🔍 1. Flight Search & Filters")
    st.markdown(
    """
    <ul style="font-size:16px; line-height:1.8;">
        <li><b>Search flights</b> by <b>Source → Destination</b></li>
        <li><b>View the cheapest available flight</b> for each route</li>
        <li><b>Apply filters:</b>
            <ul>
                <li>Number of stops</li>
                <li>Economy / Business class</li>
            </ul>
        </li>
        <li><b>Smart validations</b> (same source &amp; destination, empty selections, etc.)</li>
    </ul>
    """, unsafe_allow_html=True)

    st.subheader("📊 2. Market & Traffic Analysis")

    st.markdown(
        """
        <ul style="font-size:16px; line-height:1.8;">
            <li>
                <b>Flight Distribution by Airline</b><br>
                Understand which airlines dominate the market.
            </li>
            <li>
                <b>Busiest Cities by Flight Traffic</b><br>
                Identifies major aviation hubs based on combined arrivals and departures.
            </li>
        </ul>
        """,unsafe_allow_html=True)
    
    st.subheader("💰 3. Pricing Analysis")
    
    st.markdown(
        """
        <ul style="font-size:16px; line-height:1.8;">
            <li>
                <b>Average Ticket Price by Airline</b><br>
                Highlights pricing differences between full-service and low-cost carriers.
            </li>
            <li>
                <b>Average Ticket Price by Number of Stops (Economy Class)</b><br>
                Shows how convenience impacts pricing in economy travel.
            </li>
        </ul>
        """,unsafe_allow_html=True)
    
    st.subheader("📈 4. Booking Strategy Insight (Key Highlight)")

    st.markdown(
    """
    <p style="font-size:16px; line-height:1.6;">
    <b>Average Ticket Price vs Days Left to Departure</b><br>

    Reveals a clear trend:
    <ul>
        <li>Ticket prices generally increase as the departure date approaches</li>
        <li>Early booking can lead to significant cost savings</li>
    </ul>

    This section acts as the <b>final insight</b> of the dashboard.
    </p>
    """,unsafe_allow_html=True)

    st.subheader("🧠 Business Insights Delivered")

    st.markdown(
    """
    <ul style="font-size:16px; line-height:1.8;">
        <li>Full-service airlines generally have higher average fares</li>
        <li>Metro cities dominate air traffic in India</li>
        <li>Economy flights with more stops tend to be costlier</li>
        <li>Early booking significantly reduces ticket prices</li>
    </ul>
    """,unsafe_allow_html=True)

    st.subheader("🛠️ Tech Stack Used")

    st.markdown(
    """
    <ul style="font-size:16px; line-height:1.8;">
        <li><span style="font-size:17px; font-weight:600;">Python</span> – Core logic & data handling</li>
        <li><span style="font-size:17px; font-weight:600;">MySQL</span> – Database for storing and querying flight data</li>
        <li><span style="font-size:17px; font-weight:600;">SQL (Advanced)</span> – Joins, aggregations, window functions</li>
        <li><span style="font-size:17px; font-weight:600;">Pandas</span> – Data processing</li>
        <li><span style="font-size:17px; font-weight:600;">Streamlit</span> – Interactive dashboard & UI</li>
        <li><span style="font-size:17px; font-weight:600;">Plotly</span> – Interactive charts & visual analytics</li>
        <li><span style="font-size:17px; font-weight:600;">dotenv</span> – Secure environment variable handling</li>
    </ul>
    """,unsafe_allow_html=True)

    st.subheader("📂 Project Highlights")

    st.markdown(
    """
    <ul style="font-size:16px; line-height:1.8;">
        <li>Clean modular code (DB layer + UI layer)</li>
        <li>Optimized SQL queries for performance</li>
        <li>Industry-style dashboard layout</li>
        <li>Analytics-first approach (not just charts)</li>
    </ul>
    """,unsafe_allow_html=True)

    st.subheader("🔗 Connect & Explore More")

    st.markdown(
    """
    <p style="font-size:16px; line-height:1.6;">
    <b>GitHub:</b> 
    <a href="https://github.com/rajeshxdatascience/movie-review-sentiment.git" target="_blank">
        github.com/rajeshxdatascience
    </a><br>

    <b>LinkedIn:</b> 
    <a href="https://www.linkedin.com/in/rajeshkumar-datascience/" target="_blank">
        linkedin.com/in/rajeshkumar-datascience
    </a><br>

    This project is built for learning, showcasing analytics skills, and demonstrating
    practical data-driven thinking.
    </p>
    """,unsafe_allow_html=True)

    st.subheader("✅ Final Note")

    st.markdown("" \
    "This dashboard reflects real-world data analysis workflows, combining SQL, Python, and visualization to solve practical problems.")