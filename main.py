import requests
from lxml import html
from enum import Enum
import re


class RegEx(Enum):
    QandA = "(Q:.*?\n)(?!Q:)([\s\S]+?(?=^Q:|\Z))"


class AWSPage(Enum):
    Parsys = "//div[@class='parsys content']"
    RTXT = "//div[@class='lb-txt-16 lb-rtxt']"
    LBRTXT = "//div[@class='lb-rtxt']"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, AWSPage))


faq_dict = {
    'Amazon API Gateway': 'https://aws.amazon.com/api-gateway/faqs/', # expand/collapse
    'Amazon Athena': 'https://aws.amazon.com/athena/faqs/',
    'Amazon Certificate Manager': 'https://aws.amazon.com/certificate-manager/faqs/',
    'Amazon Cloud Directory': 'https://aws.amazon.com/cloud-directory/faqs/',
    'Amazon Cloudfront': 'https://aws.amazon.com/cloudfront/faqs/',
    'Amazon CloudTrail': 'https://aws.amazon.com/cloudtrail/faqs/',  # expand/collapse
    'Amazon CloudWatch': 'https://aws.amazon.com/cloudwatch/faqs/',
    'Amazon Cognito': 'https://aws.amazon.com/cognito/faqs/',  # done
    'Amazon EBS': 'https://aws.amazon.com/ebs/faqs/',
    'Amazon EFS': 'https://aws.amazon.com/efs/faq/',
    'Amazon Elastic MapReduce': 'https://aws.amazon.com/elasticmapreduce/faqs/',
    'Amazon Elastic Transcoder': 'https://aws.amazon.com/elastictranscoder/faqs/',
    'Amazon FSx for Lustre': 'https://aws.amazon.com/fsx/lustre/faqs/',
    'Amazon Glacier': 'https://aws.amazon.com/glacier/faqs/',
    'Amazon Kinesis': 'https://aws.amazon.com/kinesis/streams/faqs/',
    'Amazon Macie': 'https://aws.amazon.com/macie/faq/',
    'Amazon Redshift': 'https://aws.amazon.com/redshift/faqs/',
    'Amazon Route 53': 'https://aws.amazon.com/route53/faqs/',
    'Amazon S3': 'https://aws.amazon.com/s3/faqs/',
    'Amazon Single Sign-On': 'https://aws.amazon.com/single-sign-on/faqs/',
    'Amazon VPC': 'https://aws.amazon.com/vpc/faqs/',
    'AWS Aurora': 'https://aws.amazon.com/rds/aurora/faqs/',
    'AWS Auto Scaling': 'https://aws.amazon.com/autoscaling/faqs/',
    'AWS Backup': 'https://aws.amazon.com/backup/faqs/',
    'AWS CloudFormation': 'https://aws.amazon.com/cloudformation/faqs/',
    'AWS CloudHSM': 'https://aws.amazon.com/cloudhsm/faqs/',
    'AWS Database Migration Service': 'https://aws.amazon.com/dms/faqs/',
    'AWS DataSyc': 'https://aws.amazon.com/datasync/faqs/',
    'AWS Direct Connect': 'https://aws.amazon.com/directconnect/faqs/',
    'AWS Directory Service': 'https://aws.amazon.com/directoryservice/faqs/',
    'AWS DynamoDB': 'https://aws.amazon.com/dynamodb/faqs/',
    'AWS Elasticache': 'https://aws.amazon.com/elasticache/faqs/',  # done
    'AWS Fargate': 'https://aws.amazon.com/fargate/faqs/',
    'AWS IAM': 'https://aws.amazon.com/iam/faqs/',
    'AWS Key Management Service': 'https://aws.amazon.com/kms/faqs/',
    'AWS Lambda': 'https://aws.amazon.com/lambda/faqs/',
    'AWS RDS': 'https://aws.amazon.com/rds/faqs/',
    'AWS Shield': 'https://aws.amazon.com/shield/faqs/',
    'AWS Snowball Edge': 'https://aws.amazon.com/snowball-edge/faqs/',
    'AWS Snowball': 'https://aws.amazon.com/snowball/faqs/',
    'AWS Snowmobile': 'https://aws.amazon.com/snowmobile/faqs/',
    'AWS Storage Gateway': 'https://aws.amazon.com/storagegateway/faqs/',
    'AWS Trusted Advisor': 'https://aws.amazon.com/premiumsupport/ta-faqs/',  # done
    'AWS WAF': 'https://aws.amazon.com/waf/faq/',  # done
    'EC2 Autoscaling': 'https://aws.amazon.com/ec2/autoscaling/faqs/',
    'EC2 Elastic Beanstalk': 'https://aws.amazon.com/elasticbeanstalk/faqs/',
    'EC2 Windows': 'https://aws.amazon.com/windows/faq/',  # done
    'EC2': 'https://aws.amazon.com/ec2/faqs/',
    'Elastic Load Balancing': 'https://aws.amazon.com/elasticloadbalancing/faqs/',
}

keys = faq_dict.keys()

def text_from_source(feature, source_code) -> str:
    content_types = AWSPage.list()

    for content_type in content_types:
        assert isinstance(content_type, str)
        if len(source_code.xpath(content_type)) > 0:
            # print("{} is valid".format(feature))
            return source_code.xpath(content_type)
        else:
            print("{} is INVALID".format(feature))

for key in faq_dict.keys():
    url = faq_dict[key]
    page = requests.get(url)
    source_code = html.fromstring(page.content)
    # text_only = source_code.text_content()
    # print(source_code.text_content())
    rtxt_elements = source_code.xpath(AWSPage.RTXT.value)
    lbrtxt_elements = source_code.xpath(AWSPage.LBRTXT.value)
    parsys_elements = source_code.xpath(AWSPage.Parsys.value)
    if (len(rtxt_elements) > 0):
        print("{} has {} elements for RTXT".format(key, len(rtxt_elements)))
        continue
    elif (len(parsys_elements) > 0):
        print("{} has {} elements for Parsys".format(key, len(parsys_elements)))
        continue
    elif (len(lbrtxt_elements) > 0):
        print("{} has {} elements for LBRTXT".format(key, len(lbrtxt_elements)))
        continue
    else:
        print("NEEDS WORK: {} has no elements.".format(key))

    # print(len(parsys_elements))




    # matches = re.findall(RegEx.QandA.value, text_only, re.DOTALL)
    # regex_sequence = re.compile(RegEx.QandA.value, re.MULTILINE)
    # for match in regex_sequence.finditer(text_only):
    #     print(match)

    # matches = re.findall(regex_sequence, text_only, re.DOTALL)
    # print(len(matches))
    # print(matches[0])

    # tree = source_code.xpath(AWSPage.ContentA.value)
    # questions = text_from_source(key, source_code)
    # print(tree[0].text_content())
