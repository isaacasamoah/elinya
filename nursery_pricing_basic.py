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
    
    # Profit margin
    st.subheader("Profit Margin")
    profit_margin = st.slider("Desired Profit Margin (%)", min_value=20, max_value=100, value=30, step=5)
    
    # GST option - define the variable here in the input section
    include_gst = st.checkbox("Add GST (10%)", value=True, help="Add Australian GST to final price")

# Calculate all costs first - ALL INPUT VARIABLES ARE NOW DEFINED
total_material_cost = pot_cost + soil_cost + fertilizer_cost + packaging_cost + other_materials
time_cost = care_hours * hourly_rate
total_cost = plant_cost + total_material_cost + time_cost

# Calculate selling price based on desired margin (before GST)
selling_price_before_gst = total_cost / (1 - profit_margin/100)
profit_amount = selling_price_before_gst - total_cost

# Now calculate GST and final price
if include_gst:
    gst_amount = selling_price_before_gst * 0.10
    final_selling_price = selling_price_before_gst + gst_amount
else:
    gst_amount = 0.0
    final_selling_price = selling_price_before_gst

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
    
    # Show price breakdown
    if include_gst:
        st.write(f"**Price before GST:** ${selling_price_before_gst:.2f}")
        st.write(f"**GST (10%):** ${gst_amount:.2f}")
        st.metric(
            label="Final Price (inc GST)", 
            value=f"${final_selling_price:.2f}",
            help=f"Includes GST and ensures {profit_margin}% profit margin"
        )
    else:
        st.metric(
            label="Selling Price", 
            value=f"${final_selling_price:.2f}",
            help=f"Ensures {profit_margin}% profit margin"
        )
    
    st.metric(
        label="Profit", 
        value=f"${profit_amount:.2f}",
        delta=f"{profit_margin}%"
    )
    
    # Visual profit check
    if profit_margin >= 20:
        st.success(f"✅ {profit_margin}% margin meets minimum target")
    else:
        st.error("❌ Below minimum 20% margin")

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

# Summary section - ALL VARIABLES ARE NOW PROPERLY DEFINED BEFORE USE
st.header("📋 Pricing Summary")

# Build GST text safely
gst_text = f" (inc GST ${actual_gst_amount:.2f})" if include_gst and actual_gst_amount > 0 else ""
discount_text = f" (after {sales_discount}% discount)" if sales_discount > 0 else ""

summary_text = f"""
**Product Pricing Decision:**
- **Final Selling Price:** ${final_selling_price:.2f}{gst_text}{discount_text}
- **Total Cost:** ${total_cost:.2f}
- **Profit:** ${actual_profit_amount:.2f} ({actual_profit_margin:.1f}%)
- **Cost Breakdown:** Plant ${plant_cost:.2f} + Materials ${total_material_cost:.2f} (incl. packaging ${packaging_cost:.2f}) + Time ${time_cost:.2f}
"""

if competitors:
    summary_text += f"\n- **Market Position:** Compared to {len(competitors)} competitors"

st.text_area("Copy this summary:", summary_text, height=150)