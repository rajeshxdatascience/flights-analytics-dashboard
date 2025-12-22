import pymysql
import streamlit as st

class DB:

    def __init__(self):
        # connect to the database server

        self.conn = pymysql.connect(
            host=st.secrets["DB_HOST"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            database=st.secrets["DB_NAME"],
            port=int(st.secrets["DB_PORT"])
        )

        self.mycursor = self.conn.cursor()

    def fetch_city_names(self):

        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(source_city) FROM new_flights
        UNION
        SELECT DISTINCT(destination_city) FROM new_flights
        """)

        data = self.mycursor.fetchall()
        
        for item in data:
            city.append(item[0])

        return city
    
    def get_flights_filtered(self, source, destination, stops=None, travel_class=None):

        query = """
            SELECT flight, airline, departure_time, stops, arrival_time, 
                class, duration, days_left, price
            FROM (
                SELECT nf.*,
                    ROW_NUMBER() OVER (
                        PARTITION BY flight
                        ORDER BY price ASC, days_left ASC
                    ) AS rn
                FROM new_flights nf
                WHERE source_city = %s
                AND destination_city = %s
        """

        params = [source, destination]

        # dynamic filters
        if stops is not None:
            query += " AND stops = %s"
            params.append(stops)

        if travel_class is not None:
            query += " AND class = %s"
            params.append(travel_class)

        query += """
            ) t
            WHERE rn = 1
            ORDER BY price ASC, days_left ASC;
        """

        self.mycursor.execute(query, tuple(params))
        return self.mycursor.fetchall()

    
    def fetch_airline_frequency(self):

        self.mycursor.execute("""
        SELECT airline AS 'Airline',
        COUNT(*) AS 'Frequency'
        FROM new_flights
        GROUP BY airline
        ORDER BY Frequency DESC
        """)

        return self.mycursor.fetchall()

    def busy_airport(self):

        self.mycursor.execute("""
        SELECT city,
        COUNT(*) AS 'traffic'
        FROM (SELECT source_city AS 'city'
                        FROM new_flights
                        UNION ALL
                        SELECT destination_city AS 'city'
                        FROM new_flights) t
        GROUP BY city
        ORDER BY traffic DESC;
        """)

        return self.mycursor.fetchall()
    
    def avg_price_vs_airline(self):

        self.mycursor.execute("""
        SELECT airline,
        ROUND(AVG(price),2) AS 'avg_price'
        FROM new_flights
        GROUP BY airline
        ORDER BY avg_price DESC; 
        """)

        return self.mycursor.fetchall()
    
    def avg_price_vs_days_left(self):

        self.mycursor.execute("""
        SELECT days_left,
        ROUND(AVG(price),2) AS 'avg_price'
        FROM new_flights
        GROUP BY days_left
        ORDER BY days_left;
        """)

        return self.mycursor.fetchall()
    
    def avg_price_vs_stops(self):

        self.mycursor.execute("""
        SELECT stops,
        ROUND(AVG(price),2) AS 'avg_price'
        FROM new_flights
        WHERE class = 'Economy'
        GROUP BY stops;
        """)

        return self.mycursor.fetchall()