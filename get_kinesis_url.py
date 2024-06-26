import boto3
STREAM_NAME = "my_first_test"

kvs = boto3.client("kinesisvideo", region_name='eu-west-1', aws_access_key_id='AKIAYZ3JB5HD7VUDHHWV', aws_secret_access_key= '')

# Grab the endpoint from GetDataEndpoint
endpoint = kvs.get_data_endpoint(APIName="GET_HLS_STREAMING_SESSION_URL", StreamName=STREAM_NAME)['DataEndpoint']

# Grab the HLS Stream URL from the endpoint
kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint,region_name='eu-west-1',aws_access_key_id='',aws_secret_access_key= '')

url = kvam.get_hls_streaming_session_url(StreamName=STREAM_NAME,PlaybackMode="LIVE")['HLSStreamingSessionURL']

print("The url for AWS Kinesis Video Stream is:")
print("\'"+url+"\'")
