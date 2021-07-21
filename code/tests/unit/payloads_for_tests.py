EXPECTED_RESPONSE_OF_JWKS_ENDPOINT = {
  'keys': [
    {
      'kty': 'RSA',
      'n': 'tSKfSeI0fukRIX38AHlKB1YPpX8PUYN2JdvfM-XjNmLfU1M74N0V'
           'mdzIX95sneQGO9kC2xMIE-AIlt52Yf_KgBZggAlS9Y0Vx8DsSL2H'
           'vOjguAdXir3vYLvAyyHin_mUisJOqccFKChHKjnk0uXy_38-1r17'
           '_cYTp76brKpU1I4kM20M__dbvLBWjfzyw9ehufr74aVwr-0xJfsB'
           'Vr2oaQFww_XHGz69Q7yHK6DbxYO4w4q2sIfcC4pT8XTPHo4JZ2M7'
           '33Ea8a7HxtZS563_mhhRZLU5aynQpwaVv2U--CL6EvGt8TlNZOke'
           'Rv8wz-Rt8B70jzoRpVK36rR-pHKlXhMGT619v82LneTdsqA25Wi2'
           'Ld_c0niuul24A6-aaj2u9SWbxA9LmVtFntvNbRaHXE1SLpLPoIp8'
           'uppGF02Nz2v3ld8gCnTTWfq_BQ80Qy8e0coRRABECZrjIMzHEg6M'
           'loRDy4na0pRQv61VogqRKDU2r3_VezFPQDb3ciYsZjWBr3HpNOkU'
           'jTrvLmFyOE9Q5R_qQGmc6BYtfk5rn7iIfXlkJAZHXhBy-ElBuiBM'
           '-YSkFM7dH92sSIoZ05V4MP09Xcppx7kdwsJy72Sust9Hnd9B7V35'
           'YnVF6W791lVHnenhCJOziRmkH4xLLbPkaST2Ks3IHH7tVltM6NsR'
           'k3jNdVM',
      'e': 'AQAB',
      'alg': 'RS256',
      'kid': '02B1174234C29F8EFB69911438F597FF3FFEE6B7',
      'use': 'sig'
    }
  ]
}

RESPONSE_OF_JWKS_ENDPOINT_WITH_WRONG_KEY = {
    'keys': [
        {
            'kty': 'RSA',
            'n': 'pSKfSeI0fukRIX38AHlKB1YPpX8PUYN2JdvfM-XjNmLfU1M74N0V'
                 'mdzIX95sneQGO9kC2xMIE-AIlt52Yf_KgBZggAlS9Y0Vx8DsSL2H'
                 'vOjguAdXir3vYLvAyyHin_mUisJOqccFKChHKjnk0uXy_38-1r17'
                 '_cYTp76brKpU1I4kM20M__dbvLBWjfzyw9ehufr74aVwr-0xJfsB'
                 'Vr2oaQFww_XHGz69Q7yHK6DbxYO4w4q2sIfcC4pT8XTPHo4JZ2M7'
                 '33Ea8a7HxtZS563_mhhRZLU5aynQpwaVv2U--CL6EvGt8TlNZOke'
                 'Rv8wz-Rt8B70jzoRpVK36rR-pHKlXhMGT619v82LneTdsqA25Wi2'
                 'Ld_c0niuul24A6-aaj2u9SWbxA9LmVtFntvNbRaHXE1SLpLPoIp8'
                 'uppGF02Nz2v3ld8gCnTTWfq_BQ80Qy8e0coRRABECZrjIMzHEg6M'
                 'loRDy4na0pRQv61VogqRKDU2r3_VezFPQDb3ciYsZjWBr3HpNOkU'
                 'jTrvLmFyOE9Q5R_qQGmc6BYtfk5rn7iIfXlkJAZHXhBy-ElBuiBM'
                 '-YSkFM7dH92sSIoZ05V4MP09Xcppx7kdwsJy72Sust9Hnd9B7V35'
                 'YnVF6W791lVHnenhCJOziRmkH4xLLbPkaST2Ks3IHH7tVltM6NsR'
                 'k3jNdVM',
            'e': 'AQAB',
            'alg': 'RS256',
            'kid': '02B1174234C29F8EFB69911438F597FF3FFEE6B7',
            'use': 'sig'
        }
    ]
}

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

EXPECTED_RESPONSE_FROM_GRAYLOG = {
    "execution": {
        "done": True,
        "cancelled": False,
        "completed_exceptionally": False
    },
    "results": {
        "query_id": {
            "query": {
                "id": "query_id",
                "timerange": {
                    "type": "relative",
                    "range": 12592000
                },
                "filter": {
                    "type": "or",
                    "filters": [
                        {
                            "type": "stream",
                            "filters": None,
                            "id": "000000000000000000000001",
                            "title": None
                        },
                        {
                            "type": "stream",
                            "filters": None,
                            "id": "60bf6fd4024ad37a05cbb006",
                            "title": None
                        }
                    ]
                },
                "query": {
                    "type": "elasticsearch",
                    "query_string": "\"24.141.154.216\""
                },
                "search_types": [
                    {
                        "timerange": None,
                        "query": None,
                        "streams": [],
                        "id": "search_type_id",
                        "name": None,
                        "limit": 101,
                        "offset": 0,
                        "sort": [
                            {
                                "field": "timestamp",
                                "order": "DESC"
                            }
                        ],
                        "decorators": [],
                        "type": "messages",
                        "filter": None
                    }
                ]
            },
            "execution_stats": {
                "duration": 33,
                "timestamp": "2021-07-20T12:37:42.058Z",
                "effective_timerange": {
                    "type": "absolute",
                    "from": "2021-02-24T18:51:02.091Z",
                    "to": "2021-07-20T12:37:42.091Z"
                }
            },
            "search_types": {
                "search_type_id": {
                    "id": "search_type_id",
                    "messages": [
                        {
                            "highlight_ranges": {},
                            "message": {
                                "gl2_accounted_message_size": 221,
                                "level": 3,
                                "gl2_remote_ip": "::1",
                                "gl2_remote_port": 43339,
                                "streams": [
                                    "000000000000000000000001"
                                ],
                                "gl2_message_id": "01F7NTA7TRK9Q36QN6Q03PKSJE",
                                "source": "%ASA-3-710003:",
                                "message": "%ASA-3-710003: TCP access denied by ACL from 49.143.32.6/4222 to outside:24.141.154.216/23",
                                "gl2_source_input": "60bf6485024ad37a05cba39c",
                                "facility_num": 20,
                                "gl2_source_node": "80fe6cad-d153-489f-91a8-beee65b2e27c",
                                "_id": "f5999d80-c856-11eb-a871-000c293368b3",
                                "facility": "local4",
                                "timestamp": "2021-06-08T12:42:17.816Z"
                            },
                            "index": "graylog_0",
                            "decoration_stats": None
                        },
                        {
                            "highlight_ranges": {},
                            "message": {
                                "gl2_accounted_message_size": 222,
                                "level": 3,
                                "gl2_remote_ip": "::1",
                                "gl2_remote_port": 49754,
                                "streams": [
                                    "000000000000000000000001"
                                ],
                                "gl2_message_id": "01F7NT94374GXQMJRV7GAH5AKM",
                                "source": "%ASA-3-710003:",
                                "message": "%ASA-3-710003: TCP access denied by ACL from 5.34.129.87/62507 to outside:24.141.154.216/23",
                                "gl2_source_input": "60bf6485024ad37a05cba39c",
                                "facility_num": 20,
                                "gl2_source_node": "80fe6cad-d153-489f-91a8-beee65b2e27c",
                                "_id": "dfc9f770-c856-11eb-a871-000c293368b3",
                                "facility": "local4",
                                "timestamp": "2021-06-08T12:41:41.223Z"
                            },
                            "index": "graylog_0",
                            "decoration_stats": None
                        },
                        {
                            "highlight_ranges": {},
                            "message": {
                                "gl2_accounted_message_size": 225,
                                "level": 3,
                                "gl2_remote_ip": "::1",
                                "gl2_remote_port": 48544,
                                "streams": [
                                    "000000000000000000000001"
                                ],
                                "gl2_message_id": "01F7NT7J8GGPSBNB6RFHH3P31A",
                                "source": "%ASA-3-710003:",
                                "message": "%ASA-3-710003: TCP access denied by ACL from 156.96.156.172/50168 to outside:24.141.154.216/80",
                                "gl2_source_input": "60bf6485024ad37a05cba39c",
                                "facility_num": 20,
                                "gl2_source_node": "80fe6cad-d153-489f-91a8-beee65b2e27c",
                                "_id": "c15f4100-c856-11eb-a871-000c293368b3",
                                "facility": "local4",
                                "timestamp": "2021-06-08T12:40:50.192Z"
                            },
                            "index": "graylog_0",
                            "decoration_stats": None
                        },
                        {
                            "highlight_ranges": {},
                            "message": {
                                "gl2_accounted_message_size": 223,
                                "level": 3,
                                "gl2_remote_ip": "::1",
                                "gl2_remote_port": 47419,
                                "streams": [
                                    "000000000000000000000001"
                                ],
                                "gl2_message_id": "01F7NT4RFEHY8F2Y4VP1RT5T5F",
                                "source": "ASA-3-710003:",
                                "message": "ASA-3-710003: TCP access denied by ACL from 156.96.156.172/50168 to outside:24.141.154.216/80",
                                "gl2_source_input": "60bf6485024ad37a05cba39c",
                                "facility_num": 20,
                                "gl2_source_node": "80fe6cad-d153-489f-91a8-beee65b2e27c",
                                "_id": "8a8cfb90-c856-11eb-a871-000c293368b3",
                                "facility": "local4",
                                "timestamp": "2021-06-08T12:39:18.216Z"
                            },
                            "index": "graylog_0",
                            "decoration_stats": None
                        }
                    ],
                    "effective_timerange": {
                        "type": "absolute",
                        "from": "2021-02-24T18:51:02.091Z",
                        "to": "2021-07-20T12:37:42.091Z"
                    },
                    "total_results": 4,
                    "type": "messages"
                }
            },
            "errors": [],
            "state": "COMPLETED"
        }
    },
    "id": "60f6c39681e5cd7cd5e9ad9a",
    "owner": "admin",
    "search_id": None
}
