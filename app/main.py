import streamlit as st

st.set_page_config(
    page_title='BrickView Analysis'
)


def main():

    st.sidebar.text("Hello")

    st.title("BrickView Analysis")
    st.markdown("""
        * Track listing performance, pricing trends, sales velocity, and agent effectiveness. 

        * Use the sidebar filters to focus on specific cities, price bands, property types, or agents. 

        """
    )

if __name__ == "__main__":
    main()