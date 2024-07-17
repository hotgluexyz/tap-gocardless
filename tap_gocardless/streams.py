"""Stream type classes for tap-gocardless."""
from singer_sdk import typing as th  # JSON Schema typing helpers
from tap_gocardless.client import GoCardlessStream


class PaymentsStream(GoCardlessStream):
    name = "payments"
    path = "/payments"
    primary_keys = ["id"]
    replication_key = None  # created_at
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("charge_date", th.StringType),
        th.Property("amount", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("currency", th.StringType),
        th.Property("status", th.StringType),
        th.Property("amount_refunded", th.IntegerType),
        th.Property("reference", th.StringType),
        th.Property("metadata", th.CustomType({"type": ["object", "string"]})),
        th.Property(
            "fx",
            th.ObjectType(
                th.Property("fx_currency", th.StringType),
                th.Property("fx_amount", th.IntegerType),
                th.Property("exchange_rate", th.NumberType),
                th.Property("estimated_exchange_rate", th.NumberType),
            ),
        ),
        th.Property(
            "links",
            th.ObjectType(
                th.Property("mandate", th.StringType),
                th.Property("creditor", th.StringType),
            ),
        ),
        th.Property("retry_if_possible", th.BooleanType),
    ).to_dict()


class MandatesStream(GoCardlessStream):
    name = "mandates"
    path = "/mandates"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("reference", th.StringType),
        th.Property("status", th.StringType),
        th.Property("scheme", th.StringType),
        th.Property("next_possible_charge_date", th.DateType),
        th.Property("payments_require_approval", th.BooleanType),
        th.Property("metadata", th.CustomType({"type": ["object", "string"]})),
        th.Property(
            "links",
            th.ObjectType(
                th.Property("customer_bank_account", th.StringType),
                th.Property("creditor", th.StringType),
                th.Property("customer", th.StringType),
            ),
        ),
        th.Property(
            "consent_parameters", th.CustomType({"type": ["object", "string"]})
        ),
        th.Property("verified_at", th.StringType),
        th.Property("funds_settlement", th.StringType),
    ).to_dict()


class RefundsStream(GoCardlessStream):
    name = "refunds"
    path = "/refunds"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("amount", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("reference", th.StringType),
        th.Property("metadata", th.CustomType({"type": ["object", "string"]})),
        th.Property("currency", th.StringType),
        th.Property("status", th.StringType),
        th.Property(
            "fx",
            th.ObjectType(
                th.Property("fx_currency", th.StringType),
                th.Property("fx_amount", th.IntegerType),
                th.Property("exchange_rate", th.NumberType),
                th.Property("estimated_exchange_rate", th.NumberType),
            ),
        ),
        th.Property(
            "links",
            th.ObjectType(
                th.Property("payment", th.StringType),
                th.Property("mandate", th.StringType),
            ),
        ),
    ).to_dict()


class PayoutsStream(GoCardlessStream):
    name = "payouts"
    path = "/payouts"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("amount", th.IntegerType),
        th.Property("deducted_fees", th.IntegerType),
        th.Property("currency", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("reference", th.StringType),
        th.Property("status", th.StringType),
        th.Property("arrival_date", th.StringType),
        th.Property("payout_type", th.StringType),
        th.Property(
            "fx",
            th.ObjectType(
                th.Property("fx_currency", th.StringType),
                th.Property("fx_amount", th.IntegerType),
                th.Property("exchange_rate", th.NumberType),
                th.Property("estimated_exchange_rate", th.NumberType),
            ),
        ),
        th.Property("tax_currency", th.StringType),
        th.Property("metadata", th.CustomType({"type": ["object", "string"]})),
        th.Property(
            "links",
            th.ObjectType(
                th.Property("creditor_bank_account", th.StringType),
                th.Property("creditor", th.StringType),
            ),
        ),
    ).to_dict()
