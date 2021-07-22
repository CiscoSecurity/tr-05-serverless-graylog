import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    USER_AGENT = ('SecureX Threat Response Integrations '
                  '<tr-integrations-support@cisco.com>')

    GRAYLOG_API_ENDPOINT = 'https://{host}/api/'
    REQUESTED_BY = 'SecureX Threat Response'

    SUPPORTED_TYPES = [
        'ip',
        'ipv6',
        'device',
        'user',
        'domain',
        'sha256',
        'md5',
        'sha1',
        'url',
        'pki_serial',
        'email',
        'imei',
        'imsi',
        'amp_computer_guid',
        'hostname',
        'mac_address',
        'file_name',
        'file_path',
        'odns_identity',
        'odns_identity_label',
        'email_messageid',
        'email_subject',
        'cisco_mid',
        'mutex',
    ]

    CTR_DEFAULT_ENTITIES_LIMIT = 100
