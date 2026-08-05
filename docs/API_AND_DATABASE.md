# 💾 RetailMind AI — Database ERD & Services API Documentation

## 1. Database Entity-Relationship Schema (SQLite)

### Products Table (`products`)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique Item ID |
| `barcode` | TEXT | UNIQUE | Scannable Barcode String |
| `product_name` | TEXT | NOT NULL | Full Catalog Product Title |
| `category` | TEXT | NOT NULL | Grocery, Dairy, Confectionery, etc. |
| `purchase_price`| REAL | DEFAULT 0 | Wholesale Cost (₹) |
| `selling_price` | REAL | DEFAULT 0 | Retail Customer MRP (₹) |
| `stock` | INTEGER | DEFAULT 50 | Current Stock Units |
| `min_stock` | INTEGER | DEFAULT 10 | Minimum Safety Threshold |
| `market` | TEXT | DEFAULT 'Nashik Mandi' | Sourcing Wholesale Market |

### Customer CRM Table (`customers`)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Customer ID |
| `customer_name`| TEXT | NOT NULL | Customer Full Name |
| `mobile` | TEXT | UNIQUE | 10-Digit Mobile Number |
| `loyalty_points`| INTEGER| DEFAULT 0 | Reward Points Accumulated |

---

## 2. Core Service Methods

### `DatabaseManager.get_products_dataframe() -> pd.DataFrame`
Fetches complete product catalog with auto-calculated profit margins and stock status indicators.

### `MLForecastingEngine.calculate_reorder_point(daily_demand, lead_time, safety_stock) -> int`
Computes mathematical Reorder Point: $ROP = (d \times L) + SS$.

### `AuthService.authenticate_user(username, password) -> Optional[Dict]`
Verifies salted PBKDF2 HMAC SHA-256 password hash.
