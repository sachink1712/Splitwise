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
def get_expenses():
    st.session_state.expenses_submitted = True


if st.session_state.people_added:
    no_of_expenses = st.session_state.get("no_of_expenses", 1)

    if st.session_state.expenses_submitted:
        st.success(f"Number of Expenses: {no_of_expenses}")
    else:
        no_of_expenses = st.number_input("How many expenses?: ", min_value=1, key="no_of_expenses")
        st.button("Add Expense Count", on_click=get_expenses)

    if len(st.session_state.expense_entries) < no_of_expenses:
        st.subheader(f"➕ Add Expense {len(st.session_state.expense_entries) + 1} of {no_of_expenses}")
        amount = st.number_input("Enter Amount: ", min_value=1, key=f"amount_{len(st.session_state.expense_entries)}")
        shared_by = st.multiselect("Split Among", st.session_state.splitwise.names, key=f"people_{len(st.session_state.expense_entries)}")

        if st.button("Add this Expense"):
            if not shared_by:
                st.warning("Please select at least one person.")
            elif amount <= 0:
                st.warning("Amount must be greater than 0")
            else:
                st.session_state.expense_entries.append({"amount": amount,"people": shared_by})
                st.success("Expense Added.")

        if len(st.session_state.expense_entries) == no_of_expenses:
            st.subheader("✅ Submit All Expenses")
            if st.button("Submit All Expenses"):
                for e in st.session_state.expense_entries:
                    st.session_state.splitwise.get_expense(e["amount"],e["people"])
                st.success("All expenses submitted to splitwise")
                st.session_state.expense_entries = []
                st.session_state.expenses_submitted = True

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