# twitter-dm-notif
AWS stack to retrieve Twitter DM and send notification

This stack utilize AWS lambda, dynamodb and  SES to retrieve Twitter DM and send email notification.

## Prerequisites:
Set up AWS account so we can deploy the above resources. 
S3 bucket with write access so we can upload artifacts.

Set up Twitter appllication to get  Twitter API key and access token.
Oonce Twitter API key and access token is avaialbe, please update config.pu.


## Package and deploy
package lambda and lambda layer and upload to S3 bucket. It will output S3 version of artifacts uploaded.
$ ./package.sh <your s3 bucket>

deploy cloud formation stack.
$ aws cloudformation deploy --template ./twitter-dm-notif-lambda.cfn.yml --stack-name twitter-dm-notif-stack \
 --profile <your aws profile> \
 --parameter-overrides SharedBucketName=<your s3 bucket> \
 TwitterDMNotifLambdaArtifactS3Version=<above output > \
 TwitterDMNotifLambdaLayerArtifactS3Version=<above output>
