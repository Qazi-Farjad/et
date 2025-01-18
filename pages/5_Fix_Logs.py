import streamlit as st
import pandas as pd
from db import get_conn
from repos.sqlite import SQLiteLogRepository


# Initialize database and repositories
conn = get_conn()
log_repo = SQLiteLogRepository(conn)

st.title("📜 Raw Logs")

# Fetch all logs
logs = log_repo.get_logs()
if logs:
    logs_df = pd.DataFrame(logs)

    # Initialize session state for tracking deletions
    if "logs_to_delete" not in st.session_state:
        st.session_state.logs_to_delete = set()

    logs_df["Delete"] = False #[log_id in st.session_state.logs_to_delete for log_id in logs_df["id"]]

    # Display the raw logs table
    st.write("**All Logs**")
    edited_df = st.data_editor(
        logs_df,
        key="logs_editor",
        use_container_width=True,
        hide_index=True,
        # num_rows="dynamic",
        column_config={
            "id": {"disabled": True},  # Disable editing for the ID column
            "timestamp": {"disabled": True},  # Disable editing for the timestamp column
            "Delete": {"editable": True},  # Allow editing for the Delete column
        },
    )

    # Update session state with selected logs for deletion
    for index, row in edited_df.iterrows():
        if row["Delete"]:
            st.session_state.logs_to_delete.add(row["id"])
        else:
            st.session_state.logs_to_delete.discard(row["id"])

    # Save changes
    if st.button("Save Changes"):
        # Update the database with the edited logs
        for index, row in edited_df.iterrows():
            log_repo.update_log(
                row["id"],
                row["exercise"],
                row["reps"]
            )
        st.success("Changes saved successfully!")

    # Delete selected logs
    if st.button("Delete Selected Logs"):
        if st.session_state.logs_to_delete:
            for log_id in st.session_state.logs_to_delete:
                log_repo.delete_log(log_id)
            st.success("Selected logs deleted successfully!")
            st.session_state.logs_to_delete = set()  # Clear the deletion set
        else:
            st.warning("No logs selected for deletion.")
            st.session_state.logs_to_delete
else:
    st.info("No logs found.")