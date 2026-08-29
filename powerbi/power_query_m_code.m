// ============================================================================
// POWER QUERY (M-CODE) SCRIPTS FOR DATA INGESTION
// Connects to PostgreSQL Database or Processed CSVs
// ============================================================================

// ----------------------------------------------------------------------------
// 1. Dim Date
// ----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/processed/dim_date.csv"), [Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"date_key", Int64.Type}, 
        {"full_date", type date}, 
        {"year", Int64.Type}, 
        {"quarter", Int64.Type}, 
        {"quarter_name", type text}, 
        {"month", Int64.Type}, 
        {"month_name", type text}, 
        {"year_month", type text}, 
        {"week", Int64.Type}, 
        {"day", Int64.Type}, 
        {"day_of_week", Int64.Type}, 
        {"day_name", type text}, 
        {"is_weekend", Int64.Type}, 
        {"is_month_end", Int64.Type}
    })
in
    #"Changed Type"

// ----------------------------------------------------------------------------
// 2. Dim Customer
// ----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/processed/dim_customer.csv"), [Delimiter=",", Columns=16, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"customer_key", Int64.Type},
        {"customer_id", type text},
        {"customer_unique_id", type text},
        {"customer_zip_code_prefix", Int64.Type},
        {"customer_city", type text},
        {"customer_state", type text},
        {"rfm_recency", Int64.Type},
        {"rfm_frequency", Int64.Type},
        {"rfm_monetary", type number},
        {"rfm_segment", type text},
        {"is_repeat_customer", Int64.Type}
    })
in
    #"Changed Type"

// ----------------------------------------------------------------------------
// 3. Fact Sales
// ----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/processed/fact_sales.csv"), [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"sales_key", Int64.Type},
        {"order_id", type text},
        {"order_item_id", Int64.Type},
        {"customer_key", Int64.Type},
        {"product_key", Int64.Type},
        {"seller_key", Int64.Type},
        {"date_key", Int64.Type},
        {"order_status", type text},
        {"price", type number},
        {"freight_value", type number},
        {"item_value", type number}
    })
in
    #"Changed Type"
