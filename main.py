from enum import Enum
from lxml import etree
from lxml import html
import re
import requests

# Amazon has several page structures. While pages my appear visually the same,
# there are different schemas within the HTML tags.
class RegEx(Enum):
    QandA = "(Q:.*?\n)(?!Q:)([\s\S]+?(?=^Q:|\Z))"
    Question = "(Q(:|\.).*?)</b></p>"
    Answers = "<p>(?!.*Q:)(.*?)</p>"
    QandAParsys = '^(Q(:|\.).*\?)([\s\S]+?(?=^Q:|\Z))'
    QandALBRTXT = '(Q(:|\\.).*\\?)([\s\S]+?(?=^Q:|\Z))'
    Q_LBRTXT = '(^Q(:|\.).*\?)'
    A_LBRTXT = '(.*)'

class AWSPage(Enum):
    Parsys = "//div[@class='parsys content']/div/div[@class='  ']/p"
    RTXT = "//div[@class='lb-txt-16 lb-rtxt']"
    LBRTXT = "//div[@class='lb-rtxt']/p"

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

# directs traffic to appropriate method depending on the response
def extract_elements(rtxt, lbrtxt, parsys):
    if (len(rtxt) > 0):
        print("{} has {} elements for RTXT".format(key, len(rtxt)))
        parse_rtxt(rtxt)
    elif (len(parsys) > 0):
        print("{} has {} elements for Parsys".format(key, len(parsys)))
        parse_parsys(parsys)
    # elif (len(lbrtxt) > 0):
        print("{} has {} elements for LBRTXT".format(key, len(lbrtxt)))
        parse_lbrtxt(lbrtxt)
    else:
        # line to catch unaddressed cases. all cases presently addressed.
        print("NEEDS WORK: {} has no elements.".format(key))

# takes an rtxt element and returns a comma delimited string of question and answer
def parse_rtxt(rtxt):
    lines = []
    for element in rtxt:
        html_element = etree.tostring(element, encoding=str)
        q = ""
        q_match = re.search(RegEx.Question.value, html_element)
        if q_match:
            q = q_match.group(0)
        a = ""
        answer_matches = re.findall(RegEx.Answers.value, html_element)
        for match in answer_matches:
            a = a + "\n" + match
        line_to_store = "{}, {}".format(q, a)
        print(line_to_store)
        lines.append(line_to_store)
    return lines

# takes a parsys element and returns a comma delimited string of question and answer
def parse_parsys(parsys):
    lines = []
    for element in parsys:
        text_contents = element.text_content()
        print(text_contents)
        q_and_a_string = re.search(RegEx.QandAParsys.value, text_contents, re.M)
        q = ""
        a = ""

        if q_and_a_string:
            q = q_and_a_string.group(1)
            a = q_and_a_string.group(3)
        line_to_store = '{}, {}'.format(q, a)
        print(line_to_store)
        lines.append(line_to_store)
    return lines

# Major PITA. Order matters.
# Elements are <p>  and <ul> tags that are children of div<class="lb-rtxt">
# Order is top to bottom.
# 1. get all elements
# 2. if Q:, classify as question
# 3. while not Q:, append to answer
# 4. save as a delimited Q & A string
# 5. return them all once you've looped thru them
# TODO refactor this to be less complex. Should be O(n), not O(n^2)
def parse_lbrtxt(lbrtxt):
    # create a landing spot to hang onto the lines extracted from the lbrtxt object
    raw_lines = []

    # loop through and strip out raw text without HTML tags
    for element in lbrtxt:
        raw_lines.append(element.text_content())

    # next, need to go through the array of stuff
    # (this could be more efficient, but need it out the door. refactor to less complex later.)
    question_to_store = ""
    answer_to_store = ""

    lines_to_return = []

    for line in raw_lines:
        # print(line)
        q_string = re.search(RegEx.Q_LBRTXT.value, line)
        a_string = re.search(RegEx.A_LBRTXT.value, line)

        if q_string:
            # if there's nothing set...
            if not question_to_store:
                # store the string
                question_to_store = q_string.group(0)
            else:
                # save the string in an array and...
                string_to_store = "{}, {}".format(question_to_store, answer_to_store)
                lines_to_return.append(string_to_store)
                # assign the current question_to_store
                question_to_store = q_string.group(0)
                # reset the answer string to accept new assignments
                answer_to_store = ""
        elif a_string:
            answer_to_store = answer_to_store + "\n" + a_string.group(1)
        else:
            print("UNADDRESSED CASE:\n{}".format(line))
    # debug_string = "{} strings in lines_to_return".format(len(lines_to_return))
    # print(debug_string)
    return lines_to_return

for key in faq_dict.keys():
    url = faq_dict[key]
    page = requests.get(url)
    source_code = html.fromstring(page.content)
    rtxt_elements = source_code.xpath(AWSPage.RTXT.value)
    lbrtxt_elements = source_code.xpath(AWSPage.LBRTXT.value)
    parsys_elements = source_code.xpath(AWSPage.Parsys.value)
    extract_elements(rtxt_elements,lbrtxt_elements,parsys_elements)
