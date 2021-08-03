import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    USER_AGENT = ('SecureX Threat Response Integrations '
                  '<tr-integrations-support@cisco.com>')

    GRAYLOG_API_ENDPOINT = 'https://{host}/api/'
    REQUESTED_BY = 'SecureX Threat Response'

    SUPPORTED_TYPES = {
        'amp_computer_guid': 'AMP computer GUID',
        'certificate_common_name': 'certificate common name',
        'certificate_issuer': 'certificate issuer',
        'certificate_serial': 'certificate serial',
        'cisco_mid': 'Cisco message ID',
        'cisco_uc_id': 'Cisco UC ID',
        'device': 'device',
        'domain': 'domain',
        'email': 'email',
        'email_messageid': 'email message ID',
        'email_subject': 'email subject',
        'file_name': 'file name',
        'file_path': 'file path',
        'hostname': 'hostname',
        'imei': 'IMEI',
        'imsi': 'IMSI',
        'ip': 'IP',
        'ipv6': 'IPv6',
        'mac_address': 'MAC address',
        'md5': 'MD5',
        'ms_machine_id': 'Microsoft machine ID',
        'mutex': 'mutex',
        'ngfw_id': 'NGFW ID',
        'ngfw_name': 'NGFW name',
        'odns_identity': 'ODNS identity',
        'odns_identity_label': 'ODNS identity label',
        'orbital_node_id': 'orbital node ID',
        'pki_serial': 'PKI serial',
        'process_name': 'process name',
        'registry_name': 'registry_name',
        'registry_path': 'registry path',
        's1_agent_id': 'SentinelOne agent ID',
        'sha1': 'SHA1',
        'sha256': 'SHA256',
        'swc_device_id': 'SWC device ID',
        'url': 'URL',
        'user': 'user',
        'user_agent': 'user agent',
    }
    CTR_DEFAULT_ENTITIES_LIMIT = 100
