import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Nursery Pricing Calculator",
    page_icon="🌱",
    layout="wide"  # Better responsive behavior
)

st.title("🌱 Nursery Pricing Calculator")
st.write("Calculate optimal pricing for your nursery products with built-in profit margins")

# Desktop view toggle - mobile is default
desktop_view = st.checkbox("🖥️ Desktop View", value=False, help="Switch to two-column layout for desktop")
st.write("---")

# Mobile-first layout - single column by default, two columns for desktop
if desktop_view:
    # Desktop layout - two columns
    col1, col2 = st.columns([2, 1])
    input_container = col1
    results_container = col2
else:
    # Mobile layout (default) - single column
    input_container = st.container()
    results_container = st.container()

with input_container:
    st.header("💰 Cost Inputs")
    
    # Plant costs
    plant_cost = st.number_input(
        "Plant Cost ($)", 
        min_value=0.0, 
        value=5.0, 
        step=0.50,
        help="Wholesale cost or cost to grow this plant"
    )
    
    # Materials costs
    st.subheader("Materials & Care")
    pot_cost = st.number_input("Pot/Container ($)", min_value=0.0, value=2.0, step=0.25)
    soil_cost = st.number_input("Soil/Growing Medium ($)", min_value=0.0, value=1.0, step=0.25)
    fertilizer_cost = st.number_input("Fertilizer/Care Products ($)", min_value=0.0, value=0.50, step=0.25)
    packaging_cost = st.number_input("Packaging/Shipping Materials ($)", min_value=0.0, value=1.50, step=0.25, 
                                   help="Box, padding, protective materials for shipping")
    other_materials = st.number_input("Other Materials ($)", min_value=0.0, value=0.0, step=0.25)
    
    # Time investment
    st.subheader("Time Investment")
    care_hours = st.number_input("Care/Prep Hours", min_value=0.0, value=1.0, step=0.25)
    hourly_rate = st.number_input("Your Hourly Rate ($)", min_value=0.0, value=20.0, step=5.0)
    
    # Pricing settings - ALL INPUT VARIABLES DEFINED HERE
    st.subheader("Pricing Settings")
    profit_margin = st.slider("Desired Profit Margin (%)", min_value=20, max_value=100, value=30, step=5)
    sales_discount = st.slider("Sales Discount (%)", min_value=0, max_value=50, value=0, step=5,
                              help="Discount applied to final price")
    minimum_sales_profit = st.slider("Minimum Sales Profit (%)", min_value=0, max_value=20, value=10, step=1,
                                    help="Lowest profit margin allowed during sales")
    include_gst = st.checkbox("Add GST (10%)", value=True, help="Add Australian GST to final price")

# ALL INPUT VARIABLES NOW DEFINED - START CALCULATIONS
# Step 1: Calculate total costs
total_material_cost = pot_cost + soil_cost + fertilizer_cost + packaging_cost + other_materials
time_cost = care_hours * hourly_rate
total_cost = plant_cost + total_material_cost + time_cost

# Step 2: Calculate base selling price (before GST, before discount)
base_selling_price = total_cost / (1 - profit_margin/100)

# Step 3: Add GST to get list price
if include_gst:
    gst_amount = base_selling_price * 0.10
    list_price = base_selling_price + gst_amount
else:
    gst_amount = 0.0
    list_price = base_selling_price

# Step 4: Apply discount to list price
if sales_discount > 0:
    discounted_price = list_price * (1 - sales_discount/100)
    
    # Calculate minimum allowable price
    min_price_before_gst = total_cost / (1 - minimum_sales_profit/100) if minimum_sales_profit > 0 else total_cost
    min_allowable_price = min_price_before_gst * 1.10 if include_gst else min_price_before_gst
    
    # Final price is higher of discounted price or minimum
    final_selling_price = max(discounted_price, min_allowable_price)
else:
    final_selling_price = list_price

# Step 5: Calculate actual achieved margins
if include_gst:
    actual_price_before_gst = final_selling_price / 1.10
    actual_gst = final_selling_price - actual_price_before_gst
else:
    actual_price_before_gst = final_selling_price
    actual_gst = 0.0

actual_profit = actual_price_before_gst - total_cost
actual_margin = (actual_profit / actual_price_before_gst) * 100 if actual_price_before_gst > 0 else 0

with results_container:
    st.header("💡 Pricing Results")
    
    # Cost breakdown
    st.subheader("Cost Breakdown")
    st.write(f"**Plant Cost:** ${plant_cost:.2f}")
    st.write(f"**Materials:** ${total_material_cost:.2f}")
    st.write(f"**Time ({care_hours}h):** ${time_cost:.2f}")
    st.write("---")
    st.write(f"**Total Cost:** ${total_cost:.2f}")
    
    # Detailed breakdown (expandable)
    with st.expander("📋 Detailed Cost Breakdown"):
        st.write(f"Plant: ${plant_cost:.2f}")
        st.write(f"Pot/Container: ${pot_cost:.2f}")
        st.write(f"Soil/Growing Medium: ${soil_cost:.2f}")
        st.write(f"Fertilizer/Care: ${fertilizer_cost:.2f}")
        st.write(f"Packaging/Shipping: ${packaging_cost:.2f}")
        if other_materials > 0:
            st.write(f"Other Materials: ${other_materials:.2f}")
        st.write(f"Time ({care_hours}h @ ${hourly_rate:.2f}/h): ${time_cost:.2f}")
    
    # Pricing recommendation
    st.subheader("Recommended Price")
    
    # Show pricing flow
    if sales_discount > 0:
        st.write(f"**List Price:** ${list_price:.2f}")
        st.write(f"**Discount ({sales_discount}%):** -${list_price - discounted_price:.2f}")
    
    if include_gst and sales_discount == 0:
        st.write(f"**Price before GST:** ${base_selling_price:.2f}")
        st.write(f"**GST (10%):** ${gst_amount:.2f}")
    
    st.metric(
        label="Final Selling Price" + (" (inc GST)" if include_gst else ""), 
        value=f"${final_selling_price:.2f}",
        help=f"Achieves {actual_margin:.1f}% profit margin"
    )
    
    st.metric(
        label="Actual Profit", 
        value=f"${actual_profit:.2f}",
        delta=f"{actual_margin:.1f}%"
    )
    
    # Profit status
    if actual_margin >= 20:
        st.success(f"✅ {actual_margin:.1f}% margin meets target")
    elif actual_margin >= minimum_sales_profit:
        st.info(f"ℹ️ {actual_margin:.1f}% margin (sales pricing)")
    elif actual_margin >= 0:
        st.warning(f"⚠️ {actual_margin:.1f}% margin (low profit)")
    else:
        st.error(f"❌ {actual_margin:.1f}% margin (loss!)")

# Market comparison section
st.header("🔍 Market Comparison")
st.write("Compare your price with local competitors")

comp_col1, comp_col2, comp_col3 = st.columns(3)

with comp_col1:
    comp1_name = st.text_input("Competitor 1 Name", placeholder="Local Garden Center")
    comp1_price = st.number_input("Their Price ($)", min_value=0.0, value=0.0, key="comp1")

with comp_col2:
    comp2_name = st.text_input("Competitor 2 Name", placeholder="Big Box Store")
    comp2_price = st.number_input("Their Price ($)", min_value=0.0, value=0.0, key="comp2")

with comp_col3:
    comp3_name = st.text_input("Competitor 3 Name", placeholder="Online Retailer")
    comp3_price = st.number_input("Their Price ($)", min_value=0.0, value=0.0, key="comp3")

# Display comparison if any competitor prices entered
competitors = []
if comp1_price > 0:
    competitors.append({"Name": comp1_name or "Competitor 1", "Price": comp1_price})
if comp2_price > 0:
    competitors.append({"Name": comp2_name or "Competitor 2", "Price": comp2_price})
if comp3_price > 0:
    competitors.append({"Name": comp3_name or "Competitor 3", "Price": comp3_price})

if competitors:
    st.subheader("Price Comparison")
    comparison_data = competitors + [{"Name": "Your Price", "Price": final_selling_price}]
    df = pd.DataFrame(comparison_data)
    
    # Sort by price for easy comparison
    df_sorted = df.sort_values("Price")
    st.dataframe(df_sorted, hide_index=True)
    
    # Quick analysis
    avg_competitor_price = sum([c["Price"] for c in competitors]) / len(competitors)
    
    if final_selling_price <= avg_competitor_price:
        st.success(f"✅ Your price (${final_selling_price:.2f}) is competitive with average competitor price (${avg_competitor_price:.2f})")
    else:
        price_diff = final_selling_price - avg_competitor_price
        st.warning(f"⚠️ Your price is ${price_diff:.2f} above average competitor price. Consider if premium quality justifies this.")

# Summary section - ALL VARIABLES PROPERLY DEFINED
st.header("📋 Pricing Summary")

gst_text = f" (inc GST ${actual_gst:.2f})" if include_gst and actual_gst > 0 else ""
discount_text = f" (after {sales_discount}% discount)" if sales_discount > 0 else ""

summary_text = f"""
**Product Pricing Decision:**
- **Final Selling Price:** ${final_selling_price:.2f}{gst_text}{discount_text}
- **Total Cost:** ${total_cost:.2f}
- **Actual Profit:** ${actual_profit:.2f} ({actual_margin:.1f}%)
- **Cost Breakdown:** Plant ${plant_cost:.2f} + Materials ${total_material_cost:.2f} (incl. packaging ${packaging_cost:.2f}) + Time ${time_cost:.2f}
"""

if competitors:
    summary_text += f"\n- **Market Position:** Compared to {len(competitors)} competitors"

st.text_area("Copy this summary:", summary_text, height=150)