# Data Cleaning & Preprocessing Log

### 1. Standardization
- Renamed raw columns to snake_case (`year`, `commodity`, `export_value`, `export_quantity`).
- Mapped commodities into high-level categories (`commodity_group`).

### 2. Deduplication & Filtering
- Removed duplicate rows across (`year`, `commodity`, `destination_country`).
- Filtered data to retain target commodities: Rice, Spices, Tea, Marine Products.

### 3. Missing Value Handling
- Interpolated short multi-year gaps using linear interpolation.
- Added `is_imputed` boolean flag for transparency.

### 4. Feature Engineering
- **`unit_value`**: Calculated as `(export_value * 1,000,000) / export_quantity` (USD/MT).
- **`yoy_growth`**: Percentage change in export value year-over-year per destination.
