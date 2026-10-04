from fastapi import FastAPI
import pandas as pd
from fastapi.responses import HTMLResponse

app = FastAPI()

df = pd.read_csv("skin clinic campaign.csv")

df["Response"] = df["Response_to_Campaign"].map({
    "Yes": 1,
    "No": 0
})

df["Product_Usage"] = pd.cut(
    df["Unique_Products_Purchased"],
    bins=[0, 4, 8, float("inf")],
    labels=["1-4", "5-8", ">8"]
)

@app.get("/")
def home():
    return {
        "message": "Skin Clinic Campaign API"
    }

@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():

    gender_response = (
        df.groupby("Gender")["Response"]
          .mean()
          .mul(100)
          .round(2)
          .reset_index(name="Response Rate")
    )

    age_response = (
        df.groupby("AgeGroup")["Response"]
          .mean()
          .mul(100)
          .round(2)
          .reset_index(name="Response Rate (%)")
    )

    purchase_response = (
        df.groupby("Purchase_Last_Quarter")["Response"]
          .mean()
          .mul(100)
          .round(2)
          .reset_index(name="Response Rate (%)")
    )
    product_response = (
        df.groupby("Product_Usage", observed=True)["Response"]
            .mean()
            .mul(100)
            .round(2)
            .reset_index(name="Response Rate (%)")
)

    return f"""
<html>
    <head>
        <title>Campaign Analysis</title>
    </head>

    <body>
        <h1>Skin Clinic Campaign Analysis</h1>

        <h2>Gender vs Campaign Response</h2>
        {gender_response.to_html(index=False)}

        <h2>Age Group vs Campaign Response</h2>
        {age_response.to_html(index=False)}

        <h2>Purchase in Last Quarter vs Campaign Response</h2>
        {purchase_response.to_html(index=False)}

        <h2>Product Usage vs Campaign Response</h2>
        {product_response.to_html(index=False)}
    </body>
</html>
"""