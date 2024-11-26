import streamlit as st
import streamlit as st
import time
from st_pages import Page, show_pages, add_page_title



def login(username, password):
    users = {
        "admin": "123456",
        "justbooks_analyst": "123456",
        "justbooks_salesoperator": "123456",
        "truly_analyst": "123456",
        "analyst": "123456",
    }
    print(users.get(username) == password)
    return username if users.get(username) == password else False







def configure_user_pages(username_value):
    pages_dict = {
        "admin@chai": [
            ("demo_login_page.py", "Logout", "↪"),
            ("pages/app.py", "App", "🍵")
        ],
        "analyst@justbooks": [
            ("demo_login_page.py", "Logout", "↪"),
            ("pages/analyst_app.py", "App", "🍵")
        ],
        "salesoperator@justbooks": [
            ("demo_login_page.py", "Logout", "↪"),
            ("pages/salesoperator_app.py", "App", "🍵")
        ],
        "analyst@truly": [
            ("demo_login_page.py", "Logout", "↪"),
            ("pages/truly_app.py", "App", "🍵")
        ]
    }

    if username_value in pages_dict:
        pages = pages_dict[username_value]
        show_pages([Page(page[0], page[1], page[2]) for page in pages])
        return pages[-1][0]  # Return the path of the app page to switch to

def handle_login(username, password):
    username_value = login(username, password)
    if username_value:
        st.success(f"User '{username}' logged in successfully!")
        st.empty()
        app_page = configure_user_pages(username_value)
        # Display a spinner for 2 seconds before redirecting
        with st.spinner("Configuring your persona, please wait.."):
            time.sleep(5)  # Introduce a 2-second delay
            st.caption("Redirecting...")
            st.switch_page(app_page)
    else:
        st.error("Invalid username or password")




def main():
    st.set_page_config(
        page_title="Insights Over ChAI",
        page_icon="🍵",
        layout="centered", #wide
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https:///',
            'About': "Made with 🍵 by Team"
        }
        )
   
    #st.title("Channel AI - CHAI 🍵")
    #kk=st.logo("chailogo.png", link="https://streamlit.io/gallery", icon_image="chailogo.png")
    #st.markdown("<h1 style='text-align: center; color: red;'>{kk}</h1>", unsafe_allow_html=True)
    st.header("Insights over ChAI 🍵",divider="rainbow")
    #st.image('chailogo.png', clamp=True,width=300)

    st.logo("chailogo.png", link="https://insightsoverchai.com", icon_image="chailogo.png")
    st.subheader("User Login")
    st.caption("""<div style='position: fixed; bottom: 0px; right: 10px;'><p>Made with 🍵 by Team ChAI</p></div>""", unsafe_allow_html=True)
    st.caption("""<div style='position: fixed; bottom: 13px; right: 10px;'><p>Version Login Page</p></div>""", unsafe_allow_html=True)
    #st.caption("""<div style='position: fixed; bottom: 18px; right: 10px;'><p>Version v2.0.9</p></div>""", unsafe_allow_html=True)
    st.caption("""<div style='position: fixed; bottom: 27px; right: 10px;'><p>Vanilla Version</p></div>""", unsafe_allow_html=True)

    import base64

    @st.cache_data 
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    
    img = get_img_as_base64("mainmain.jpg")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: 180%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    





    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    with st.container(border=True):
        username = st.text_input("Username")  # Adjust width as per your requirement
        password = st.text_input("Password", type="password")  # Adjust width as per your requirement



    show_pages(
    [   
        Page("insightsoverchai.py"),
    ]
)
    


    if st.button("Login"):

        username_value=login(username, password)


        




        if (username_value=='analyst'):
            show_pages(
                [   
                    Page("insightsoverchai.py","Logout","↪"),
                    Page("pages/modular_code_01.py", "App", "🍵"),
                ]
            )
            
            st.success(f"User '{username}' logged in successfully!")

            with st.spinner("Configuring your persona, please wait.."):
                time.sleep(5)  
                st.caption("Redirecting...")
                st.switch_page("pages/modular_code_01.py")

        # elif (username_value=='admin'):
        #     show_pages(
        #         [   
        #             Page("insightsoverchai.py","Logout","↪"),
        #             Page("pages/app.py", "App", "🍵"),
        #         ]
        #     )
            
        #     st.success(f"User '{username}' logged in successfully!")
        #     with st.spinner("Configuring your persona, please wait.."):
        #         time.sleep(5) 
        #         st.caption("Redirecting...")
        #         st.switch_page("pages/app.py")


        # elif (username_value=='justbooks_salesoperator'):
        #     show_pages(
        #         [   
        #             Page("insightsoverchai.py","Logout","↪"),
        #             Page("pages/salesoperator_app.py", "App", "🍵"),
        #         ]
        #     )
            
        #     st.success(f"User '{username}' logged in successfully!")

        #     with st.spinner("Configuring your persona, please wait.."):
        #         time.sleep(5) 
        #         st.caption("Redirecting...")
        #         st.switch_page("pages/salesoperator_app.py")




        # elif (username_value=='truly_analyst'):
        #     show_pages(
        #         [   
        #             Page("insightsoverchai.py","Logout","↪"),
        #             Page("pages/truly_app.py", "App", "🍵"),
        #         ]
        #     )
            

        #     st.success(f"User '{username}' logged in successfully!")

        #     with st.spinner("Configuring your persona, please wait.."):
        #         time.sleep(5)  
        #         st.caption("Redirecting...")
        #         st.switch_page("pages/truly_app.py")

        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()


    
