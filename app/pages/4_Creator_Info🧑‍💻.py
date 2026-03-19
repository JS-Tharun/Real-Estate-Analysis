import streamlit as st

st.write("# 🧑‍💻Creator of this Project")

col1, col2 = st.columns([1,5])

with col1:
  with st.container():
    with st.container(horizontal_alignment='left'):
      st.image("images/dp.jpg", width=250)
      
      st.link_button("**Go to LinkedIn 🧰**", "https://linkedin.com/in/tharun-j-s")
      st.link_button("**Go to Github 💻**", "https://github.com/JS-Tharun")
      st.link_button("**View Resume 📄**", "https://tharun-j-s-resume.tiiny.site")

    

with col2:
  st.write("## Tharun J S - Machine Learning Engineer")
  st.write("""
    ### About Creator:

    1+ yrs of experience in Data Oriented **Machine Learning Engineering**, specialized in EDA, Feature Engineering, Model Optimization, Neural Networks and Edge Machine Translation. Proficient in Python, SQL, Tensorflow and edge MLOps including data preprocessing, model training, model evaluation and deployment in mobile devices.

    Hands-on experience in architecting end-to-end revenue operations pipelines for a software application using Chargebee and Razorpay, spanning customer onboarding and retention through the generation of predictable recurring revenue.

    ### Skills Used:
    * **Langauges:** Python, SQL
    * **Libraries & Tools:** Pandas, Numpy, Matplotlib, Seaborn, Plotly, Altair, Streamlit, MySQL Connector
    * **Database:** : MySQL


  """)
