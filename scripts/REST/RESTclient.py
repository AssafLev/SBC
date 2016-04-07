import json
import logging
import requests
from requests.packages import urllib3

DEFAULT_PORT = 80
SECURED_PORT = 443
SECURED_PROTOCOL = 'https'
DEFAULT_PROTOCOL = 'http'
DEFAULT_API_VERSION = 'v1'

urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

class HTTPClient(object):

    def __init__(self, host, port=DEFAULT_PORT,
                 protocol=DEFAULT_PROTOCOL, api_version=DEFAULT_API_VERSION,
                 headers=None, query_params=None, cert=None, trust_all=False):

        self.port = port
        self.host = host
        self.url = '{0}://{1}:{2}/api/{3}'.format(protocol, host, port,api_version)
        self.headers = headers.copy() if headers else {}
        if not self.headers.get('Content-type'):
            self.headers['Content-type'] = 'application/json'
        self.query_params = query_params.copy() if query_params else {}
        self.logger = logging.getLogger('vTM_client.http')
        self.cert = cert
        self.trust_all = trust_all

    @staticmethod
    def _raise_client_error(response, url=None):
        try:
            result = response.json()
        except Exception:
            message = response.content
            if url:
                message = '{0} [{1}]'.format(message, url)
            error_msg = '{0}: {1}'.format(response.status_code, message)
            raise exceptions.vTMClientError(
                error_msg,
                status_code=response.status_code)
        message = result['message']
        code = result['error_code']
        server_traceback = result['server_traceback']
        error = exceptions.ERROR_MAPPING.get(code,
                                             exceptions.vTMClientError)
        raise error(message, server_traceback,
                    response.status_code, error_code=code)

    def verify_response_status(self, response, expected_code=200):
        if response.status_code != expected_code:
            self._raise_client_error(response)

    def _do_request(self, requests_method, request_url, body, params, headers,
                    expected_status_code, stream, verify):
        response = requests_method(request_url,
                                   data=body,
                                   params=params,
                                   headers=headers,
                                   stream=stream,
                                   verify=verify)
        if self.logger.isEnabledFor(logging.DEBUG):
            for hdr, hdr_content in response.request.headers.iteritems():
                self.logger.debug('request header:  %s: %s'
                                  % (hdr, hdr_content))
            self.logger.debug('reply:  "%s %s" %s'
                              % (response.status_code,
                                 response.reason, response.content))
            for hdr, hdr_content in response.headers.iteritems():
                self.logger.debug('response header:  %s: %s'
                                  % (hdr, hdr_content))

        if response.status_code != expected_status_code:
            self._raise_client_error(response, request_url)

        if stream:
            return StreamedResponse(response)

        return response.json()

    def get_request_verify(self):
        if self.cert:
            # verify will hold the path to the self-signed certificate
            return self.cert
        # certificate verification is required iff trust_all is False
        return not self.trust_all

    def do_request(self,
                   requests_method,
                   uri,
                   data=None,
                   params=None,
                   headers=None,
                   expected_status_code=200,
                   stream=False):
        request_url = '{0}{1}'.format(self.url, uri)

        # build headers
        headers = headers or {}
        total_headers = self.headers.copy()
        total_headers.update(headers)

        # build query params
        params = params or {}
        total_params = self.query_params.copy()
        total_params.update(params)

        # data is either dict, bytes data or None

        is_dict_data = isinstance(data, dict)

        body = json.dumps(data) if is_dict_data else data

        if self.logger.isEnabledFor(logging.DEBUG):
            log_message = 'Sending request: {0} {1}'.format(
                requests_method.func_name.upper(),
                request_url)
            if is_dict_data:
                log_message += '; body: {0}'.format(body)
            elif data is not None:
                log_message += '; body: bytes data'
            self.logger.debug(log_message)
        return self._do_request(
            requests_method=requests_method, request_url=request_url,
            body=body, params=total_params, headers=total_headers,
            expected_status_code=expected_status_code, stream=stream,
            verify=self.get_request_verify())

    def get(self, uri, data=None, params=None, headers=None, _include=None,
            expected_status_code=200, stream=False):
        if _include:
            fields = ','.join(_include)
            if not params:
                params = {}
            params['_include'] = fields
        return self.do_request(requests.get,
                               uri,
                               data=data,
                               params=params,
                               headers=headers,
                               expected_status_code=expected_status_code,
                               stream=stream)

    def put(self, uri, data=None, params=None, headers=None,
            expected_status_code=200, stream=False):
        return self.do_request(requests.put,
                               uri,
                               data=data,
                               params=params,
                               headers=headers,
                               expected_status_code=expected_status_code,
                               stream=stream)

    def patch(self, uri, data=None, params=None, headers=None,
              expected_status_code=200, stream=False):
        return self.do_request(requests.patch,
                               uri,
                               data=data,
                               params=params,
                               headers=headers,
                               expected_status_code=expected_status_code,
                               stream=stream)

    def post(self, uri, data=None, params=None, headers=None,
             expected_status_code=200, stream=False):
        return self.do_request(requests.post,
                               uri,
                               data=data,
                               params=params,
                               headers=headers,
                               expected_status_code=expected_status_code,
                               stream=stream)

    def delete(self, uri, data=None, params=None, headers=None,
               expected_status_code=200, stream=False):
        return self.do_request(requests.delete,
                               uri,
                               data=data,
                               params=params,
                               headers=headers,
                               expected_status_code=expected_status_code,
                               stream=stream)


class StreamedResponse(object):

    def __init__(self, response):
        self._response = response

    @property
    def headers(self):
        return self._response.headers

    def bytes_stream(self, chunk_size=8192):
        return self._response.iter_content(chunk_size)

    def lines_stream(self):
        return self._response.iter_lines()

    def close(self):
        self._response.close()


class deviceClient(object):

    """device client"""

    def __init__(self, host='localhost', port=None, protocol=DEFAULT_PROTOCOL,
                 api_version=DEFAULT_API_VERSION, headers=None,
                 query_params=None, cert=None, trust_all=False):

        if not port:
            if protocol == SECURED_PROTOCOL:
                # SSL
                port = SECURED_PORT
            else:
                port = DEFAULT_PORT

        self._client = HTTPClient(host, port, protocol, api_version,headers, query_params, cert, trust_all)


#        self.plugins = PluginsClient(self._client)

