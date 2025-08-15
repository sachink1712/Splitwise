from splitwise import SplitWise
import streamlit as st

if 'splitwise' not in st.session_state:
    st.session_state.splitwise = SplitWise()
if 'people_added' not in st.session_state:
    st.session_state.people_added = False
if 'expenses_submitted' not in st.session_state:
    st.session_state.expenses_submitted = False
if 'expense_entries' not in st.session_state:
    st.session_state.expense_entries = []
if 'split_amount' not in st.session_state:
    st.session_state.split_amount = {}

st.title("💸 Splitwise")

# ----- ADD PEOPLE -----
st.subheader("👥 Add People")


def add_people():
    name_list = [name.strip() for name in st.session_state.name_input.split(",") if name.strip()]
    st.session_state.splitwise.get_people(name_list)
    st.session_state.people_added = True


if not st.session_state.people_added:
    st.text_input("Enter Names (Comma Separated)", key="name_input")
    st.button("Add People", on_click=add_people)
else:
    st.success(f"People Added:  {', '.join(st.session_state.splitwise.names)}")

# ----- ADD EXPENSES -----
def lock_expense_count():
    st.session_state.expenses_submitted = True
    st.session_state.locked_expense_count = st.session_state.temp_expense_count

# 💡 Only proceed if people are added
if st.session_state.people_added:

    # Show number input if not locked yet
    if not st.session_state.expenses_submitted:
        st.number_input("How many expenses?", min_value=1, key="temp_expense_count")
        st.button("✅ Confirm Expense Count", on_click=lock_expense_count)

    # Only continue if locked_expense_count is now set
    if st.session_state.expenses_submitted and "locked_expense_count" in st.session_state:
        no_of_expenses = st.session_state.locked_expense_count
        st.success(f"Number of Expenses: {no_of_expenses}")

        # Add each expense
        if len(st.session_state.expense_entries) < no_of_expenses:
            current_idx = len(st.session_state.expense_entries)
            st.subheader(f"➕ Add Expense {current_idx + 1} of {no_of_expenses}")
            amount = st.number_input("Enter Amount:", min_value=1, key=f"amount_{current_idx}")
            shared_by = st.multiselect("Split Among", st.session_state.splitwise.names, key=f"people_{current_idx}")

            if st.button("Add this Expense", key=f"add_expense_{current_idx}"):
                if not shared_by:
                    st.warning("Please select at least one person.")
                else:
                    st.session_state.expense_entries.append({"amount": amount, "people": shared_by})
                    st.success("Expense Added ✅")
                    # st.experimental_rerun()

        # Submit all
        if len(st.session_state.expense_entries) == no_of_expenses:
            st.subheader("✅ Submit All Expenses")
            if st.button("Submit All Expenses"):
                for e in st.session_state.expense_entries:
                    st.session_state.splitwise.get_expense(e["amount"], e["people"])

                st.success("All expenses submitted.")
                st.session_state.expenses_submitted = False



# --- SHOW ADDED EXPENSES (Preview) ---
if st.session_state.expense_entries:
    st.markdown("### 📝 Total Expenses")
    for idx, e in enumerate(st.session_state.expense_entries, start=1):
        st.write(f"{idx}. ₹{e['amount']:.2f} split among {', '.join(e['people'])}")

# ----- Calculate Split -----
if st.session_state.expense_entries:
    def split_calculation():
        for e in st.session_state.expense_entries:
            split = e['amount']/len(e['people'])
            for each_name in e['people']:
                if each_name in st.session_state.split_amount:
                    st.session_state.split_amount[each_name] += split
                else:
                    st.session_state.split_amount[each_name] = split
        return st.session_state.split_amount


    if st.button("💰 Show Split"):
        split = split_calculation()
        st.subheader("🔄 Split Summary")
        for person, amount in split.items():
            st.markdown(f"<h4 stype='font-size:30px;'><strong>{person.title()}</strong> owes <span style='color:red;'>₹{amount:.2f}</span></h4>", unsafe_allow_html=True)