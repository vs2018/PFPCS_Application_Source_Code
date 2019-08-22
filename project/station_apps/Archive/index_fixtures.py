transform_input = [
    (
        "2019-06-23T17:09:00+01:00",
        "In addition to that, research by campaign group Fair Fuel UK found that over the past five years fuel prices between petrol station can differ by 4p to 21p per litre. This means motorists could save much more money if they travelled to alternative stations to top up their fuel.",
        "neg",
        0.24,
        0.76,
    ),
    (
        "2019-06-25T06:15:00Z",
        "“However, until this takes place, we would encourage drivers to find the best fuel deal local to them, or along their intended route, before they set off using an such asPetrolPrices.com which will help them to avoid being ripped off on the motorway. “For too long millions of UK motorists",
        "neg",
        0.24,
        0.76,
    ),
]

parse_data_input = {
    "id": "WxNhrtsIdbb3uW1Y-HP8y14KXokwrwmcUK7C3JlkBVLiyOfbka1gakKoAo9vfFi4",
    "result_metadata": {"score": 18.724169},
    "enriched_title": {
        "entities": [
            {
                "count": 1,
                "sentiment": {"score": -0.42566, "label": "negative"},
                "text": "UK",
                "relevance": 0.33,
                "type": "Location",
                "disambiguation": {"subtype": ["Country"]},
            }
        ],
        "sentiment": {"document": {"score": 0, "label": "neutral"}},
        "semantic_roles": [],
        "concepts": [
            {
                "text": "Inflation",
                "relevance": 0.886784,
                "dbpedia_resource": "http://dbpedia.org/resource/Inflation",
            }
        ],
        "categories": [
            {"score": 0.952919, "label": "/society/work/unemployment"},
            {"score": 0.850255, "label": "/finance/bank"},
            {
                "score": 0.769746,
                "label": "/business and industrial/advertising and marketing",
            },
        ],
        "relations": [
            {
                "type": "residesIn",
                "sentence": "UK consumer inflation remains unchanged in June",
                "score": 0.280198,
                "arguments": [
                    {
                        "text": "consumer",
                        "location": [3, 11],
                        "entities": [{"type": "Person", "text": "consumer"}],
                    },
                    {
                        "text": "UK",
                        "location": [0, 2],
                        "entities": [
                            {
                                "type": "GeopoliticalEntity",
                                "text": "UK",
                                "disambiguation": {"subtype": ["Area"]},
                            }
                        ],
                    },
                ],
            }
        ],
        "keywords": [
            {
                "text": "UK consumer inflation",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.998396,
                "count": 1,
            },
            {
                "text": "June",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.613217,
                "count": 1,
            },
        ],
    },
    "crawl_date": "2019-07-17T08:40:29Z",
    "url": "https://english.mubasher.info/news/3503627/UK-consumer-inflation-remains-unchanged-in-June",
    "host": "english.mubasher.info",
    "text": "This stable rate came after a drop costs of in motor fuels, accommodation services, electricity, gas and other fuels was wiped out by climbing prices of clothing and food. The price index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate, stabilized at 1.9% last June, the Office for",
    "main_image_url": "https://static.mubasher.info/File.Story_Image/1db65c026720d1579d1aaf579b1e21b1/640.jpg",
    "country": "GB",
    "source_type": "mainstream",
    "language": "en",
    "publication_date": "2019-07-17T08:42:00Z",
    "enriched_text": {
        "entities": [
            {
                "count": 3,
                "sentiment": {"score": -0.335299, "label": "negative"},
                "text": "UK",
                "relevance": 0.825725,
                "type": "Location",
                "disambiguation": {
                    "subtype": [
                        "AdministrativeDivision",
                        "GovernmentalJurisdiction",
                        "Kingdom",
                        "MeteorologicalService",
                        "Country",
                    ],
                    "name": "United Kingdom",
                    "dbpedia_resource": "http://dbpedia.org/resource/United_Kingdom",
                },
            },
            {
                "count": 1,
                "sentiment": {"score": 0, "label": "neutral"},
                "text": "official",
                "relevance": 0.422181,
                "type": "JobTitle",
            },
            {
                "count": 1,
                "sentiment": {"score": 0, "label": "neutral"},
                "text": "12-month",
                "relevance": 0.422181,
                "type": "Quantity",
            },
            {
                "count": 1,
                "sentiment": {"score": 0, "label": "neutral"},
                "text": "$1.2403",
                "relevance": 0.422181,
                "type": "Quantity",
            },
            {
                "count": 1,
                "sentiment": {"score": 0, "label": "neutral"},
                "text": "0.02%",
                "relevance": 0.422181,
                "type": "Quantity",
            },
            {
                "count": 1,
                "sentiment": {"score": 0, "label": "neutral"},
                "text": "0.05%",
                "relevance": 0.422181,
                "type": "Quantity",
            },
            {
                "count": 1,
                "sentiment": {"score": 0, "label": "neutral"},
                "text": "1.9%",
                "relevance": 0.422181,
                "type": "Quantity",
            },
            {
                "count": 1,
                "sentiment": {"score": 0, "label": "neutral"},
                "text": "2%",
                "relevance": 0.422181,
                "type": "Quantity",
            },
        ],
        "sentiment": {"document": {"score": -0.39822, "label": "negative"}},
        "semantic_roles": [
            {
                "subject": {
                    "text": "the headline gauge for the country’s inflation",
                    "keywords": [
                        {"text": "headline gauge"},
                        {"text": "inflation"},
                        {"text": "country"},
                    ],
                },
                "sentence": "UK consumer inflation remains unchanged in June 17 July 2019 11:42 AM Last Updated: 17 July 2019 11:42 AM UK consumer inflation remains unchanged in June Mubasher: The UK’s consumer price index (CPI), the headline gauge for the country’s inflation came in at 2% year-on-year in June, unchanged from May’s reading, official data showed on Wednesday.",
                "object": {
                    "text": "in at 2% year-on-year in June",
                    "entities": [{"type": "Quantity", "text": "2"}],
                },
                "action": {
                    "verb": {"text": "come", "tense": "past"},
                    "text": "came",
                    "normalized": "come",
                },
            },
            {
                "subject": {
                    "text": "official data",
                    "keywords": [{"text": "official data"}],
                    "entities": [{"type": "JobTitle", "text": "official"}],
                },
                "sentence": "UK consumer inflation remains unchanged in June 17 July 2019 11:42 AM Last Updated: 17 July 2019 11:42 AM UK consumer inflation remains unchanged in June Mubasher: The UK’s consumer price index (CPI), the headline gauge for the country’s inflation came in at 2% year-on-year in June, unchanged from May’s reading, official data showed on Wednesday.",
                "action": {
                    "verb": {"text": "show", "tense": "past"},
                    "text": "showed",
                    "normalized": "show",
                },
            },
            {
                "subject": {
                    "text": "This stable rate",
                    "keywords": [{"text": "stable rate"}],
                },
                "sentence": " This stable rate came after a drop costs of in motor fuels, accommodation services, electricity, gas and other fuels was wiped out by climbing prices of clothing and food.",
                "action": {
                    "verb": {"text": "come", "tense": "past"},
                    "text": "came",
                    "normalized": "come",
                },
            },
            {
                "subject": {
                    "text": "accommodation services, electricity, gas and other fuels",
                    "keywords": [
                        {"text": "fuels"},
                        {"text": "accommodation services"},
                        {"text": "electricity"},
                        {"text": "gas"},
                    ],
                },
                "sentence": " This stable rate came after a drop costs of in motor fuels, accommodation services, electricity, gas and other fuels was wiped out by climbing prices of clothing and food.",
                "object": {
                    "text": "wiped out by climbing prices of clothing and food",
                    "keywords": [
                        {"text": "prices"},
                        {"text": "clothing"},
                        {"text": "food"},
                    ],
                },
                "action": {
                    "verb": {"text": "be", "tense": "past"},
                    "text": "was",
                    "normalized": "be",
                },
            },
            {
                "subject": {
                    "text": "by climbing prices of clothing and food",
                    "keywords": [
                        {"text": "prices"},
                        {"text": "clothing"},
                        {"text": "food"},
                    ],
                },
                "sentence": " This stable rate came after a drop costs of in motor fuels, accommodation services, electricity, gas and other fuels was wiped out by climbing prices of clothing and food.",
                "object": {
                    "text": "accommodation services, electricity, gas and other fuels",
                    "keywords": [
                        {"text": "fuels"},
                        {"text": "accommodation services"},
                        {"text": "electricity"},
                        {"text": "gas"},
                    ],
                },
                "action": {
                    "verb": {"text": "wipe", "tense": "past"},
                    "text": "was wiped",
                    "normalized": "be wipe",
                },
            },
            {
                "subject": {
                    "text": "This stable rate came after a drop costs of in motor fuels, accommodation services, electricity, gas and other fuels",
                    "keywords": [
                        {"text": "motor fuels"},
                        {"text": "stable rate"},
                        {"text": "drop costs"},
                        {"text": "accommodation services"},
                    ],
                },
                "sentence": " This stable rate came after a drop costs of in motor fuels, accommodation services, electricity, gas and other fuels was wiped out by climbing prices of clothing and food.",
                "object": {
                    "text": "prices of clothing and food",
                    "keywords": [
                        {"text": "prices"},
                        {"text": "clothing"},
                        {"text": "food"},
                    ],
                },
                "action": {
                    "verb": {"text": "climb", "tense": "past"},
                    "text": "climbing",
                    "normalized": "climb",
                },
            },
            {
                "subject": {
                    "text": "the costs of owner occupiers’ housing, (CPIH) 12-month rate",
                    "keywords": [
                        {"text": "12-month rate"},
                        {"text": "owner occupiers"},
                        {"text": "costs"},
                        {"text": "housing"},
                    ],
                    "entities": [{"type": "Quantity", "text": "12-month"}],
                },
                "sentence": " The price index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate, stabilized at 1.9% last June, the Office for National Statistics (ONS) said.",
                "object": {
                    "text": "The price index",
                    "keywords": [{"text": "price index"}],
                },
                "action": {
                    "verb": {"text": "cover", "tense": "present"},
                    "text": "covering",
                    "normalized": "cover",
                },
            },
            {
                "subject": {
                    "text": "The price index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate,",
                    "keywords": [
                        {"text": "12-month rate"},
                        {"text": "owner occupiers"},
                        {"text": "price index"},
                        {"text": "costs"},
                    ],
                    "entities": [{"type": "Quantity", "text": "12-month"}],
                },
                "sentence": " The price index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate, stabilized at 1.9% last June, the Office for National Statistics (ONS) said.",
                "object": {
                    "text": "at 1.9%",
                    "entities": [{"type": "Quantity", "text": "1.9"}],
                },
                "action": {
                    "verb": {"text": "stabilize", "tense": "past"},
                    "text": "stabilized",
                    "normalized": "stabilize",
                },
            },
            {
                "subject": {
                    "text": "the Office for National Statistics (ONS)",
                    "keywords": [{"text": "National Statistics"}, {"text": "Office"}],
                },
                "sentence": " The price index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate, stabilized at 1.9% last June, the Office for National Statistics (ONS) said.",
                "object": {
                    "text": "The price index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate, stabilized at 1.9% last June",
                    "keywords": [
                        {"text": "12-month rate"},
                        {"text": "owner occupiers"},
                        {"text": "price index"},
                        {"text": "costs"},
                    ],
                    "entities": [
                        {"type": "Quantity", "text": "12-month"},
                        {"type": "Quantity", "text": "1.9"},
                    ],
                },
                "action": {
                    "verb": {"text": "say", "tense": "past"},
                    "text": "said",
                    "normalized": "say",
                },
            },
            {
                "subject": {
                    "text": "by 0.02%",
                    "entities": [{"type": "Quantity", "text": "0.02"}],
                },
                "sentence": " By 8:40 am GMT, the GBP/USD pair ticked down by 0.02% to $1.2403, while the EUR/GBP pair inched up by 0.05% to GBP 0.9041.",
                "object": {
                    "text": "the GBP/USD pair",
                    "keywords": [{"text": "GBP/USD pair"}],
                },
                "action": {
                    "verb": {"text": "tick", "tense": "past"},
                    "text": "ticked",
                    "normalized": "tick",
                },
            },
            {
                "subject": {
                    "text": "the EUR/GBP pair",
                    "keywords": [{"text": "EUR/GBP pair"}],
                },
                "sentence": " By 8:40 am GMT, the GBP/USD pair ticked down by 0.02% to $1.2403, while the EUR/GBP pair inched up by 0.05% to GBP 0.9041.",
                "object": {
                    "text": "by 0.05%",
                    "entities": [{"type": "Quantity", "text": "0.05"}],
                },
                "action": {
                    "verb": {"text": "inch", "tense": "past"},
                    "text": "inched",
                    "normalized": "inch",
                },
            },
        ],
        "concepts": [
            {
                "text": "Consumer price index",
                "relevance": 0.980874,
                "dbpedia_resource": "http://dbpedia.org/resource/Consumer_price_index",
            },
            {
                "text": "Inflation",
                "relevance": 0.940019,
                "dbpedia_resource": "http://dbpedia.org/resource/Inflation",
            },
            {
                "text": "United Kingdom",
                "relevance": 0.767069,
                "dbpedia_resource": "http://dbpedia.org/resource/United_Kingdom",
            },
            {
                "text": "Price index",
                "relevance": 0.721003,
                "dbpedia_resource": "http://dbpedia.org/resource/Price_index",
            },
            {
                "text": "GDP deflator",
                "relevance": 0.692501,
                "dbpedia_resource": "http://dbpedia.org/resource/GDP_deflator",
            },
            {
                "text": "Bank of England",
                "relevance": 0.60576,
                "dbpedia_resource": "http://dbpedia.org/resource/Bank_of_England",
            },
            {
                "text": "Isle of Man",
                "relevance": 0.546747,
                "dbpedia_resource": "http://dbpedia.org/resource/Isle_of_Man",
            },
            {
                "text": "Northern Ireland",
                "relevance": 0.485999,
                "dbpedia_resource": "http://dbpedia.org/resource/Northern_Ireland",
            },
            {
                "text": "Personal consumption expenditures price index",
                "relevance": 0.479627,
                "dbpedia_resource": "http://dbpedia.org/resource/Personal_consumption_expenditures_price_index",
            },
            {
                "text": "Price indices",
                "relevance": 0.473969,
                "dbpedia_resource": "http://dbpedia.org/resource/Price_indices",
            },
            {
                "text": "Pricing",
                "relevance": 0.473063,
                "dbpedia_resource": "http://dbpedia.org/resource/Pricing",
            },
            {
                "text": "Greenwich Mean Time",
                "relevance": 0.471727,
                "dbpedia_resource": "http://dbpedia.org/resource/Greenwich_Mean_Time",
            },
            {
                "text": "Pound sterling",
                "relevance": 0.46715,
                "dbpedia_resource": "http://dbpedia.org/resource/Pound_sterling",
            },
            {
                "text": "The Football League",
                "relevance": 0.463721,
                "dbpedia_resource": "http://dbpedia.org/resource/The_Football_League",
            },
            {
                "text": "Office for National Statistics",
                "relevance": 0.460135,
                "dbpedia_resource": "http://dbpedia.org/resource/Office_for_National_Statistics",
            },
            {
                "text": "Cost",
                "relevance": 0.443929,
                "dbpedia_resource": "http://dbpedia.org/resource/Cost",
            },
            {
                "text": "Austrian School",
                "relevance": 0.436201,
                "dbpedia_resource": "http://dbpedia.org/resource/Austrian_School",
            },
            {
                "text": "Newport",
                "relevance": 0.432528,
                "dbpedia_resource": "http://dbpedia.org/resource/Newport",
            },
        ],
        "categories": [
            {"score": 0.929122, "label": "/society/work/unemployment"},
            {"score": 0.8178, "label": "/finance/bank"},
            {"score": 0.687864, "label": "/finance/investing"},
        ],
        "relations": [
            {
                "type": "residesIn",
                "sentence": "UK consumer inflation remains unchanged in June 17 July 2019 11:42 AM Last Updated: 17 July 2019 11:42 AM UK consumer inflation remains unchanged in June Mubasher: The UK's consumer price index (CPI), the headline gauge for the country's inflation came in at 2% year-on-year in June, unchanged from May's reading, official data showed on Wednesday.",
                "score": 0.259935,
                "arguments": [
                    {
                        "text": "consumer",
                        "location": [3, 11],
                        "entities": [{"type": "Person", "text": "consumer"}],
                    },
                    {
                        "text": "UK",
                        "location": [0, 2],
                        "entities": [
                            {
                                "type": "GeopoliticalEntity",
                                "text": "UK",
                                "disambiguation": {"subtype": ["Area"]},
                            }
                        ],
                    },
                ],
            },
            {
                "type": "residesIn",
                "sentence": "UK consumer inflation remains unchanged in June 17 July 2019 11:42 AM Last Updated: 17 July 2019 11:42 AM UK consumer inflation remains unchanged in June Mubasher: The UK's consumer price index (CPI), the headline gauge for the country's inflation came in at 2% year-on-year in June, unchanged from May's reading, official data showed on Wednesday.",
                "score": 0.360735,
                "arguments": [
                    {
                        "text": "consumer",
                        "location": [109, 117],
                        "entities": [{"type": "Person", "text": "consumer"}],
                    },
                    {
                        "text": "UK",
                        "location": [106, 108],
                        "entities": [
                            {
                                "type": "GeopoliticalEntity",
                                "text": "UK",
                                "disambiguation": {"subtype": ["Area"]},
                            }
                        ],
                    },
                ],
            },
        ],
        "keywords": [
            {
                "text": "UK consumer inflation",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.861986,
                "count": 2,
            },
            {
                "text": "UK’s consumer price index",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.768116,
                "count": 1,
            },
            {
                "text": "June Mubasher",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.623282,
                "count": 1,
            },
            {
                "text": "stable rate",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.616021,
                "count": 1,
            },
            {
                "text": "drop costs",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.613781,
                "count": 1,
            },
            {
                "text": "last June",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.603799,
                "count": 1,
            },
            {
                "text": "costs of owner occupiers",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.586325,
                "count": 1,
            },
            {
                "text": "motor fuels",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.579883,
                "count": 1,
            },
            {
                "text": "June",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.570813,
                "count": 2,
            },
            {
                "text": "official data",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.548409,
                "count": 1,
            },
            {
                "text": "National Statistics",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.548409,
                "count": 1,
            },
            {
                "text": "headline gauge",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.545437,
                "count": 1,
            },
            {
                "text": "price index",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.540865,
                "count": 1,
            },
            {
                "text": "prices of clothing",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.531839,
                "count": 1,
            },
            {
                "text": "12-month rate",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.530237,
                "count": 1,
            },
            {
                "text": "country’s inflation",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.527516,
                "count": 1,
            },
            {
                "text": "accommodation services",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.5261,
                "count": 1,
            },
            {
                "text": "housing",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.523668,
                "count": 1,
            },
            {
                "text": "CPI",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.523375,
                "count": 1,
            },
            {
                "text": "electricity",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.51895,
                "count": 1,
            },
            {
                "text": "gas",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.517798,
                "count": 1,
            },
            {
                "text": "GBP",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.517551,
                "count": 2,
            },
            {
                "text": "fuels",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.516825,
                "count": 1,
            },
            {
                "text": "EUR",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.509914,
                "count": 1,
            },
            {
                "text": "Office",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.509084,
                "count": 1,
            },
            {
                "text": "ONS",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.505096,
                "count": 1,
            },
            {
                "text": "food",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.504203,
                "count": 1,
            },
            {
                "text": "USD pair",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.475674,
                "count": 1,
            },
            {
                "text": "May’s reading",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.452033,
                "count": 1,
            },
            {
                "text": "GBP pair",
                "sentiment": {"score": 0, "label": "neutral"},
                "relevance": 0.440708,
                "count": 1,
            },
            {
                "text": "July",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.439221,
                "count": 2,
            },
            {
                "text": "CPIH",
                "sentiment": {"score": -0.451439, "label": "negative"},
                "relevance": 0.408025,
                "count": 1,
            },
            {
                "text": "Wednesday",
                "sentiment": {"score": 0.404555, "label": "positive"},
                "relevance": 0.389914,
                "count": 1,
            },
        ],
    },
    "extracted_metadata": {
        "sha1": "e34fd822b3fc8975bba670f06e516ed45dbb6604",
        "filename": "1563352829353.zip-527e1e481efb4333e1e1410fa3af1b03.xml",
        "file_type": "json",
    },
    "external_links": ["http://www.facebook.com/2008/fbml"],
    "title": "UK consumer inflation remains unchanged in June",
    "forum_title": "News Feed",
    "highlight": {
        "enriched_text.semantic_roles.object.text": [
            "accommodation services, electricity, gas and other <em>fuels</em>",
            "The <em>price</em> index",
            "<em>prices</em> of clothing and food",
            "wiped out by climbing <em>prices</em> of clothing and food",
            "The <em>price</em> index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate, stabilized at 1.9% last June",
        ],
        "enriched_text.concepts.dbpedia_resource": [
            "http://dbpedia.org/resource/<em>Pricing</em>"
        ],
        "enriched_text.relations.arguments.entities.text": ["<em>UK</em>"],
        "enriched_text.concepts.text": [
            "<em>Pricing</em>",
            "<em>Price</em> index",
            "<em>Price</em> indices",
            "Consumer <em>price</em> index",
            "Personal consumption expenditures <em>price</em> index",
        ],
        "enriched_title.entities.text": ["<em>UK</em>"],
        "enriched_text.semantic_roles.subject.text": [
            "by climbing <em>prices</em> of clothing and food",
            "This stable rate came after a drop costs of in motor <em>fuels</em>, accommodation services, electricity, gas and other <em>fuels</em>",
            "The <em>price</em> index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate,",
            "accommodation services, electricity, gas and other <em>fuels</em>",
        ],
        "enriched_text.relations.sentence": [
            "<em>UK</em> consumer inflation remains unchanged in June 17 July 2019 11:42 AM Last Updated: 17 July 2019 11:42 AM <em>UK</em> consumer inflation remains unchanged in June Mubasher: The <em>UK's</em> consumer <em>price</em> index (CPI), the headline gauge for the country's inflation came in at 2% year-on-year in June, unchanged from May's reading, official data showed on Wednesday."
        ],
        "enriched_title.relations.arguments.text": ["<em>UK</em>"],
        "url": [
            "https://english.mubasher.info/news/3503627/<em>UK</em>-consumer-inflation-remains-unchanged-in-June"
        ],
        "enriched_text.semantic_roles.object.keywords.text": [
            "<em>fuels</em>",
            "<em>prices</em>",
            "<em>price</em> index",
        ],
        "enriched_title.keywords.text": ["<em>UK</em> consumer inflation"],
        "text": [
            "This stable rate came after a drop costs of in motor <em>fuels</em>, accommodation services, electricity, gas and other <em>fuels</em> was wiped out by climbing <em>prices</em> of clothing and food. The <em>price</em> index, covering the costs of owner occupiers’ housing, (CPIH) 12-month rate, stabilized at 1.9% last June, the Office for"
        ],
        "enriched_text.keywords.text": [
            "<em>UK’s</em> consumer <em>price</em> index",
            "<em>fuels</em>",
            "motor <em>fuels</em>",
            "<em>UK</em> consumer inflation",
            "<em>price</em> index",
        ],
        "enriched_text.entities.text": ["<em>UK</em>"],
        "enriched_text.semantic_roles.sentence": [
            "This stable rate came after a drop costs of in motor <em>fuels</em>, accommodation services, electricity, gas and other <em>fuels</em> was wiped out by climbing <em>prices</em> of clothing and food.",
            "<em>UK</em> consumer inflation remains unchanged in June 17 July 2019 11:42 AM Last Updated: 17 July 2019 11:42 AM <em>UK</em> consumer inflation remains unchanged in June Mubasher: The <em>UK’s</em> consumer <em>price</em> index (CPI), the headline gauge for the country’s inflation came in at 2% year-on-year in June, unchanged from May’s reading, official data showed on Wednesday.",
        ],
        "enriched_title.relations.arguments.entities.text": ["<em>UK</em>"],
        "enriched_title.relations.sentence": [
            "<em>UK</em> consumer inflation remains unchanged in June"
        ],
        "enriched_text.relations.arguments.text": ["<em>UK</em>"],
        "title": ["<em>UK</em> consumer inflation remains unchanged in June"],
        "enriched_text.semantic_roles.subject.keywords.text": [
            "<em>fuels</em>",
            "<em>prices</em>",
            "motor <em>fuels</em>",
            "<em>price</em> index",
        ],
    },
}


text_classification_data = "Supermarkets raise price of petrol almost every day for three months. Posted by Wales Connected | Jul 5, 2019 | Motoring | 0 | The UK’s four big supermarkets have raised the price of petrol almost every day for three months, the RAC can reveal.. Posted by Wales Connected | Jul 5, 2019 | Motoring | 0 | The UK's four big supermarkets have raised the price of petrol almost every day for three months, the RAC can reveal.. Data from RAC Fuel Watch shows the supermarkets, which sell 45% of the country's fuel, have increased the price of unleaded at the pumps virtually every day since 21 February (apart from five days when they stayed the same) in response to rising wholesale costs, but they have done so on days when other retailers have managed to lower their prices.. RAC fuel spokesman Simon Williams said: Our data very clearly shows the wholesale price of unleaded has increased dramatically over the last three months which has inevitably led to forecourt prices rising."


scrape_url_input = [
    "https://media.rac.co.uk/pressreleases/march-sees-welcome-relief-at-the-pumps-as-fuel-drops-by-2-dot-5p-a-litre-1897589",
    "https://media.rac.co.uk/pressreleases/fuel-11-pounds-more-expensive-than-a-year-ago-but-prices-stabilise-in-february-1837553",
    "https://media.rac.co.uk/pressreleases/fuel-rises-2p-a-litre-in-january-to-highest-for-more-than-two-years-1780386",
    "https://media.rac.co.uk/pressreleases/petrol-and-diesel-prices-rise-and-are-at-highest-for-18-months-1722697",
    "https://media.rac.co.uk/pressreleases/petrol-and-diesel-prices-down-in-november-but-rises-on-the-cards-1678228",
    "https://media.rac.co.uk/pressreleases/rac-calls-for-urgent-pump-price-cut-as-wholesale-costs-fall-1643578",
    "https://media.rac.co.uk/pressreleases/october-sees-biggest-petrol-price-rise-at-uk-forecourts-in-three-and-a-half-years-1631154",
    "https://media.rac.co.uk/pressreleases/fuel-prices-edge-up-in-august-despite-early-supermarket-cut-1545260",
    "https://media.rac.co.uk/pressreleases/july-brings-an-end-to-four-months-of-rising-fuel-prices-1504393",
    "https://media.rac.co.uk/pressreleases/rac-issues-plea-for-immediate-pump-price-cuts-1495275",
    "https://media.rac.co.uk/pressreleases/rac-calls-on-fuel-retailers-to-pass-on-wholesale-unleaded-price-savings-1474852",
    "https://media.rac.co.uk/pressreleases/motorists-hit-by-fourth-straight-month-of-fuel-price-rises-1465598",
    "https://media.rac.co.uk/pressreleases/may-sees-price-of-petrol-and-diesel-increase-for-third-month-in-a-row-1428898",
    "https://media.rac.co.uk/pressreleases/price-of-petrol-increases-for-second-month-in-a-row-adding-ps1-45-to-a-fill-up-1394365",
    "https://media.rac.co.uk/pressreleases/price-of-petrol-goes-up-3p-a-litre-in-march-signalling-first-rise-since-july-2015-1361807",
    "https://media.rac.co.uk/pressreleases/february-sees-price-of-petrol-fall-for-eighth-straight-month-1332419",
    "https://media.rac.co.uk/pressreleases/price-of-fuel-may-have-reached-low-point-for-now-warns-the-rac-1307244",
    "https://media.rac.co.uk/pressreleases/petrol-and-diesel-prices-may-go-as-low-as-86p-a-litre-if-oil-price-continues-to-fall-1291895",
    "https://media.rac.co.uk/pressreleases/price-of-petrol-falls-for-sixth-month-in-a-row-with-the-gift-of-sub-ps1-a-litre-1286445",
    "https://media.rac.co.uk/pressreleases/supermarkets-should-lead-the-way-by-selling-diesel-for-under-ps1-a-litre-1274662",
    "https://media.rac.co.uk/pressreleases/petrol-to-fall-to-ps1-a-litre-for-christmas-as-oil-goes-below-40-1269517",
    "https://media.rac.co.uk/pressreleases/a-landmark-fuel-month-diesel-drops-to-lowest-price-in-six-years-and-petrol-drops-for-fifth-month-in-a-row-1266281",
    "https://media.rac.co.uk/pressreleases/petrol-and-diesel-price-cuts-expected-as-oil-hits-40-a-barrel-1255963",
    "https://media.rac.co.uk/pressreleases/price-of-petrol-falls-for-fourth-consecutive-month-1246488",
    "https://media.rac.co.uk/pressreleases/petrol-falls-2p-a-litre-in-september-as-oil-price-stays-below-50-a-barrel-1228303",
    "https://media.rac.co.uk/pressreleases/fuel-falls-more-than-4p-a-litre-in-august-as-oil-price-plummets-to-six-year-low-1211413",
    "https://media.rac.co.uk/pressreleases/diesel-falls-5p-a-litre-in-july-as-retailers-pass-on-wholesale-price-savings-1198362",
    "https://media.rac.co.uk/pressreleases/diesel-wholesale-cheaper-than-petrol-throughout-june-yet-pump-price-gap-still-remains-1188022",
    "https://media.rac.co.uk/pressreleases/may-makes-it-four-miserable-months-of-price-rises-at-the-pumps-2882278",
    "https://media.rac.co.uk/pressreleases/april-sees-second-worst-monthly-petrol-price-rise-since-2000-2867610",
    "https://media.rac.co.uk/pressreleases/a-rough-month-for-drivers-petrol-suffers-second-consecutive-monthly-price-rise-in-march-2855767",
    "https://media.rac.co.uk/pressreleases/fuel-price-rise-in-february-ends-three-months-of-cuts-2842909",
    "https://media.rac.co.uk/pressreleases/petrol-and-diesel-prices-drop-for-third-month-in-a-row-2832710",
    "https://media.rac.co.uk/pressreleases/fuel-prices-drop-again-in-december-but-remain-too-high-2820026",
    "https://media.rac.co.uk/pressreleases/motorists-lose-out-as-retailers-refuse-to-cut-petrol-prices-in-october-despite-drop-in-wholesale-cost-2789219",
    "https://media.rac.co.uk/pressreleases/rac-urges-retailers-to-slash-at-least-3p-a-litre-off-the-price-of-petrol-2760234",
    "https://media.rac.co.uk/pressreleases/drivers-suffer-petrol-price-rises-for-eight-out-of-the-last-12-months-2675566",
    "https://media.rac.co.uk/pressreleases/cost-of-petrol-and-diesel-creep-up-in-july-2617044",
    "https://media.rac.co.uk/pressreleases/drivers-see-some-respite-from-rising-fuel-prices-in-june-but-july-remains-uncertain-2569193",
    "https://media.rac.co.uk/pressreleases/may-sees-worst-increase-in-price-of-petrol-in-at-least-18-years-2529445",
    "https://media.rac.co.uk/pressreleases/fuel-prices-reach-three-and-a-half-year-high-and-worst-still-to-come-2511783",
    "https://media.rac.co.uk/pressreleases/april-sees-worst-rise-in-fuel-prices-for-16-months-2496891",
    "https://media.rac.co.uk/pressreleases/february-brings-relief-for-drivers-at-the-pumps-with-2p-a-litre-drop-2437875",
    "https://media.rac.co.uk/pressreleases/january-sees-fuel-prices-rise-for-third-month-in-row-2411731",
    "https://media.rac.co.uk/pressreleases/petrol-and-diesel-most-expensive-for-three-years-as-prices-go-up-by-2p-a-litre-in-november-2315640",
    "https://media.rac.co.uk/pressreleases/unleaded-price-set-to-overtake-diesel-for-the-first-time-in-over-a-year-as-us-demand-rockets-2130426",
    "https://media.rac.co.uk/pressreleases/june-sees-forecourt-fuel-fall-by-2p-a-litre-for-second-month-in-a-row-2050843",
    "https://media.rac.co.uk/pressreleases/rac-presses-retailers-to-cut-fuel-prices-as-oil-price-slumps-2007888",
]
