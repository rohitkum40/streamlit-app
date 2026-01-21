import streamlit as st
import pandas as pd
import time
# add title
st.title("Startup dashboard")

#add header
st.header("I am learning streamlit")

# add subheader
st.subheader("hi am learning streamlit")

st.write("rohit")

st.markdown("""
### My Favorite Movies
- **Race 3**
- **Humshakals**
- **Housefull 4**
""")

# display code
st.code("""
def foo(input):
    retun foo**2
x = foo(2)
print(x)
""")

# convert into mathmatical symbol
st.latex("""
x^2 + y^2 + 6 = 0
""")


# display datframe

df = pd.DataFrame(
    {
        "name":["rohit","aman","kiran","suman"],
        "marks":[40,20,20,40],
        "package":[10,20,20,10]

    }
)
st.dataframe(df)

st.metric("Revenue","Rs 3L","-3%")


# display json
st.json(
{
        "name":["rohit","aman","kiran","suman"],
        "marks":[40,20,20,40],
        "package":[10,20,20,10]

    }
)

# add media
st.image(r"C:\Users\DELL\OneDrive\Desktop\500-led-temperature-water-bottle-display-iindicator-water-bottle-original-imagzbk5snpy4c6h.webp")
st.video(r"C:\Users\DELL\OneDrive\Desktop\AQMzkht8AVBH8gf1K_DCi3Q1_2UTyihkqAiJryX0VpKzMY94p5P_ya3Jy2S7jVPida5cm_BLARfaLNziiBam5VqJp1iB0_j_mYLEw_SXMQ.mp4")

# sidebar

st.sidebar.title("About")

col1, col2, col3 = st.columns(3)
with col1:
    st.image(r"C:\Users\DELL\OneDrive\Desktop\500-led-temperature-water-bottle-display-iindicator-water-bottle-original-imagzbk5snpy4c6h.webp")
with col2:
    st.image(r"C:\Users\DELL\OneDrive\Desktop\500-led-temperature-water-bottle-display-iindicator-water-bottle-original-imagzbk5snpy4c6h.webp")
with col3:
    st.image(r"C:\Users\DELL\OneDrive\Desktop\500-led-temperature-water-bottle-display-iindicator-water-bottle-original-imagzbk5snpy4c6h.webp")

# print message

st.error("login failed")
st.success("login successful")
st.info("login successful")
st.warning("login successful")


# profress bar

bar = st.progress(0)
for i in range(100):
    #time.sleep(0.1)
    bar.progress(i)


# user input
email = st.text_input("email","")
age = st.number_input("age",0,100)
date = st.date_input("date")
password = st.text_input("password","")


