import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data_from_excel():

    df=pd.read_excel("C:\\Users\\gulsh\\Desktop\\sales_analysis\\supermarkt_sales.xlsx",
            sheet_name="Sales",
            skiprows=3,
            usecols="B:R",
            nrows=1000,)
    #print(df)
 # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df=get_data_from_excel()
#st.dataframe(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender")

#st.dataframe(df_selection)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)




left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
#st.plotly_chart(fig_product_sales)
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown("""---""")

# Donut Chart for Sales by Gender
sales_by_gender = df_selection.groupby(by=["Gender"])[["Total"]].sum()
fig_donut = px.pie(
    sales_by_gender,
    values="Total",
    names=sales_by_gender.index,
    title="<b>Sales by Gender</b>",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Blues
)
fig_donut.update_traces(textinfo='percent+label')

# Pie Chart for Sales by Customer Type
sales_by_customer_type = df_selection.groupby(by=["Customer_type"])[["Total"]].sum()
fig_pie = px.pie(
    sales_by_customer_type,
    values="Total",
    names=sales_by_customer_type.index,
    title="<b>Sales by Customer Type</b>",
    color_discrete_sequence=px.colors.sequential.RdBu
)
fig_pie.update_traces(textinfo='percent+label')

# Line Chart for Sales Over Time (by Date)
df_selection['Date'] = pd.to_datetime(df_selection['Date'])
sales_by_date = df_selection.groupby(by=["Date"])[["Total"]].sum()
fig_line = px.line(
    sales_by_date,
    x=sales_by_date.index,
    y="Total",
    title="<b>Sales Over Time</b>",
    color_discrete_sequence=["#0083B8"]
)
fig_line.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    plot_bgcolor="rgba(0,0,0,0)"
)

# Treemap for Sales by Product Line
fig_treemap = px.treemap(
    df_selection,
    path=['Product line'],
    values='Total',
    title='<b>Sales Distribution by Product Line</b>',
    color='Total',
    color_continuous_scale='RdBu'
)

# Sunburst Chart for Sales by City, Customer Type, and Gender
fig_sunburst = px.sunburst(
    df_selection,
    path=['City', 'Customer_type', 'Gender'],
    values='Total',
    title='<b>Sales Distribution by City, Customer Type, and Gender</b>',
    color='Total',
    color_continuous_scale='RdBu'
)

# Bubble Chart for Sales, Unit Price, and Quantity by Product Line
fig_bubble = px.scatter(
    df_selection,
    x='Unit price',
    y='Quantity',
    size='Total',
    color='Product line',
    hover_name='Product line',
    title='<b>Sales, Unit Price, and Quantity by Product Line</b>',
    size_max=60,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Plot additional charts
#st.markdown("## Additional Visualizations")
donut_column, pie_column = st.columns(2)
donut_column.plotly_chart(fig_donut, use_container_width=True)
pie_column.plotly_chart(fig_pie, use_container_width=True)

treemap_column, sunburst_column = st.columns(2)
treemap_column.plotly_chart(fig_treemap, use_container_width=True)
sunburst_column.plotly_chart(fig_sunburst, use_container_width=True)

st.plotly_chart(fig_line, use_container_width=True)
st.plotly_chart(fig_bubble, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
