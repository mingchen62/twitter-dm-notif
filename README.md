# twitter-dm-notif
AWS stack to retrieve Twitter DM and send notification

This stack utilize AWS lambda, dynamodb and  SES to retrieve Twitter DM and send email notification.

## Prerequisites:
* Set up AWS account so we can deploy the above resources. 
* S3 bucket with write access so we can upload artifacts. S3 versioing shall be enabled for the s3 bucket.

* Set up Twitter appllication to get Twitter API key and access token.
Once Twitter API key and access token is avaialbe, please install key/secrets in AWS SSM.
The consumer keys can be found on  application's Details
https://dev.twitter.com/apps (under "OAuth settings")

The access tokens of applications's Details page is located at https://dev.twitter.com/apps (located under "Your access token")
The name conventions of those key/secrets is:

"/third-party/twitter/consumer-key",

"/third-party/twitter/consumer-secret",

"/third-party/twitter/access-token",

"/third-party/twitter/access-token-secret",


## Configuration:

* Install twitter key/secrets in AWS SSM
You can use this command to set those parameters. For example,

$ aws ssm put-parameter  --name "/third-party/twitter/consumer-key" --type SecureString --value <Your twitter app key>
 
$ aws ssm put-parameter --name "/third-party/twitter/consumer-secret"  --type SecureString   --value <Your twitter app secret>
 
$ aws ssm put-parameter --name "/third-party/twitter/access-token"  --type SecureString   --value <Your twitter access token>
 
$ aws ssm put-parameter --name "/third-party/twitter/access-token-secret"  --type SecureString   --value <Your twitter access secret>

You can use this command to confirm those parameters are set correctly

$ 	aws ssm get-parameter --name "/third-party/twitter/consumer-key" --with-decryption

$ 	aws ssm get-parameter --name "/third-party/twitter/consumer-secret" --with-decryption

$ 	aws ssm get-parameter --name "/third-party/twitter/access-token" --with-decryption

$ 	aws ssm get-parameter --name "/third-party/twitter/access-token-secret" --with-decryption

* Configure email address in AWS SES
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-set-up.html
Once sender/reciepent email addresses are verified in AWS SES, you can specify them in cloud formation:
RECEPIENTEMAILADDRESS, SENDEMAILADDRESS

## Package and deploy
* package lambda and lambda layer and upload to S3 bucket. It will output S3 version of artifacts once those artifacts are uploaded.
* 
$ ./package_deploy.sh <your s3 bucket>

* deploy cloud formation stack.
You can deploy vis cloud formation console or use the follwoing command:

$ aws cloudformation deploy --template ./twitter-dm-notif-lambda.cfn.yml --stack-name twitter-dm-notif-stack \
 --profile <your aws profile> \
 --parameter-overrides SharedBucketName=< s3 artifact bucket> \
 TwitterDMNotifLambdaArtifactS3Version=<above output > \
 TwitterDMNotifLambdaLayerArtifactS3Version=<above output>
