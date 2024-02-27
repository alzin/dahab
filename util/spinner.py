import streamlit as st


class Spinner:
    @staticmethod
    def _load_css():
        """Load the CSS for the spinner and overlay."""
        css = """
        <style>
        .overlay {
            position: fixed;
            display: none;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            right: 0;
            background-color: rgba(0,0,0,0);
            z-index: 2;
            cursor: progress;
        }

        .spinner {
            margin: 0;
            position: fixed;
            top: 40%;
            left: 48%;
            -ms-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
            border: 8px solid #f3f3f3;
            border-radius: 50%;
            border-top: 8px solid #3498db;
            width: 60px;
            height: 60px;
            -webkit-animation: spin 2s linear infinite;
            animation: spin 2s linear infinite;
        }

        .alert-message {
            position: fixed;
            top: 55%;
            left: 50%;
            -ms-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
            color: white;
            font-size: 20px;
            text-align: center;
        }

        @-webkit-keyframes spin {
            0% { -webkit-transform: rotate(0deg); }
            100% { -webkit-transform: rotate(360deg); }
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    @staticmethod
    def show(message="Please wait..."):
        """Show the spinner with an optional message."""
        Spinner._load_css()
        overlay_html = f"""
        <div class="overlay" style="display: block;">
            <div class="spinner"></div>
            <div class="alert-message">{message}</div>
        </div>
        """
        st.markdown(overlay_html, unsafe_allow_html=True)
        # Using session state to track the spinner state
        st.session_state.spinner_visible = True

    @staticmethod
    def remove():
        """Remove the spinner if it's showing."""
        if st.session_state.get('spinner_visible', False):
            hide_script = """
            <script>
            document.querySelector('.overlay').style.display = 'none';
            </script>
            """
            st.markdown(hide_script, unsafe_allow_html=True)
            st.session_state.spinner_visible = False
