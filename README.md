



### Creating IAM credencial required with AWS CLI




### Creating a Key pairs

Amazon EC2/EMR (and all products) uses public–key cryptography to encrypt and decrypt login information. Public–key cryptography uses a public key to encrypt a piece of data, such as a password, then the recipient uses the private key to decrypt the data. The public and private keys are known as a key pair.

To log in our Cluster or Instance, we must create a key pair, specify the name of the key pair when you launch the instance, and provide the private key when you connect to the instance. Linux instances have no password, and you use a key pair to log in using SSH.

To create a key pair: 

- Go to [EC2 dashboard](https://eu-west-1.console.aws.amazon.com/ec2/) and click "Create Key Pair".

After this, PEM file will be downloaded, please store this file in a safe location in your computer.


Set ``400`` permissions mask to PEM file (to avoid this problem connecting with ssh: [PEM Error](#errors/errors.md#UNPROTECTED PRIVATE KEY FILE)).

```
chmod 400 /home/manuparra/.ssh/PredictivaIO.pem
```


### Creating a simple Spark Cluster with the next features:

- **emr**: 5.4.0 see [releases](http://docs.aws.amazon.com//emr/latest/ReleaseGuide/images/emr-5.4.0.png).
- **KeyName**: Name of the Key Pair generated from EC2/KeyPairs  (not the ``.pem`` file).
- **Name**: Name of the software-sandbox. Here you can add more software bundles.
- **m3.xlarge**: Flavour of the instances.
- **instance-count**: Number of instances counting the master (ie. 2 -> 1 master 1 slave).


```
aws emr create-cluster --name "SparkClusterTest" --release-label emr-5.4.0 --applications Name=Spark --ec2-attributes KeyName=PredictivaIO --instance-type m3.xlarge --instance-count 2 --use-default-roles
```

after this, you will get Cluster ID in JSON this format:

```
{
    "ClusterId": "j-26H8B5P1XGYM0"
}
```

Check the status of the created cluster:

```
aws emr list-clusters
```

Check the status of active/terminated or failed Clusters (``[--active | --terminated | --failed]``)

```
aws emr list-clusters --active
```

This show the following:

```
{
    "Clusters": [
        {
            "Status": {
                "Timeline": {
                    "ReadyDateTime": 1490305701.226, 
                    "CreationDateTime": 1490305385.744
                }, 
                "State": "WAITING", 
                "StateChangeReason": {
                    "Message": "Cluster ready to run steps."
                }
            }, 
            "NormalizedInstanceHours": 16, 
            "Id": "j-26H8B5P1XGYM0", 
            "Name": "Spark cluster"
        }
    ]
}
```

In this moment the Cluster is ``WAITING``. 

Valid cluster states  include: ``STARTING``, ``BOOTSTRAPPING``, ``RUNNING``, ``WAITING``, ``TERMINATING``, ``TERMINATED``, and ``TERMINATED_WITH_ERRORS``.


We can see all details about the cluster created:

```
aws emr list-instances --cluster-id  j-26H8B5P1XGYM0
```

Output is:

```
{
    "Instances": [
        {
            "Status": {
                "Timeline": {
                    "CreationDateTime": 1490356300.053
                }, 
                "State": "BOOTSTRAPPING", 
                "StateChangeReason": {}
            }, 
            "Ec2InstanceId": "i-001855d3651ae1054", 
            "EbsVolumes": [], 
            "PublicDnsName": "ec2-54-229-82-137.eu-west-1.compute.amazonaws.com", 
            "InstanceType": "m3.xlarge", 
            "PrivateDnsName": "ip-172-31-21-212.eu-west-1.compute.internal", 
            "Market": "ON_DEMAND", 
            "PublicIpAddress": "54.229.82.137", 
            "InstanceGroupId": "ig-31OMOWVJ48XGJ", 
            "Id": "ci-32ELRJPXEQOR7", 
            "PrivateIpAddress": "172.31.21.212"
        }, 
        {
            "Status": {
                "Timeline": {
                    "CreationDateTime": 1490356300.053
                }, 
                "State": "BOOTSTRAPPING", 
                "StateChangeReason": {}
            }, 
            "Ec2InstanceId": "i-0ca767cb507dcfd2f", 
            "EbsVolumes": [], 
            "PublicDnsName": "ec2-54-194-201-167.eu-west-1.compute.amazonaws.com", 
            "InstanceType": "m3.xlarge", 
            "PrivateDnsName": "ip-172-31-20-141.eu-west-1.compute.internal", 
            "Market": "ON_DEMAND", 
            "PublicIpAddress": "54.194.201.167", 
            "InstanceGroupId": "ig-1JJADD5HFSD8N", 
            "Id": "ci-1UNET4ZQB58AD", 
            "PrivateIpAddress": "172.31.20.141"
        }
    ]
}
```


### Connecting with SSH

```
aws emr ssh --cluster-id j-26H8B5P1XGYM0 --key-pair-file /home/manuparra/.ssh/PredictivaIO.pem 
```

If you have the [PEM Error](#errors/errors.md#UNPROTECTED PRIVATE KEY FILE)) solve it, and try out ssh again.

If the command was fine you will get the next (so, you are connected to the Cluster created):

```

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/
18 package(s) needed for security, out of 41 available
Run "sudo yum update" to apply all updates.
                                                                    
EEEEEEEEEEEEEEEEEEEE MMMMMMMM           MMMMMMMM RRRRRRRRRRRRRRR    
E::::::::::::::::::E M:::::::M         M:::::::M R::::::::::::::R   
EE:::::EEEEEEEEE:::E M::::::::M       M::::::::M R:::::RRRRRR:::::R 
  E::::E       EEEEE M:::::::::M     M:::::::::M RR::::R      R::::R
  E::::E             M::::::M:::M   M:::M::::::M   R:::R      R::::R
  E:::::EEEEEEEEEE   M:::::M M:::M M:::M M:::::M   R:::RRRRRR:::::R 
  E::::::::::::::E   M:::::M  M:::M:::M  M:::::M   R:::::::::::RR   
  E:::::EEEEEEEEEE   M:::::M   M:::::M   M:::::M   R:::RRRRRR::::R  
  E::::E             M:::::M    M:::M    M:::::M   R:::R      R::::R
  E::::E       EEEEE M:::::M     MMM     M:::::M   R:::R      R::::R
EE:::::EEEEEEEE::::E M:::::M             M:::::M   R:::R      R::::R
E::::::::::::::::::E M:::::M             M:::::M RR::::R      R::::R
EEEEEEEEEEEEEEEEEEEE MMMMMMM             MMMMMMM RRRRRRR      RRRRRR
                                                                    
[hadoop@ip-172-31-18-31 ~]$ 

```

### Starting interactive BigData Analytics

Spark supports Scala, Python and R. We can choose to write them as standalone Spark applications, or within an interactive interpreter.

Once logged in you can use three possible interactive development environments that brings the cluster (by default):

#### Python

We can use pyspark interactive shell:

```
[hadoop@ip-[redacted] ~]$ pyspark
```

Press ``CRTL+D`` to exit or write ``exit``.

#### Scala

```
[hadoop@ip-[redacted] ~]$ spark-shell
```

Press ``CRTL+D`` to exit or write ``exit``.

#### R

```
[hadoop@ip-[redacted] ~]$ sparkR
```

Press ``CRTL+D`` to exit or write ``exit``.


### Terminating the simple Spark Cluster

Use AWS CLI:

```
aws emr terminate-clusters --cluster-id j-26H8B5P1XGYM0
````

You can check if the Cluster is terminated:

```
aws emr list-clusters --terminated
```


### Adding applications on cluster creationg time

EMR release contains several distributed applications available for installation on your cluster in all-in-one deployment. EMR defines each application as not only the set of the components which comprise that open source project but also a set of associated components which are required for that the application to function. 

When you choose to install an application using the console, API, or CLI, Amazon EMR installs and configures this set of components across nodes in your cluster. The following applications are supported for this release: 

- Flink 
- Ganglia
- Hadoop 
- HBase 
- Hive
- Mahout
- Spark
- Zeppelin and [more](http://docs.aws.amazon.com//emr/latest/ReleaseGuide/emr-release-components.html).


#### Cluster with Spark, Hadoop, YARN with Ganglia, and Zeppelin

Add ``--application Name=XXXX Name=YYYY, ...`` to AWS CLI creation command:

```
aws emr create-cluster --name "SparkClusterTest01" --release-label emr-5.4.0 --applications Name=Spark Name=Hadoop Name=Ganglia Name=Zeppelin --ec2-attributes KeyName=PredictivaIO --instance-type m3.xlarge --instance-count 2 --use-default-roles
```

Try connect with SSH:

```
aws emr ssh --cluster-id <Cluster ID> --key-pair-file /home/manuparra/.ssh/PredictivaIO.pem 
```

Remember terminate your cluster is you have finished your job:

```
aws emr terminate-clusters --cluster-id j-26H8B5P1XGYM0
````


#### Cluster with Spark and Zeppelin

Just add only ``Name=Spark`` and ``Name=Zeppelin`` :

```
aws emr create-cluster --name "SparkClusterTest02" --release-label emr-5.4.0 --applications Name=Spark Name=Zeppelin --ec2-attributes KeyName=PredictivaIO --instance-type m3.xlarge --instance-count 2 --use-default-roles
```

Try connect with SSH:

```
aws emr ssh --cluster-id <Cluster ID> --key-pair-file /home/manuparra/.ssh/PredictivaIO.pem 
```



### Override Cluster Software configuration

You can override the default configurations for applications you install by supplying a configuration object when specifying applications you want installed at cluster creation time.

#### Creating Cluster and add support with Zeppelin interactive analytics 

Sometimes software installed on the cluster probably use a port to comunicate with it.

To add support to aditional software and show the software on external port, we need to create a RULE on Security group. 

Security group acts as a virtual firewall that controls the traffic for one or more instances. When you launch an instance, you associate one or more security groups with the instance. You add rules to each security group that allow traffic to or from its associated instances. You can modify the rules for a security group at any time; the new rules are automatically applied to all instances that are associated with the security group. When we decide whether to allow traffic to reach an instance, we evaluate all the rules from all the security groups that are associated with the instance.

To create or to add a new rule, go to [Security Groups](https://eu-west-1.console.aws.amazon.com/ec2/v2/home?region=eu-west-1#SecurityGroups:sort=groupId) in the menu EC2 (choose SecurityGroups) and 
select:

- ElasticMapReduce-master ... (Master group for Elastic MapReduce created on ....)

and Edit Rules on INBOUND :

- Add Custom TCP o UDP Rule
- Add the port specific for the software
- Add Source and choose: Anywhere

We create new Cluster with Zeppelin support:

```
aws emr create-cluster --name "SparkClusterTest" --release-label emr-5.4.0 --applications Name=Spark Name=Hadoop Name=Ganglia Name=Zeppelin --ec2-attributes KeyName=PredictivaIO --instance-type m3.xlarge --instance-count 2 --use-default-roles
```

After it has been created, check the details of the cluster and get the Public DNS  Name:

```
aws emr list-instances --cluster-id j-XXXXXXXXXX
````

Check the PublicDNSName :


```
    ...
    "PublicDnsName": "ec2-54-229-189-0.eu-west-1.compute.amazonaws.com", 
    ...
```

And now, in your browser:

http://ec2-54-229-189-0.eu-west-1.compute.amazonaws.com:8890 

You will see Zeppelin Interactive data analytics web-site of your cluster:

![Zeppelin](https://zeppelin.apache.org/docs/0.7.0/assets/themes/zeppelin/img/notebook.png)



# Extras

## Using Python without pyspark:

Install on Cluster:

```
sudo pip install py4j
``` 

Access to python (not pyspark):

```
python 
```

Create this function:

```
def configure_spark(spark_home=None, pyspark_python=None):
	import os, sys
	spark_home = spark_home or "/usr/lib/spark/"
	os.environ['SPARK_HOME'] = spark_home
	# Add the PySpark directories to the Python path:
	sys.path.insert(1, os.path.join(spark_home, 'python'))
	sys.path.insert(1, os.path.join(spark_home, 'python', 'pyspark'))
	sys.path.insert(1, os.path.join(spark_home, 'python', 'build'))
	# If PySpark isn't specified, use currently running Python binary:
	pyspark_python = pyspark_python or sys.executable
	os.environ['PYSPARK_PYTHON'] = pyspark_python

```

And now, we can use python and spark:

```
configure_spark("/usr/lib/spark/")

from pyspark import SparkContext
...

```




