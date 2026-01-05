# Google Sheets Columns Guide

## Available Columns in Price Tracker

Your Google Sheets now tracks **14 columns** of product data:

### 1. **Product Name** (Column A)
- The actual product name extracted from the Shopee URL
- Example: "Crocs Classic Sandal V2 in White"
- **Auto-populated:** Yes

### 2. **Product ID** (Column B)
- Unique Shopee product identifier
- Example: "25956400196"
- **Auto-populated:** Yes

### 3. **Price** (Column C)
- Current product price in Philippine Peso (₱)
- Example: "1899.00"
- **Auto-populated:** Yes

### 4. **Original Price** (Column D)
- Full price before discount
- Example: "2299.00"
- **Auto-populated:** Yes
- **Use:** Compare with current price to see discount value

### 5. **Savings Amount** (Column E) ⭐ *Calculated*
- Amount saved by buying at current price
- **Formula:** `=D-C` (Original Price - Current Price)
- Example: "400.00"
- **Auto-populated:** Yes (formula applies automatically)
- **Use:** See exact peso amount saved

### 6. **Discount (%)** (Column F)
- Percentage discount from original price
- Example: "17"
- **Auto-populated:** Yes

### 7. **Shop Name** (Column G)
- Name of the seller/shop
- Example: "Official Crocs Store"
- **Auto-populated:** Yes

### 8. **Rating** (Column H)
- Product rating (out of 5 stars)
- Example: "4.9"
- **Auto-populated:** Yes
- **Use:** Quick quality indicator

### 9. **Category** (Column I)
- Product category for organization
- Example: "Footwear"
- **Auto-populated:** Yes
- **Use:** Filter by product type

### 10. **Stock Status** (Column J)
- Availability status
- Example: "In Stock", "Low Stock", "Out of Stock"
- **Auto-populated:** Yes
- **Use:** Know when to buy

### 11. **Reviews Count** (Column K)
- Number of customer reviews
- Example: "3421"
- **Auto-populated:** Yes
- **Use:** Popularity/social proof indicator

### 12. **Notes** (Column L)
- Manual notes field (editable)
- Example: "Good quality, fast shipping", "Defective item returned"
- **Auto-populated:** No
- **Use:** Add personal observations, purchase decisions, or status updates
- **How to use:** Manually edit this cell in Google Sheets

### 13. **URL** (Column M)
- Full product link
- **Auto-populated:** Yes
- **Use:** Click to verify product details anytime

### 14. **Timestamp** (Column N)
- Date and time when price was recorded
- Example: "2026-01-05T14:06:51.123456"
- **Auto-populated:** Yes
- **Use:** Track when each price check occurred

---

## How to Use the Columns

### Track Price Changes
1. Run `python track.py` regularly (daily/weekly)
2. Each run adds a new row
3. Compare **Price** column values over time to see trends

### Calculate Total Savings
Create a formula in a new cell:
```
=SUM(E:E)  # Total of all Savings Amount values
```

### Filter Products
Use Google Sheets filters to view:
- Only "Footwear" category products
- Products with "In Stock" status
- Products with rating > 4.7

### Find Best Deals
Sort by **Discount (%)** column (descending) to find highest discounts

### Track Specific Product Notes
Add notes in Column L:
- "Price dropped! Good time to buy"
- "Out of stock - skip"
- "Already purchased on Jan 5"

---

## Auto-Calculated Columns

### Savings Amount (Column E)
**Automatically calculated** when you track a product:
- Formula: `=Original Price - Current Price`
- Shows the exact amount saved
- Updates automatically with each price change

### Example:
| Product Name | Price | Original Price | Savings Amount |
|---|---|---|---|
| Crocs Sandal | 1899 | 2299 | **400** |
| Adidas Shoes | 2499 | 3999 | **1500** |

---

## Customization Tips

### Add Your Own Formulas

You can add more calculated columns:

**Column O - Price per Unit:**
```
=C2/QUANTITY  # If you know quantity
```

**Column P - Days Since Track:**
```
=TODAY()-INT(N2)  # Days since recorded
```

**Column Q - Savings Percentage:**
```
=E2/D2*100  # Alternative to discount column
```

### Create a Summary Sheet
1. Create a new sheet: "Summary"
2. Add formulas for:
   - Total amount saved: `=SUM('Price Tracker'!E:E)`
   - Average discount: `=AVERAGE('Price Tracker'!F:F)`
   - Number of products tracked: `=COUNTA('Price Tracker'!A:A)-1`

---

## Example Data

### Sample Row
```
Product Name: Crocs Classic Sandal V2 in White
Product ID: 25956400196
Price: 1899.00
Original Price: 2299.00
Savings Amount: 400.00  (automatically calculated)
Discount (%): 17
Shop Name: Official Crocs Store
Rating: 4.9
Category: Footwear
Stock Status: In Stock
Reviews Count: 3421
Notes: [Empty - add your notes here]
URL: https://shopee.ph/Crocs-Classic-Sandal-V2-in-White-i.159408769.25956400196
Timestamp: 2026-01-05T12:00:03.123456
```

---

## Tips & Tricks

✅ **Do:**
- Track at consistent intervals (same day each week)
- Use Notes column for purchase history
- Create charts from Price column over time
- Sort by Discount to find best deals

❌ **Don't:**
- Manually edit Price/Original Price columns (these are auto-filled)
- Delete timestamp columns (needed for tracking trends)
- Trust completely on demo data (see REAL_SCRAPING_STATUS.md)

---

## Questions?

See `README.md` for more information about the price tracker project.
