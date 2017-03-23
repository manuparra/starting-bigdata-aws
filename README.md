




### Creating a Key pairs


Set ``400`` permissions mask to PEM file (to avoid this problem connecting with ssh: [PEM Error](#errors/errors.md#UNPROTECTED PRIVATE KEY FILE))

```
chmod 400 /home/manuparra/.ssh/PredictivaIO.pem
```


Creating a simple Spark Cluster with the next features:

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






### Override Cluster Software configuration

You can override the default configurations for applications you install by supplying a configuration object when specifying applications you want installed at cluster creation time.




