import pandas as pd
import re
from typing import Dict, Any

class AIEngine:
    """
    Conversational NLP NLU Query Parsing Engine.
    Parses Hindi, Hinglish, and English retail queries regarding
    stock, pricing, profit margins, mandi rates, and sales.
    """

    @staticmethod
    def process_query(query: str, products_df: pd.DataFrame) -> Dict[str, Any]:
        q_lower = query.lower().strip()

        if not q_lower:
            return {"type": "info", "message": "Please enter or speak a question to query RetailMind AI."}

        # 1. Stock Queries
        if any(w in q_lower for w in ["stock", "kitna bacha", "kitna hai", "available", "quantity", "batao"]):
            # Search for specific product matches
            matched_products = []
            for _, row in products_df.iterrows():
                p_name = str(row.get("product_name", "")).lower()
                short_name = str(row.get("name", "")).lower()
                brand = str(row.get("brand", "")).lower()

                # Match tokens
                tokens = [t for t in re.split(r'\s+', q_lower) if len(t) > 2 and t not in ["stock", "kitna", "hai", "batao", "ka", "ki", "price"]]
                if any(t in p_name or t in short_name or t in brand for t in tokens):
                    matched_products.append(row)

            if matched_products:
                res_df = pd.DataFrame(matched_products)
                summary_lines = []
                for _, r in res_df.iterrows():
                    summary_lines.append(f"• **{r['product_name']}**: Current Stock = **{r['stock']} {r['unit']}** (Status: {r.get('stock_status', '🟢 Healthy')})")
                return {
                    "type": "success",
                    "title": f"📦 Stock Query Results ({len(matched_products)} items found)",
                    "message": "\n".join(summary_lines),
                    "dataframe": res_df[['product_name', 'stock', 'unit', 'min_stock', 'stock_status', 'market']]
                }
            else:
                # Return general low stock list
                low_df = products_df[products_df["stock"] <= products_df["min_stock"]]
                return {
                    "type": "warning",
                    "title": "⚠️ Low Stock Summary",
                    "message": f"Found **{len(low_df)} products** below minimum threshold.",
                    "dataframe": low_df[['product_name', 'stock', 'unit', 'min_stock', 'stock_status']]
                }

        # 2. Margin & Profit Queries
        elif any(w in q_lower for w in ["profit", "margin", "faida", "kamai", "revenue"]):
            top_margin = products_df.sort_values("margin_pct", ascending=False).head(5)
            return {
                "type": "success",
                "title": "💰 Top Profit Margin Products",
                "message": "Here are your highest margin products:",
                "dataframe": top_margin[['product_name', 'purchase_price', 'selling_price', 'profit_margin', 'margin_pct']]
            }

        # 3. Mandi / Wholesale Price Queries
        elif any(w in q_lower for w in ["mandi", "market", "wholesale", "nashik", "pune", "sasta", "cheapest"]):
            best_mkt = products_df.groupby("market")["selling_price"].mean().idxmin()
            min_val = products_df.groupby("market")["selling_price"].mean().min()
            return {
                "type": "info",
                "title": "🌾 Mandi Market Rate Intelligence",
                "message": f"🥇 **{best_mkt}** is currently the cheapest sourcing market (Average rate: **₹{min_val:.2f}/item**).",
                "dataframe": products_df.groupby("market").agg(Avg_Selling=("selling_price", "mean"), Avg_Purchase=("purchase_price", "mean"), Items=("id", "count")).reset_index()
            }

        # Default Fallback
        return {
            "type": "info",
            "title": "🤖 RetailMind AI Assistance",
            "message": f"Query processed: *\"{query}\"*. Try asking:\n- *\"Atta ka stock batao\"*\n- *\"Sugar ka profit margin kitna hai\"*\n- *\"Cheapest Mandi market kaunsa hai\"*",
            "dataframe": products_df[['product_name', 'category', 'selling_price', 'stock']].head(5)
        }
