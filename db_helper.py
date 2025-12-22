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
    
    def get_flight_details(self, source, destination):

        query = """
            SELECT flight, airline, departure_time, stops, arrival_time, 
		    class, duration, days_left, price
            FROM ( SELECT nf.*,
                    ROW_NUMBER() OVER (
                    PARTITION BY flight
                    ORDER BY price ASC, days_left ASC) AS rn
		            FROM new_flights nf
		            WHERE source_city = %s
		            AND destination_city = %s) t
        
            WHERE rn = 1;
            """
        self.mycursor.execute(query, (source, destination))
        data = self.mycursor.fetchall()
        return data


    def non_stops(self, source, destination):

        query = """
            SELECT flight, airline, departure_time, stops, arrival_time, 
		    class, duration, days_left, price
            FROM ( SELECT nf.*,
                    ROW_NUMBER() OVER (
                    PARTITION BY flight
                    ORDER BY price ASC, days_left ASC) AS rn
		            FROM new_flights nf
		            WHERE source_city = %s
		            AND destination_city = %s
                    AND stops = 0) t
        
            WHERE rn = 1 AND stops = 0
            ORDER BY price ASC, days_left ASC;
            """
        self.mycursor.execute(query, (source, destination))
        data = self.mycursor.fetchall()
        return data
    
    def one_stops(self, source, destination):

        query = """
            SELECT flight, airline, departure_time, stops, arrival_time, 
		    class, duration, days_left, price
            FROM ( SELECT nf.*,
                    ROW_NUMBER() OVER (
                    PARTITION BY flight
                    ORDER BY price ASC, days_left ASC) AS rn
		            FROM new_flights nf
		            WHERE source_city = %s
		            AND destination_city = %s
                    AND stops = 1) t
        
            WHERE rn = 1 AND stops = 1
            ORDER BY price ASC, days_left ASC;
            """
        self.mycursor.execute(query, (source, destination))
        data = self.mycursor.fetchall()
        return data
    
    def two_stops(self, source, destination):

        query = """
            SELECT flight, airline, departure_time, stops, arrival_time, 
		    class, duration, days_left, price
            FROM ( SELECT nf.*,
                    ROW_NUMBER() OVER (
                    PARTITION BY flight
                    ORDER BY price ASC, days_left ASC) AS rn
		            FROM new_flights nf
		            WHERE source_city = %s
		            AND destination_city = %s
                    AND stops > 1) t
        
            WHERE rn = 1 AND stops > 1
            ORDER BY price ASC, days_left ASC;
            """
        self.mycursor.execute(query, (source, destination))
        data = self.mycursor.fetchall()
        return data
    
    def economy_class(self, source, destination):

        query = """
            SELECT flight, airline, departure_time, stops, arrival_time, 
		    class, duration, days_left, price
            FROM ( SELECT nf.*,
                    ROW_NUMBER() OVER (
                    PARTITION BY flight
                    ORDER BY price ASC, days_left ASC) AS rn
		            FROM new_flights nf
		            WHERE source_city = %s
		            AND destination_city = %s
                    AND class = 'Economy') t
        
            WHERE rn = 1 AND class = 'Economy'
            ORDER BY price ASC, days_left ASC;
            """
        self.mycursor.execute(query, (source, destination))
        data = self.mycursor.fetchall()
        return data
    
    def business_class(self, source, destination):

        query = """
            SELECT flight, airline, departure_time, stops, arrival_time, 
		    class, duration, days_left, price
            FROM ( SELECT nf.*,
                    ROW_NUMBER() OVER (
                    PARTITION BY flight
                    ORDER BY price ASC, days_left ASC) AS rn
		            FROM new_flights nf
		            WHERE source_city = %s
		            AND destination_city = %s
                    AND class = 'Business') t
        
            WHERE rn = 1 AND class = 'Business'
            ORDER BY price ASC, days_left ASC;
            """
        self.mycursor.execute(query, (source, destination))
        data = self.mycursor.fetchall()
        return data
    
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