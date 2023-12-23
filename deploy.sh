#!/bin/sh
if [ -z "${AWS_ACCOUNT_ID}" ]; then
  echo "ERROR: AWS_ACCOUNT_ID is not set"
  exit 1
fi
export ECR_REPOSITORY=${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/discord_toybox:latest

aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com
docker build -t discord_toybox .
docker tag discord_toybox:latest ${ECR_REPOSITORY}
docker push ${ECR_REPOSITORY}
