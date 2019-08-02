import boto3
import sys

def main():
    if len(sys.argv)<4:
        print('Usage: python dlm.py {name, max count, type}, update with {name, max count, type, policyId} ')
        sys.exit(0)
    elif len(sys.argv)==5:
        policyid = sys.argv[4]
        name = sys.argv[1]
        count = int(sys.argv[2])
        storeType = sys.argv[3]
        client = boto3.client('dlm')
        response1 = client.update_lifecycle_policy(
        PolicyId=policyid,
        ExecutionRoleArn='arn:aws:iam::411815166437:role/service-role/AWSDataLifecycleManagerDefaultRole',
        State='ENABLED',
        Description='update current policy',
        PolicyDetails={
            'PolicyType': 'EBS_SNAPSHOT_MANAGEMENT',
            'ResourceTypes': [
                storeType,
            ],
            'TargetTags': [
                {
                    'Key': 'Name',
                    'Value': name
                },
            ],
            'Schedules': [
                {
                    'Name': name,
                    'CopyTags': True,
                    'CreateRule': {
                        'Interval': 24,
                        'IntervalUnit': 'HOURS',
                        'Times': [
                        '14:20',
                    ]
                    },
                    'RetainRule': {
                        'Count': count
                    }
                },
            ],
        }
    )
    else:
        name = sys.argv[1]
        count = int(sys.argv[2])
        storeType = sys.argv[3]
        client =  boto3.client('dlm')
        response2 = client.create_lifecycle_policy(
        ExecutionRoleArn='arn:aws:iam::411815166437:role/service-role/AWSDataLifecycleManagerDefaultRole',
        Description='Create a snapshot every 24 hours and the snapshots are stored for around 2 days',
        State='ENABLED',
        PolicyDetails={
            'PolicyType': 'EBS_SNAPSHOT_MANAGEMENT',
            'ResourceTypes': [
                storeType,
            ],
            'TargetTags': [
                {
                    'Key': 'Name',
                    'Value': name
                },

            ],
            'Schedules': [
                {
                    'Name': name,
                    'CopyTags': True,
                    'TagsToAdd': [
                    {
                        'Key': name,
                        'Value': 'EBS volume backup'
                    },
                    ],
                    'CreateRule': {
                        'Interval': 24,
                        'IntervalUnit': 'HOURS',
                        'Times': [
                        '14:20',
                    ]
                    },
                    'RetainRule': {
                        'Count': count
                    }
                },
            ],
        }
    )
        with open('policyId.txt','w') as f:
            f.write(response2['PolicyId']+'\n')

if __name__ == '__main__':
    main()