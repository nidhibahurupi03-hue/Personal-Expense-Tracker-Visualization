def generate_insights(df, prediction):

    insights = []

    total = df['amount'].sum()
    avg = df['amount'].mean()

    top = df.groupby('category')['amount'].sum().idxmax()

    insights.append(f"💰 Total Spending: ₹{total}")
    insights.append(f"📊 Average Spending: ₹{avg:.2f}")
    insights.append(f"🔥 Top Category: {top}")

    if prediction > total:
        insights.append("⚠️ Risk: Next month spending may increase!")

    if avg > 1000:
        insights.append("⚠️ High spending behavior detected!")

    if total < 5000:
        insights.append("✅ Good savings behavior")

    return insights