
import streamlit as st

from src.database.database import get_all_books
from src.detection.misplaced_checker import check_misplaced_books


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SHELFNEX | Smart Library System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "detection_results" not in st.session_state:
    st.session_state["detection_results"] = []

if "scan_history" not in st.session_state:
    st.session_state["scan_history"] = []


# --------------------------------------------------
# CUSTOM DARK THEME
# --------------------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0b1120;
    color: #e5e7eb;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263449;
}

section[data-testid="stSidebar"] p {
    color: #cbd5e1;
}

/* Headings */
h1, h2, h3 {
    color: #f8fafc !important;
}

/* Normal text */
p, label {
    color: #cbd5e1;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #172338, #111c2e);
    border: 1px solid #293b55;
    padding: 20px;
    border-radius: 14px;
}

/* Metric values */
div[data-testid="stMetricValue"] {
    color: #60a5fa;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
    border: none;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #172338;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
}

/* Dataframes and other bordered elements */
div[data-testid="stDataFrame"] {
    border: 1px solid #293b55;
    border-radius: 10px;
}

/* Divider */
hr {
    border-color: #263449;
}

/* Custom brand panel */
.brand-panel {
    background: linear-gradient(120deg, #172554, #123c70);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #315b91;
    margin-bottom: 24px;
}

.brand-title {
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 2px;
}

.brand-subtitle {
    color: #bfdbfe;
    font-size: 14px;
}

/* Information cards */
.info-panel {
    background-color: #111c2e;
    border: 1px solid #293b55;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.small-muted {
    color: #94a3b8;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

books = get_all_books()
total_books = len(books)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="padding: 12px 0 24px 0;">
        <div style="font-size: 27px; font-weight: 800;
                    color: #60a5fa; letter-spacing: 2px;">
            📚 SHELFNEX
        </div>
        <div style="font-size: 12px; color: #94a3b8;">
            INTELLIGENCE BEYOND THE SHELF
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Book Collection",
            "Scan Shelf",
            "Detection Reports"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown(
        "<p class='small-muted'>SHELFNEX SYSTEM</p>",
        unsafe_allow_html=True
    )

    st.caption("Library Monitoring Prototype")
    st.caption("Version 1.0")


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":

    st.markdown("""
    <div class="brand-panel">
        <div class="brand-title">SHELFNEX</div>
        <div class="brand-subtitle">
            Smart Library Book Monitoring System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("System Overview")

    latest_results = st.session_state["detection_results"]

    scanned_count = len(latest_results)

    misplaced_count = sum(
        1 for book in latest_results
        if book["status"] == "MISPLACED"
    )

    correct_count = sum(
        1 for book in latest_results
        if book["status"] == "CORRECT"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Registered Books", total_books)
    col2.metric("Latest Scan", scanned_count)
    col3.metric("Correctly Placed", correct_count)
    col4.metric("Misplaced Books", misplaced_count)

    st.divider()

    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-panel">
            <h3>📷 Shelf Scanning</h3>
            <p class="small-muted">
                Enter detected book text and check whether
                books are on their registered shelves.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Shelf Scanner", key="dashboard_scan"):
            st.session_state["navigation_target"] = "Scan Shelf"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="info-panel">
            <h3>📖 Book Collection</h3>
            <p class="small-muted">
                Browse the registered books and their
                assigned shelf locations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Book Collection", key="dashboard_books"):
            st.session_state["navigation_target"] = "Book Collection"
            st.rerun()

    st.divider()

    st.subheader("Latest Detection Results")

    if latest_results:

        for book in latest_results:

            if book["status"] == "MISPLACED":
                st.error(
                    f"📕 {book['title']} — "
                    f"Correct shelf: {book['correct_shelf']}"
                )
            else:
                st.success(
                    f"📗 {book['title']} — "
                    f"Correctly placed on {book['correct_shelf']}"
                )

    else:
        st.info("No shelf scanning results yet. Start your first scan.")


# --------------------------------------------------
# BOOK COLLECTION PAGE
# --------------------------------------------------

elif page == "Book Collection":

    st.title("📖 Book Collection")

    st.caption("Browse all books registered in the SHELFNEX database.")

    search = st.text_input(
        "Search books",
        placeholder="Search by title, author or shelf code..."
    )

    filtered_books = []

    for book in books:

        book_id, title, author, isbn, shelf = book

        search_text = (
            f"{title} {author} {shelf} {isbn}"
        ).lower()

        if search.lower() in search_text:
            filtered_books.append({
                "Book Title": title,
                "Author": author,
                "ISBN": isbn if isbn else "Not available",
                "Shelf Code": shelf
            })

    col1, col2 = st.columns(2)

    col1.metric("Total Registered Books", total_books)
    col2.metric("Search Results", len(filtered_books))

    st.divider()

    if filtered_books:

        st.dataframe(
            filtered_books,
            width="stretch",
            hide_index=True
        )

    else:
        st.warning("No matching books found.")


# --------------------------------------------------
# SCAN SHELF PAGE
# --------------------------------------------------

elif page == "Scan Shelf":

    st.title("📷 Shelf Scanner")

    st.caption(
        "Check detected book titles against their registered shelf locations."
    )

    st.markdown("""
    <div class="info-panel">
        <h3>How scanning works</h3>
        <p class="small-muted">
            1. Enter the shelf code being scanned.<br>
            2. Enter the book text detected by OCR.<br>
            3. Press Check Shelf to identify misplaced books.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("shelf_scan_form"):

        shelf_code = st.text_input(
            "Shelf Code",
            placeholder="Example: HISTORY-02"
        )

        ocr_text = st.text_area(
            "Detected Book Text",
            placeholder=(
                "Enter one book title per line...\n"
                "Example:\n"
                "The Silk Road\n"
                "Sapiens"
            ),
            height=180
        )

        submitted = st.form_submit_button(
            "🔍 Check Shelf",
            type="primary"
        )

    if submitted:

        if not shelf_code.strip():
            st.warning("Please enter a shelf code.")

        elif not ocr_text.strip():
            st.warning("Please enter detected book text.")

        else:

            results = check_misplaced_books(
                ocr_text,
                shelf_code
            )

            st.session_state["detection_results"] = results

            st.session_state["scan_history"].append({
                "shelf": shelf_code.strip().upper(),
                "results": results
            })

            st.success("Shelf checking completed!")

    # Display latest results

    results = st.session_state["detection_results"]

    if results:

        st.divider()

        st.subheader("📋 Scan Results")

        misplaced = [
            book for book in results
            if book["status"] == "MISPLACED"
        ]

        correct = [
            book for book in results
            if book["status"] == "CORRECT"
        ]

        col1, col2 = st.columns(2)

        col1.metric("Misplaced Books", len(misplaced))
        col2.metric("Correctly Placed", len(correct))

        for book in results:

            if book["status"] == "MISPLACED":

                st.error(
                    f"📕 {book['title']}\n\n"
                    f"Scanned shelf: {book['scanned_shelf']}\n\n"
                    f"Correct shelf: {book['correct_shelf']}"
                )

            else:

                st.success(
                    f"📗 {book['title']} — "
                    f"Correct shelf: {book['correct_shelf']}"
                )

    else:

        st.info("No detection results yet.")


# --------------------------------------------------
# DETECTION REPORTS PAGE
# --------------------------------------------------

elif page == "Detection Reports":

    st.title("📊 Detection Reports")

    st.caption("Review the results of your shelf scans.")

    history = st.session_state["scan_history"]

    if history:

        st.metric("Total Scans This Session", len(history))

        st.divider()

        for index, scan in enumerate(reversed(history), start=1):

            with st.expander(
                f"Scan {len(history) - index + 1} — {scan['shelf']}"
            ):

                results = scan["results"]

                if not results:
                    st.info("No registered book titles were recognised.")

                for book in results:

                    if book["status"] == "MISPLACED":

                        st.error(
                            f"{book['title']} — "
                            f"Correct shelf: {book['correct_shelf']}"
                        )

                    else:

                        st.success(
                            f"{book['title']} — Correctly placed"
                        )

    else:

        st.info(
            "No scan history available. "
            "Complete a shelf scan to generate a report."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<div style="text-align:center; padding: 12px;">
    <div style="color:#60a5fa; font-weight:700;
                letter-spacing:2px;">
        SHELFNEX
    </div>
    <div style="color:#64748b; font-size:12px;">
        Intelligence Beyond the Shelf | Library Monitoring System
    </div>
</div>
""", unsafe_allow_html=True)
