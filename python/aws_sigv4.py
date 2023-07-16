import hashlib
import hmac
import datetime

def generate_signature(key, message):
    return hmac.new(key, message.encode('utf-8'), hashlib.sha256).digest()

def calculate_signature(request, region, service, access_key, secret_key):
    # Step 1: Create a Canonical Request
    http_method = 'GET'
    uri_path = '/my-object.txt'
    query_parameters = 'param1=value1'
    host = 's3.amazonaws.com'
    content_type = 'application/octet-stream'

    canonical_request = f"""{http_method}
{uri_path}
{query_parameters}
host:{host}
content-type:{content_type}

host;content-type
{hashlib.sha256(''.encode('utf-8')).hexdigest()}"""

    # Step 2: Create a String to Sign
    algorithm = 'AWS4-HMAC-SHA256'
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    datestamp = timestamp[:8]
    credential_scope = f"{datestamp}/{region}/{service}/aws4_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    string_to_sign = f"""{algorithm}
{timestamp}
{credential_scope}
{hashed_canonical_request}"""

    # Step 3: Derive the Signing Key
    k_date = generate_signature(('AWS4' + secret_key).encode('utf-8'), datestamp)
    k_region = generate_signature(k_date, region)
    k_service = generate_signature(k_region, service)
    signing_key = generate_signature(k_service, 'aws4_request')

    # Step 4: Calculate the Signature
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    # Step 5: Add the Signature to the Request
    authorization_header = f"{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders=host;content-type, Signature={signature}"

    return authorization_header

# Example usage
region = 'us-west-2'
service = 's3'
access_key = 'YOUR_ACCESS_KEY'
secret_key = 'YOUR_SECRET_KEY'

request = 'GET /my-object.txt?param1=value1 HTTP/1.1\nHost: s3.amazonaws.com'
signature = calculate_signature(request, region, service, access_key, secret_key)
print(signature)
