#!/bin/bash

rm -rf "./target" || true
mkdir "./target"

if [ "$#" -ne 1 ] ; then
  echo "Usage: $0 <s3 bucket>" >&2
  exit 1
fi

s3_bucket=$1

#aws_profile=<Your aws profile>

## package lambda
cd ./lambda; zip "../target/twitter-dm-notif-lambda.zip" *.py; cd ../
# copy to s3 bucket
aws s3 cp target/twitter-dm-notif-lambda.zip s3://${s3_bucket}/twitter-dm-notif-lambda.zip

#twitter_dm_notif_lambda_s3_version=$(aws s3api put-object --bucket ${s3_bucket} --body target/twitter-dm-notif-lambda.zip --key twitter-dm-notif-lambda.zip } | jq -j '.VersionId')
#echo "twitter_dm_notif_lambda_s3_version=${twitter_dm_notif_lambda_s3_version}"

## build/package lambda layer
cd ./lambda/customer_layer; ./build.sh; cp ./twitter-dm-notif-lambda-layer.zip ../../target/; cd ../../
# copy to s3 bucket
aws s3 cp target/twitter-dm-notif-lambda-layer.zip s3://${s3_bucket}/twitter-dm-notif-lambda-layer.zip

#twitter_dm_notif_lambda_layer_s3_version=$(aws s3api put-object --bucket ${s3_bucket} --body target/twitter-dm-notif-lambda-layer.zip --key twitter-dm-notif-lambda-layer.zip } | jq -j '.VersionId')
#echo "twitter_dm_notif_lambda_layer_s3_version=${twitter_dm_notif_lambda_layer_s3_version}"

#aws cloudformation deploy --template ./twitter-dm-notif-lambda.cfn.yml --stack-name twitter-dm-notif-stack  --profile ${aws_profile}
