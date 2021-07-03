## Getting started with AWS SDK for Python (Boto3)

Boto3 makes it easy to integrate your Python application, library, or script with AWS services including Amazon S3, Amazon EC2, Amazon DynamoDB, and more.


##### Key Features

###### Resource APIs

Boto3 has two distinct levels of APIs. Client (or "low-level") APIs provide one-to-one mappings to the underlying HTTP 
API operations. Resource APIs hide explicit network calls but instead provide resource objects and collections to access 
attributes and perform actions. For example:

```
for i in ec2.instances.all():
    if i.state['Name'] == 'stopped':
        i.start()
```

###### Waiters

Boto3 comes with 'waiters', which automatically poll for pre-defined status changes in AWS resources. For example, you 
can start an Amazon EC2 instance and use a waiter to wait until it reaches the 'running' state, or you can create a new 
Amazon DynamoDB table and wait until it is available to use. Boto3 has waiters for both client and resource APIs.

###### Service-specific High-level Features

Boto3 comes with many features that are service-specific, such as automatic multi-part transfers for Amazon S3 and 
simplified query conditions for Amazon DynamoDB.


##### Resources:

* https://aws.amazon.com/sdk-for-python/
* https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
* https://realpython.com/python-boto3-aws-s3/
* https://harrymoreno.com/2017/04/24/How-to-fill-and-empty-an-s3-bucket-with-python.html