navbar = """
    <style>

    .st-emotion-cache-1cvow4s a{
    text-decoration: none;
    
    }


        .stAppHeader{
            display:none}
        .navbar {
            background-color: #d8d9da; 
            padding: 15px 20px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .navbar-logo {
            max-height: 40px;  /* Set logo size */
        }

        .navbar-link {
            font-size: 18px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            text-transform: uppercase;
        }

        .navbar-link:hover {
            color: #1f83c5;  /* Lighter blue for hover */
            text-decoration: none
        }

        /* To avoid the navbar overlapping the content */
        body {
            padding-top: 60px;
        }
    </style>
    
    <nav class="navbar">
        <div >
            <img src="https://sunway.edu.np/wp-content/uploads/2025/01/site-logo.png" alt="Logo" class="navbar-logo" style="margin-left: 3rem;">
        </div>
        <div>
        <a href="https://sunway.edu.np/" target="_self" class="navbar-link" style="margin-right: 3rem;">Home</a>
        </div>

    </nav>
"""

background_image ='https://www.snhu.edu/-/media/images/masthead-image/fourtypesofcollegedegrees-banner.ashx?h=340&w=890&hash=6DDD09080AC87C3778189E3E9FCCAFAF'
background_style = f"""
        <style>
        .stApp {{
            background-image: url("{background_image}");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }}

        /* Create a semi-transparent overlay */
        .stApp::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgb(8, 10, 18);
            opacity: 0.90;  /* Adjust opacity (50%) */
            pointer-events: none;  /* Allows interactions with content below */
        }}


        .stButton, .stTextInput, .stSelectbox, .stRadio, .stCheckbox, .stSlider {{
            z-index: 2;
        }}
        </style>
        """

rewrite_default_css = """
        <style>
            .st-emotion-cache-b0y9n5 {
                border-radius:0rem;
                border-top-right-radius: 0.5rem;
                border-bottom-right-radius: 0.5rem;

                border-top: 2px solid rgba(250, 250, 250, 0.2);  /* Border on top */
                border-right: 2px solid rgba(250, 250, 250, 0.2);  /* Border on left */
                border-bottom: 2px solid rgba(250, 250, 250, 0.2);  /* Border on bottom */

                height: 2.66rem;
                background-color:#262730;

            }
            .st-emotion-cache-ocqkz7{
                gap: 0rem;
                }

            .st-b7{
                background-color:transparent;
                
                }
            .st-aw {
                border-bottom-right-radius:0rem;

                border-top: 2px solid rgba(250, 250, 250, 0.2);  /* Border on top */
                border-left: 2px solid rgba(250, 250, 250, 0.2);  /* Border on left */
                border-bottom: 2px solid rgba(250, 250, 250, 0.2);  /* Border on bottom */
                }
            .st-av{
                border-top-right-radius:0rem;}

            .st-emotion-cache-yw8pof{
                z-index:2;
                }
        </style>
    """


def question_template(question):
      return f"""
                <div style="
                background-color:rgba(51,51,51,1);
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
                margin-right: 3rem;
                margin-left: 8rem;
                background-color: rgb(8, 10, 18)">
                <span style="padding-left: 20px;">{question}</span>
                </div>
                """

def response_template(response):
    return f"""
            <div style="background-color:#262730; color: white; padding: 10px; border-radius: 5px; margin-right: 3rem;">
                {response}
            </div>
            <br>"""
