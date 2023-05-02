import streamlit as st
from database.user_database import UserDatabase
from utils.diet_plan import ask_diet_plan_questions, generate_diet_plan, store_diet_plan_to_vector_db



def main():
    user_db = UserDatabase("users.db")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.header("Login or Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if user_db.validate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

        with st.expander("Register"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif user_db.user_exists(new_username):
                    st.error("Username already exists")
                else:
                    user_db.add_user(new_username, new_password, diet_plan=None)
                    st.success("User registered successfully!")

    else:
        username = st.session_state.user
        diet_plan = user_db.get_user_diet_plan(username)

        if diet_plan:
            col1, col2, col3 = st.columns(3)
            if col1.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.experimental_rerun()
            if col2.button("Ask additional questions"):
                user_input = ask_diet_plan_questions()
                st.experimental_rerun()
            if col3.button("Update diet plan"):
                # Placeholder for update functionality
                st.experimental_rerun()
            st.header("Your Diet Plan")
            st.write(diet_plan)
        else:
            st.header("Answer the following questions to generate your personalized diet plan")
            user_input = ask_diet_plan_questions()
            
            if st.button("Generate Diet Plan"):
                with st.spinner("Generating Diet Plan..."):
                    diet_plan = generate_diet_plan(user_input)
                    store_diet_plan_to_vector_db((username, diet_plan))
                    user_db.update_diet_plan(username, diet_plan)
                st.write(diet_plan)
                st.success("Diet plan has been generated and stored in the vector database!")
                st.experimental_rerun()

if __name__ == "__main__":
    main()