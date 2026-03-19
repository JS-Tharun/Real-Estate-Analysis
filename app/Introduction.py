import streamlit as st

st.set_page_config(
    page_title='🏙 BrickView',
    layout='wide'
)


def main():
    with st.container():
        st.title("BrickView 🌇")
        st.write("## Data-Driven Insights for Property Buyers, Investors, and Sales Agents ✅")
        st.write("An interactive real estate analytics dashboard that helps analyze:")
        st.markdown("""
            
            ### 🏠 Analyze Property Listings
            * Explore real estate listings by location, price range, property type, and other key attributes.

            ### 📊💸 Understand Pricing Trends
            * Identify how property prices vary across cities and neighborhoods.

            ### 🕔 Monitor Time on Market
            * Understand how long properties remain listed before being sold.

            ### 👨‍💼 Evaluate Agent Performance

            Track agent activity and performance based on listings and completed sales.

            ### 📍 Explore Property Locations

            Use the interactive map to visualize property listings geographically.

        """)
        st.divider()

        st.markdown(f"""

            ### How to Use This App

            1️⃣ Navigate through the pages using the sidebar menu

            2️⃣ Apply filters such as:

            * Location, Property Type, Price Range, Sqft Range, etc

            * Amenities such as furnishing, parking space availability, power backup, etc

            * Sales Agent

            * Buyers

            3️⃣ Explore the interactive charts and tables to discover insights.

            4️⃣ Identify the top performing agents in the Agents Performance Page.

            5️⃣ Run predefined SQL queries to investigate deeper analytics.

            6️⃣ Use the data management section to modify the underlying database records.
        """)

        st.divider()

        st.markdown("""
            ### Pages Overview

            | Page | Description |
            | ---- | ----------- |
            | Dashboard 📊| Interactive charts and filters to explore real estate trends |
            | SQL Queries 📑| Run predefined SQL queries to analyze data directly |
            | Data Management 📂| Create, update, view, and delete records in database tables |
            | Creator Info 🧑‍💻| About the creator of the project |
        """)

if __name__ == "__main__":
    main()