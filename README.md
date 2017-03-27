


# Setting up AWS 

## Creating IAM credencial required with AWS CLI

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources for your users. You use IAM to control who can use your AWS resources (authentication) and what resources they can use and in what ways (authorization).

- Go to [IAM](https://console.aws.amazon.com/iam/).
- Click on the left Add user.
- Write User name
- In Access Type check: ``Programmatic access``. It enables an access key ID and secret access key for the AWS API, CLI, SDK, and other development tools.
- In Permissions add AdministratorAccess Policy (if this user will be administrator).
- Add to Group of AdministratorAccess



## Installing AWS CLI

The AWS Command Line Interface (CLI) is a unified tool to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.

*Windows*

Download and run the [64-bit](https://s3.amazonaws.com/aws-cli/AWSCLI64.msi)  Windows installer.

*Mac and Linux*

Requires Python 2.6.5 or higher. Install using pip:

```
sudo pip install awscli
```


Use AWS Access Key ID from Security Credentials Tab of the user and the same to AWS Secret Access Key. If you want to generate a new Access key, you will get a new pair of Access Key ID and Secret Access Key.

Check your REGION NAME [here](http://docs.aws.amazon.com/general/latest/gr/rande.html).

After install, configure AWS CLI:

```
$ aws configure
AWS Access Key ID [None]: XXXXXXXXXXXX
AWS Secret Access Key [None]: YYYYYYYYYYYYY
Default region name [None]: eu-west-1
Default output format [None]:  
```

### Check if AWS CLI is working

Try:

```
aws s3 ls
```

If it returns without error, AWS CLI is working fine.



## Creating a Key pairs

Amazon EC2/EMR (and all products) uses public–key cryptography to encrypt and decrypt login information. Public–key cryptography uses a public key to encrypt a piece of data, such as a password, then the recipient uses the private key to decrypt the data. The public and private keys are known as a key pair.

To log in our Cluster or Instance, we must create a key pair, specify the name of the key pair when you launch the instance, and provide the private key when you connect to the instance. Linux instances have no password, and you use a key pair to log in using SSH.

To create a key pair: 

- Go to [EC2 dashboard](https://eu-west-1.console.aws.amazon.com/ec2/) and click "Create Key Pair".

After this, PEM file will be downloaded, please store this file in a safe location in your computer.


Set ``400`` permissions mask to PEM file (to avoid this problem connecting with ssh: [PEM Error](#errors/errors.md#UNPROTECTED PRIVATE KEY FILE)).

```
chmod 400 /home/manuparra/.ssh/PredictivaIO.pem
```


# Creating a simple Spark Cluster

Creating a Spark Cluster with the next features:

- **emr**: 5.4.0 see [releases](http://docs.aws.amazon.com//emr/latest/ReleaseGuide/images/emr-5.4.0.png).
- **KeyName**: Name of the Key Pair generated from EC2/KeyPairs  (not the ``.pem`` file).
- **Name**: Name of the software-sandbox. Here you can add more software bundles.
- **m3.xlarge**: Flavour of the instances. [Types](https://aws.amazon.com/es/ec2/instance-types/).
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

To check the status of the created cluster:

```
aws emr list-clusters
```

To check the status of active/terminated or failed Clusters (``[--active | --terminated | --failed]``)

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


## Connecting with SSH


Try the next. If the command cannot connnect, check Security group and add a RULE for SSH :

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

And now you are in the Master Node of your cluster.




# Starting interactive BigData Analytics

Spark supports Scala, Python and R. We can choose to write them as standalone Spark applications, or within an interactive interpreter.

Once logged in you can use three possible interactive development environments that brings the cluster (by default):

## Python

We can use pyspark interactive shell:

```
[hadoop@ip-[redacted] ~]$ pyspark
```

Working with this sample:

```

lines=sc.textFile("s3n://datasets-preditiva/500000_ECBDL14_10tst.data")

print lines.count()

print lines.take(10)

lines.saveAsTextFile("s3n://datasets-preditiva/results/10_ECBDL14_10tst.data")

#from pyspark.sql import Row
#parts = lines.map(lambda l: l.split(","))
#table = parts.map(lambda p: (p[0], p[1] , p[2] , p[3] , p[4] , p[5] , p[6] ))
#schemaTable = spark.createDataFrame(table)
#schemaTable.createOrReplaceTempView("mytable")

#print schemaTable.printSchema()

```



Press ``CRTL+D`` to exit or write ``exit``.

## Scala

```
[hadoop@ip-[redacted] ~]$ spark-shell
```

Working with this sample:

```
val x = sc.textFile("s3n://datasets-preditiva/500000_ECBDL14_10tst.data")
x.take(5)
x.saveAsTextFile("s3n://datasets-preditiva/results/10_ECBDL14_10tst.data")

```

Press ``CRTL+D`` to exit or write ``exit``.

## R

```
[hadoop@ip-[redacted] ~]$ sparkR
```

Working with this sample:

```
data <- textFile(sc, "s3n://datasets-preditiva/500000_ECBDL14_10tst.data")

brief <- take(data,10)

saveAsTextFile(brief,"s3n://datasets-preditiva/results/10_ECBDL14_10tst.data")


```

Press ``CRTL+D`` to exit or write ``exit``.

## Operations on EMR Spark Cluster 

### Terminating the Spark Cluster

Use AWS CLI:

```
aws emr terminate-clusters --cluster-id j-26H8B5P1XGYM0
````

You can check if the Cluster is terminated:

```
aws emr list-clusters --terminated
```


### Adding applications in cluster creation time

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


### Change Cluster Software configuration

You can override the default configurations for applications you install by supplying a configuration object when specifying applications you want installed at cluster creation time.

#### Creating Cluster and add support with Zeppelin interactive analytics 

Sometimes software installed on the cluster probably use a port to comunicate with it.

To add support to aditional software and show the software on external port, we need to create a RULE on Security group. 

Security group acts as a virtual firewall that controls the traffic for one or more instances. When you launch an instance, you associate one or more security groups with the instance. You add rules to each security group that allow traffic to or from its associated instances. You can modify the rules for a security group at any time; the new rules are automatically applied to all instances that are associated with the security group. When we decide whether to allow traffic to reach an instance, we evaluate all the rules from all the security groups that are associated with the instance.

To create or to add a new rule, go to [Security Groups](https://eu-west-1.console.aws.amazon.com/ec2/v2/home?region=eu-west-1#SecurityGroups:sort=groupId) in the menu EC2 (choose SecurityGroups) and 
select:

- ElasticMapReduce-master ... (Master group for Elastic MapReduce created on ....) and Edit Rules on INBOUND :
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



# Submitting BigData applications to the cluster

This section describes the methods for submitting work to an AWS EMR cluster. You can submit work to a cluster by adding steps or by interactively submitting Hadoop jobs to the master node. The maximum number of PENDING and ACTIVE steps allowed in a cluster is 256. You can submit jobs interactively to the master node even if you have 256 active steps running on the cluster. You can submit an unlimited number of steps over the lifetime of a long-running cluster, but only 256 steps can be ACTIVE or PENDING at any given time.

## Executing algorithms with spark-submit

The spark-submit script in Spark’s bin directory is used to launch applications on a cluster. It can use all of Spark’s supported cluster managers through a uniform interface so you don’t have to configure your application specially for each one.

### Application in Python


Connect to your created Cluster via SSH and save the following code in your Cluster home with the name ``wordcount.py``:

```
from __future__ import print_function
from pyspark import SparkContext

import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: wordcount  ", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="WordCount")
    text_file = sc.textFile(sys.argv[1])

    counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    
    counts.saveAsTextFile(sys.argv[2])
    
    sc.stop()
```

Now execute this command:

```
spark-submit --deploy-mode cluster  --master yarn  --num-executors 5  --executor-cores 5  --executor-memory 4g  --conf spark.yarn.submit.waitAppCompletion=false wordcount.py s3://datasets-preditiva/inputtext.txt s3://datasets-preditiva/results-wordcount/
```

Check Memory configuration [here](http://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-hadoop-task-config.html).

Note that the property ``spark.yarn.submit.waitAppCompletion`` with the step definitions. When this property is set to false, the client submits the application and exits, not waiting for the application to complete. This setting allows you to submit multiple applications to be executed simultaneously by the cluster and is only available in cluster mode.


## Executing algorithms with AWS EMR Steps

### Application in Python


Now execute this command:

```
aws emr add-steps --cluster-id j-2L74YHK3V8BCP --steps Type=spark,Name=SparkWordCountApp,Args=[--deploy-mode,cluster,--master,yarn,--conf,spark.yarn.submit.waitAppCompletion=false,--num-executors,5,--executor-cores,5,--executor-memory,8g,s3://code-predictiva/wordcount.py,s3://datasets-preditiva/inputtext.txt,s3://datasets-preditiva/resultswordcount/],ActionOnFailure=CONTINUE
```

### List steps

Provides a list of steps for the cluster in reverse order unless you specify stepIds with the request.
```
aws emr list-steps --cluster-id j-2L74YHK3V8BCP
```



### Cancel steps

You can cancel steps using the the AWS Management Console, the AWS CLI, or the Amazon EMR API. Only steps that are PENDING can be canceled.

```
aws emr cancel-steps --cluster-id j-XXXXXXXXXXXXX --step-ids s-YYYYYYYYYY
```



# Starting with Datasets and SparkDataFrames

A Dataset is a distributed collection of data. Dataset is a new interface added in Spark 1.6 that provides the benefits of RDDs (strong typing, ability to use powerful lambda functions) with the benefits of Spark SQL’s optimized execution engine. A Dataset can be constructed from JVM objects and then manipulated using functional transformations (map, flatMap, filter, etc.). The Dataset API is available in Scala and Java. Python does not have the support for the Dataset API. But due to Python’s dynamic nature, many of the benefits of the Dataset API are already available (i.e. you can access the field of a row by name naturally row.columnName). The case for R is similar.

A DataFrame is a Dataset organized into named columns. It is conceptually equivalent to a table in a relational database or a data frame in R/Python, but with richer optimizations under the hood. DataFrames can be constructed from a wide array of sources such as: structured data files, tables in Hive, external databases, or existing RDDs. The DataFrame API is available in Scala, Java, Python, and R. In Scala and Java, a DataFrame is represented by a Dataset of Rows. In the Scala API, DataFrame is simply a type alias of Dataset[Row]. While, in Java API, users need to use Dataset<Row> to represent a DataFrame.


![RDDsDataframes](http://www.datascienceassn.org/sites/default/files/users/user34/SparkDatasets.png)

## Reading and writing data from/to distinct sources

![Sources](https://camo.githubusercontent.com/d3121ca676fe0828f519e85b1f8724e18ba0c2b9/68747470733a2f2f73697465732e676f6f676c652e636f6d2f736974652f6d616e7570617272612f686f6d652f66696c65735f4150492e706e67)



*Python:*

```
....

df = spark.read.csv("s3://datasets-preditiva/500000_ECBDL14_10tst.data",header=True, mode="DROPMALFORMED", schema=schema)

df.show()

df.write.save("s3://datasets-preditiva/results-simple/500000_ECBDL14_10tst.data", format="parquet")
```

*R*:

```
df <- read.df("s3://datasets-preditiva/500000_ECBDL14_10tst.data","csv",header = "true", inferSchema = "true");

head(df);

f1andf2 <- select(df, "f1", "f2");

f1andClass <- select(df, "f1", "Class");

write.df(f1andf2, "s3://datasets-preditiva/results-columns-class/", "csv");
write.df(f1andClass, "s3://datasets-preditiva/results-columns-class/", "csv");

```

## Querying with SPARKSQL

Spark SQL supports operating on a variety of data sources through the DataFrame interface. A DataFrame can be operated on using relational transformations and can also be used to create a temporary view. Registering a DataFrame as a temporary view allows you to run SQL queries over its data. This section describes the general methods for loading and saving data using the Spark Data Sources and then goes into specific options that are available for the built-in data sources.

Use ``createOrReplaceTempView``

### Starting with Queries

*Python*:

```
...
df = spark.read.csv("s3://datasets-preditiva/500000_ECBDL14_10tst.data")

df.createOrReplaceTempView("tableSQL")

resultDF = spark.sql("SELECT COUNT(*) from tableSQL")
...

```


*R*:

```
...
df = read.df("s3://datasets-preditiva/500000_ECBDL14_10tst.data","csv",header = "true", inferSchema = "true")

createOrReplaceTempView(df,"tableSQL")

resultDF <- sql("SELECT COUNT(*) from tableSQL")

head(resultDF)
...

```

### More with SparkSQL

#### Selecting 

Python: 

```
# Selecting two columns

df = spark.read.csv("s3://datasets-preditiva/500000_ECBDL14_10tst.data")

df.createOrReplaceTempView("tableSQL")

df.show()

resultDF = spark.sql("SELECT f1, class from tableSQL")
```

R:

```
# Selecting two columns

df = read.df("s3://datasets-preditiva/500000_ECBDL14_10tst.data","csv",header = "true", inferSchema = "true")

createOrReplaceTempView(df,"tableSQL")

resultDF <- sql("SELECT f1,class from tableSQL")
```

#### Filtering

Python: 

```
# Selecting two columns and filtering with condition

df = spark.read.csv("s3://datasets-preditiva/500000_ECBDL14_10tst.data")

df.createOrReplaceTempView("tableSQL")

df.show()

resultDF = spark.sql("SELECT f1, class from tableSQL where class='1'")
```

R:

```
# Selecting two columns and filtering with condition

df = read.df("s3://datasets-preditiva/500000_ECBDL14_10tst.data","csv",header = "true", inferSchema = "true")

createOrReplaceTempView(df,"tableSQL")

resultDF <- sql("SELECT f1, class from tableSQL where class='1'")
```

Python: 

```
# Selecting  columns and filtering with multiple conditions

df = spark.read.csv("s3://datasets-preditiva/500000_ECBDL14_10tst.data")

df.createOrReplaceTempView("tableSQL")

df.show()

resultDF = spark.sql("SELECT f1, class from tableSQL where class='1' and f1>0.5 ")

```

R:

```
# Selecting  columns and filtering with multiple conditions

df = read.df("s3://datasets-preditiva/500000_ECBDL14_10tst.data","csv",header = "true", inferSchema = "true")

createOrReplaceTempView(df,"tableSQL")

resultDF <- sql("SELECT f1, class from tableSQL where class='1' and f1>0.5")
```

#### Grouping

Python:

```
df = spark.read.csv("s3://datasets-preditiva/500000_ECBDL14_10tst.data")

df.createOrReplaceTempView("tableSQL")

resultDF = spark.sql("SELECT count(*),class from tableSQL group by class")
```

R:

```
# Count the number of elements of the class

df = read.df("s3://datasets-preditiva/500000_ECBDL14_10tst.data","csv",header = "true", inferSchema = "true")

createOrReplaceTempView(df,"tableSQL")

resultDF <- sql("SELECT count(*),class from tableSQL group by class")
```


#### Aggregating 

Python:

```
df = spark.read.csv("s3://datasets-preditiva/500000_ECBDL14_10tst.data")

df.createOrReplaceTempView("tableSQL")

resultDF = spark.sql("SELECT SUM(f1),AVG(f3),class from tableSQL group by class")

resultDF.show()
```

R:

```
# Count the number of elements of the class

df = read.df("s3://datasets-preditiva/500000_ECBDL14_10tst.data","csv",header = "true", inferSchema = "true")

createOrReplaceTempView(df,"tableSQL")

resultDF <- sql("SELECT SUM(f1),AVG(f3),class from tableSQL group by class")
```






# BigData development environment with Spark and Hadoop

Download the virtual machine with the development environment [here](https://drive.google.com/file/d/0ByPBMv-S_GMEakRCVVRTejZKVm8/view?usp=sharing). (approx: 4 GB)

Credentials to the Virtual Machine are:

- User: root
- Key: sparkR

## Requirements of the Virtual Machine:

- VIRTUALBOX installed, available at: https://www.virtualbox.org/wiki/Downloads 
- At least 2GB of RAM for the Virtual Machine (datasets must be less than 2GB).
- PC must be 64bit and at least 4GB of RAM (2GB for MVirtual and another 2GB for PC)
- Compatible with Windows, Mac OSX and Linux

## Connecting to the development environment from outside of the VM

Virtual Machine exposes a few ports:

- shh on 22000 
- Jupyter notebooks on 25980  (for Spark Python development).
- RStudio on 8787 (for SparkR develpment)


Connecting with SSH:

```
ssh -p 22000 root@localhost
```

Connecting  with Jupyter Notebooks : 

```
http://localhost:25980
```

![imgJupyter](https://camo.githubusercontent.com/db9d5bc4e6f3b153f5bf921f90db7c237a212cf0/68747470733a2f2f73697465732e676f6f676c652e636f6d2f736974652f6d616e7570617272612f686f6d652f6a7570797465722e6a7067)

Connecting with RStudio: 

```
http://localhost:8787
```

![imgRstudio](https://camo.githubusercontent.com/3d08b1352af5f25687fb934ff0a485e00b85f465/68747470733a2f2f73697465732e676f6f676c652e636f6d2f736974652f6d616e7570617272612f686f6d652f7273747564696f2e6a7067)



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


