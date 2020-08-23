import requests
from lxml import html
from lxml import etree
from enum import Enum
import re



class RegEx(Enum):
    QandA = "(Q:.*?\n)(?!Q:)([\s\S]+?(?=^Q:|\Z))"
    Question = "(Q(:|\.).*?)</b></p>"
    Answers = "<p>(?!.*Q:)(.*?)</p>"


class AWSPage(Enum):
    Parsys = "//div[@class='parsys content']"
    RTXT = "//div[@class='lb-txt-16 lb-rtxt']"
    LBRTXT = "//div[@class='lb-rtxt']"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, AWSPage))


faq_dict = {
    # 'Amazon API Gateway': 'https://aws.amazon.com/api-gateway/faqs/', # expand/collapse
    # 'Amazon Athena': 'https://aws.amazon.com/athena/faqs/',
    # 'Amazon Certificate Manager': 'https://aws.amazon.com/certificate-manager/faqs/',
    # 'Amazon Cloud Directory': 'https://aws.amazon.com/cloud-directory/faqs/',
    # 'Amazon Cloudfront': 'https://aws.amazon.com/cloudfront/faqs/',
    # 'Amazon CloudTrail': 'https://aws.amazon.com/cloudtrail/faqs/',  # expand/collapse
    # 'Amazon CloudWatch': 'https://aws.amazon.com/cloudwatch/faqs/',
    # 'Amazon Cognito': 'https://aws.amazon.com/cognito/faqs/',  # done
    # 'Amazon EBS': 'https://aws.amazon.com/ebs/faqs/',
    # 'Amazon EFS': 'https://aws.amazon.com/efs/faq/',
    # 'Amazon Elastic MapReduce': 'https://aws.amazon.com/elasticmapreduce/faqs/',
    # 'Amazon Elastic Transcoder': 'https://aws.amazon.com/elastictranscoder/faqs/',
    # 'Amazon FSx for Lustre': 'https://aws.amazon.com/fsx/lustre/faqs/',
    # 'Amazon Glacier': 'https://aws.amazon.com/glacier/faqs/',
    # 'Amazon Kinesis': 'https://aws.amazon.com/kinesis/streams/faqs/',
    # 'Amazon Macie': 'https://aws.amazon.com/macie/faq/',
    # 'Amazon Redshift': 'https://aws.amazon.com/redshift/faqs/',
    # 'Amazon Route 53': 'https://aws.amazon.com/route53/faqs/',
    'Amazon S3': 'https://aws.amazon.com/s3/faqs/',
    # 'Amazon Single Sign-On': 'https://aws.amazon.com/single-sign-on/faqs/',
    # 'Amazon VPC': 'https://aws.amazon.com/vpc/faqs/',
    # 'AWS Aurora': 'https://aws.amazon.com/rds/aurora/faqs/',
    # 'AWS Auto Scaling': 'https://aws.amazon.com/autoscaling/faqs/',
    # 'AWS Backup': 'https://aws.amazon.com/backup/faqs/',
    # 'AWS CloudFormation': 'https://aws.amazon.com/cloudformation/faqs/',
    # 'AWS CloudHSM': 'https://aws.amazon.com/cloudhsm/faqs/',
    # 'AWS Database Migration Service': 'https://aws.amazon.com/dms/faqs/',
    # 'AWS DataSyc': 'https://aws.amazon.com/datasync/faqs/',
    # 'AWS Direct Connect': 'https://aws.amazon.com/directconnect/faqs/',
    # 'AWS Directory Service': 'https://aws.amazon.com/directoryservice/faqs/',
    # 'AWS DynamoDB': 'https://aws.amazon.com/dynamodb/faqs/',
    # 'AWS Elasticache': 'https://aws.amazon.com/elasticache/faqs/',  # done
    # 'AWS Fargate': 'https://aws.amazon.com/fargate/faqs/',
    # 'AWS IAM': 'https://aws.amazon.com/iam/faqs/',
    # 'AWS Key Management Service': 'https://aws.amazon.com/kms/faqs/',
    # 'AWS Lambda': 'https://aws.amazon.com/lambda/faqs/',
    # 'AWS RDS': 'https://aws.amazon.com/rds/faqs/',
    # 'AWS Shield': 'https://aws.amazon.com/shield/faqs/',
    # 'AWS Snowball Edge': 'https://aws.amazon.com/snowball-edge/faqs/',
    # 'AWS Snowball': 'https://aws.amazon.com/snowball/faqs/',
    # 'AWS Snowmobile': 'https://aws.amazon.com/snowmobile/faqs/',
    # 'AWS Storage Gateway': 'https://aws.amazon.com/storagegateway/faqs/',
    # 'AWS Trusted Advisor': 'https://aws.amazon.com/premiumsupport/ta-faqs/',  # done
    # 'AWS WAF': 'https://aws.amazon.com/waf/faq/',  # done
    # 'EC2 Autoscaling': 'https://aws.amazon.com/ec2/autoscaling/faqs/',
    # 'EC2 Elastic Beanstalk': 'https://aws.amazon.com/elasticbeanstalk/faqs/',
    # 'EC2 Windows': 'https://aws.amazon.com/windows/faq/',  # done
    # 'EC2': 'https://aws.amazon.com/ec2/faqs/',
    # 'Elastic Load Balancing': 'https://aws.amazon.com/elasticloadbalancing/faqs/',
}

# TODO method to parse regex

# TODO method to parse the array of HTML elements
def extract_elements(rtxt, lbrtxt, parsys):
    if (len(rtxt) > 0):
        print("{} has {} elements for RTXT".format(key, len(rtxt)))
        parse_rtxt(rtxt)
        # continue
    # elif (len(parsys) > 0):
    #     print("{} has {} elements for Parsys".format(key, len(parsys)))
    #     # continue
    # elif (len(lbrtxt) > 0):
    #     print("{} has {} elements for LBRTXT".format(key, len(lbrtxt)))
    #     # continue
    else:
        print("NEEDS WORK: {} has no elements.".format(key))


# takes an rtxt element and returns a comma delimited string of question and answer
def parse_rtxt(rtxt):
    lines = []
    for element in rtxt:
        html_element = etree.tostring(element, encoding=str)
        question_string = ""
        q_match = re.search(RegEx.Question.value,html_element, re.UNICODE)
        if q_match:
            question_string = q_match.group(0)
        answer_string = ""
        answer_matches = re.findall(RegEx.Answers.value,html_element,re.UNICODE)
        for match in answer_matches:
            answer_string = answer_string + "\n" + match
        lines.append("{}, {}".format(question_string, answer_string))
    print(len(lines))
    return lines

# once script is written, decompose it to separate concerns

keys = faq_dict.keys()
for key in faq_dict.keys():
    url = faq_dict[key]
    page = requests.get(url)
    source_code = html.fromstring(page.content)
    rtxt_elements = source_code.xpath(AWSPage.RTXT.value)
    lbrtxt_elements = source_code.xpath(AWSPage.LBRTXT.value)
    parsys_elements = source_code.xpath(AWSPage.Parsys.value)
    extract_elements(rtxt_elements,lbrtxt_elements,parsys_elements)
