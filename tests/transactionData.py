class transaction_test_data:
    transaction_data_2023 = [
        {
            "amount": -44.98,
            "bdate": "2023-01-22",
            "currencycode": "EUR",
            "customerreferenz": "XXXXXX",
            "peer": "PayPal Europe S.a.r.l. et Cie S.C.A",
            "peeraccount": "XXXXXXXXX",
            "peerbic": "XXXXXXXXX",
            "peerid": "XXXXXXXXXXX",
            "postingtext": "FOLGELASTSCHRIFT",
            "reasonforpayment": "XXXXXX PP.XXXXX.PP . Foo-bar AG, Ihr Einkauf bei "
            "Foo-bar AG",
            "vdate": "2023-01-22",
        },
        {
            "amount": -70.05,
            "bdate": "2023-01-22",
            "currencycode": "EUR",
            "customerreferenz": "68251782022947180823144926",
            "peer": "FEFASE GmbH",
            "peeraccount": "XXXXXXXXX",
            "peerbic": "XXXXXXXXX",
            "peerid": "XXXXXXXXX",
            "postingtext": "SEPA-ELV-LASTSCHRIFT",
            "reasonforpayment": "ELV68251782 18.08 14.49 MEFAS ",
            "vdate": "2023-01-22",
        },
        {
            "amount": -7.49,
            "bdate": "2023-01-22",
            "currencycode": "EUR",
            "customerreferenz": "3REFeSERENC",
            "peer": "PEER",
            "peeraccount": "XXXXXXXXX",
            "peerbic": "XXXXXXXXX",
            "peerid": "XXXXXXXXX",
            "postingtext": "FOLGELASTSCHRIFT",
            "reasonforpayment": "VIELEN DANK VON BAR-FOO GMBH",
            "vdate": "2023-01-22",
        },
    ]

    transaction_data_2024 = [
        {
            "amount": -84.18,
            "bdate": "2024-12-22",
            "currencycode": "EUR",
            "customerreferenz": "XXXXXX",
            "peer": "PayPal Europe S.a.r.l. et Cie S.C.A",
            "peeraccount": "XXXXXXXXX",
            "peerbic": "XXXXXXXXX",
            "peerid": "XXXXXXXXXXX",
            "postingtext": "FOLGELASTSCHRIFT",
            "reasonforpayment": "XXXXXX PP.XXXXX.PP . Foo-bar AG, Ihr Einkauf bei "
            "Foo-bar AG",
            "vdate": "2024-12-02",
        },
        {
            "amount": -700.05,
            "bdate": "2023-01-22",
            "currencycode": "EUR",
            "customerreferenz": "68251782022947180823144926",
            "peer": "FEFASE GmbH",
            "peeraccount": "XXXXXXXXX",
            "peerbic": "XXXXXXXXX",
            "peerid": "XXXXXXXXX",
            "postingtext": "SEPA-ELV-LASTSCHRIFT",
            "reasonforpayment": "ELV68251782 18.08 14.49 MEFAS ",
            "vdate": "2023-01-22",
        },
        {
            "amount": -1.49,
            "bdate": "2024-05-22",
            "currencycode": "EUR",
            "customerreferenz": "3REFeSERENC",
            "peer": "PEER",
            "peeraccount": "XXXXXXXXX",
            "peerbic": "XXXXXXXXX",
            "peerid": "XXXXXXXXX",
            "postingtext": "FOLGELASTSCHRIFT",
            "reasonforpayment": "VIELEN DANK VON BAR-FOO GMBH",
            "vdate": "2023-01-22",
        },
    ]

    transaction_data_filtered_2024 = [
        {
            "amount": -84.18,
            "bdate": "2024-12-22",
            "customerreferenz": "XXXXXX",
            "peer": "Rewe Gmbh",
            "postingtext": "FOLGELASTSCHRIFT",
            "reasonforpayment": "XXXXXX PP.XXXXX.PP . Rewe, Ihr Einkauf bei Rewe",
        },
        {
            "amount": -700.05,
            "bdate": "2023-01-22",
            "customerreferenz": "68251782022947180823144926",
            "peer": "Mediamarkt GmbH",
            "postingtext": "SEPA-ELV-LASTSCHRIFT",
            "reasonforpayment": "ELV68251782 18.08 14.49 MEFAS ",
        },
        {
            "amount": -1.49,
            "bdate": "2024-05-22",
            "customerreferenz": "3REFeSERENC",
            "peer": "PEER",
            "postingtext": "FOLGELASTSCHRIFT",
            "reasonforpayment": "VIELEN DANK VON BAR-FOO GMBH",
        },
        {
            "amount": -800,
            "bdate": "2024-09-01",
            "customerreferenz": "skfjljkKjk",
            "peer": "Lorenz Hofmann",
            "postingtext": "LASTSCHRIFT",
            "reasonforpayment": "Miete",
        },
    ]
