This lab will cover the following two topics:

1. Dynamic contextualization and model serving in a scalable production environment 
3. Reliable continuous integration and development process

--------------------

Important:

0. _It is expected that students have finished the prelab of the distributed e-infrastructures part._

1. _NOTE: Please terminate VMs once you finish the task._ 

2. The tasks and the configurations are designed for the Ubuntu 18.04 with medium VM flavour.  

3. We will use SNIC Science Cloud (SSC) for all the tasks. In case you want to learn more about SSC visit the website  http://cloud.snic.se

4. We recommend you to create a VM in SSC and execute all the tasks on that virtual machine. You can run the tasks on your laptops but it may break your local working environment.

3. For all the tasks clone the repository:

https://github.com/SNICScienceCloud/technical-training.git

The code for all the tasks is available in the "model-serving" directory. 

```
 - model-serving
   -- Single_server_without_docker
   -- Single_server_with_docker
   -- CI_CD
   -- OpenStack-Client
```
------------------------

# Dynamic contextualization

Dynamic contextualization is a process of preparing a customized computing environment at runtime. The process ranging from creating/defining user roles and permissions to updating/installing different packages and initiating services. 

## Task-1: Single server deployment 

In this task, we will learn how the dynamic contextualization works using Cloudinit package. For this task, we need to use OpenStack APIs to start a VM and contextualize it at run time. The contextualization process will setup the following working environment: 


1. Flask web application as a frontend server 
2. Celery and RabbitMQ server for backend server
3. Model execution environment based on Keras and TensorFlow

In case you are not familiar with the above-mentioned packages please read the following links: 

1. Flask Application -> https://flask.palletsprojects.com/en/1.1.x/
2. Celery and RabbitMQ -> https://docs.celeryproject.org/en/stable/getting-started/
3. Keras and TensorFlow -> https://www.tensorflow.org/guide/keras
4. OpenStack -> https://www.openstack.org/

The execution process will start when a client will send a prediction request from the front-end web server. The server will pass the request to the backend Celery environment where running workers in the setup will pick up the task, run the predictions by loading the available model, send back the results and finally frontend server will display the results.

### Steps for the contextualization

0. Start a VM from the SSC dashboard and login to the client VM.

```console 
ssh -i PATH-TO-PRIVATE-KEY ubuntu@<CLIENT-VM-FLOATING-IP>
```

1. Clone the git repository.

```console
git clone https://github.com/SNICScienceCloud/technical-training.git
```

2. Goto the `technical-training/model-serving/single_server_without_docker/production_server/` directory. This directory contains the code that will run on the  production server VM.
 
Following is the structure of the code: 

``` 
 - Flask Application based frontend 
    -- app.py
    -- static
    -- templates
 - Celery and RabbitMQ setup
    -- run_task.py
    -- workerA.py
 - Machine learning Model and Data 
    -- model.h5
    -- model.json
    -- pima-indians-diabetes.csv
```

Open files and try to understand the application's structure. 

3. Goto the `technical-training/model-serving/openstack-client/single_node_without_docker_client/` directory. This is the code that we will contextualize our production server. The code is based on the following two files:

```console
- CloudInit configuration file  
  -- cloud-cfg.txt
- OpenStack python code
  -- start_instance.py
```

Open the files and try to understand the steps. _NOTE: You need to setup variable values in the start_instance.py script._ 

-------------

In order to run this code, you need to have OpenStack API environment running. 

_NOTE: Openstack APIs are only need to be installed on the client VM._ 

Follow the instructions available on the following links: 

- Goto https://docs.openstack.org/install-guide/environment-packages-ubuntu.html , http://docs.openstack.org/cli-reference/common/cli_install_openstack_command_line_clients.html and download the client tools and API for OpenStack.

- Download the Runtime Configuration (RC) file from the SSC site (Project->Compute->Access & Security->API Access->Download OpenStack RC File).

- Confirm that your RC file have following enviroment variables:

```console
export OS_USER_DOMAIN_NAME="snic"
export OS_IDENTITY_API_VERSION="3"
export OS_PROJECT_DOMAIN_NAME="snic"
export OS_PROJECT_NAME="SNIC 2020/20-25"
```

- Set the environment variables by sourcing the RC-file:

```console 
source <project_name>_openrc.sh
```

- The successful execution of the following commands will confirm that you have the correct packages available on your VM:

```console
openstack server list
```

```console
openstack image list
```

- For the API communication we need following extra packages:

```console
apt install python3-openstackclient
apt install python3-novaclient
apt install python3-keystoneclient
```

------------------

4. Once you have setup the environment, run the following command. 

```console 
python3 start_instance.py
```

The command will start a new server and initiate the contextualization process. It will take approximately 10 to 15 minutes. The progress can be seen on the cloud dashboard. Once the process finish, attach a floating IP to your production server and access the webpage from your client machine. 

- Welcome page `http://<PRODUCTION-SERVER-IP>:5100`
- Predictions page `http://<PRODUCTION-SERVER-IP>:5100/predictions`

## Questions

1. Explain how the application works? Write one paragraph about application's framework. 

2. What are the drawbacks of the contextualization strategy adopted in the task-1? Write at least four drawbacks.

3. Currently, the contextualization process takes 10 to 15 minutes. How can we reduce the deployment time?   

-----------------------------

TERMINATE THE SERVER VM STARTED FOR TASK-1!

-----------------------------

## Task-2: Single server deployment with Docker Containers

In this task, we will repeat the same deployment process but with Docker containers. This time we  will create a flexible containerized deployment environment where each container has a defined role. 

1. Now goto `technical-training/model-serving/single_server_with_docker/production_server/` directory on the client VM. The directory contains the code that will run on your production server. Following is the structure of the code: 

``` 
 - Flask Application based frontend 
    -- app.py
    -- static
    -- templates
 - Celery and RabbitMQ setup
    -- run_task.py
    -- workerA.py
 - Machine learning Model and Data 
    -- model.h5
    -- model.json
    -- pima-indians-diabetes.csv
 - Docker files
    -- Dockerfile
    -- docker-compose.yml
```

Open different files and try to understand the application's structure. 

2. Goto the `technical-training/model-serving/openstack-client/single_node_with_docker_client/` directory. This is the code that we will run to contextualize the production server. The code is based on the following two files:

```console
- CloudInit configuration file  
  -- cloud-cfg.txt
- OpenStack python code
  -- start_instance.py
```

Open the files and try to understand the steps. _NOTE: You need to setup variable values in the start_instance.py script._ 

3. Run the following command. 

```console 
python3 start_instance.py
```

The command will start a new server and initiate the contextualization process. It will take approximately 10 to 15 minutes. The progress can be seen on the cloud dashboard. Once the process finish, attach a floating IP to your production server and access the webpage from your client machine. 

Welcome page `http://<PRODUCTION-SERVER-IP>:5100`. Predictions page `http://<PRODUCTION-SERVER-IP>:5100/predictions`

4. The next step is to test the horizontal scalability of the setup. 

- Login to the production server. 

```console 
ssh -i ubuntu@<PRODUCTION-SERVER-IP>
```

- Switch to the superuser mode.
   
```console
sudo bash
```

- Check the cluster status:

```console 
cd /technical-training/model-serving/single_server_with_docker/production_server
```

```console
docker-compose ps
```

The output will be as following:

```console
   Name                          Command               State                                             Ports                                           
------------------------------------------------------------------------------------------------------------------------------------------------------------------
production_server_rabbit_1     docker-entrypoint.sh rabbi ...   Up      15671/tcp, 0.0.0.0:15672->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp
production_server_web_1        python ./app.py --host=0.0.0.0   Up      0.0.0.0:5100->5100/tcp
production_server_worker_1_1   celery -A workerA worker - ...   Up  
```

Following three containers are running on the production server: 

```
production_server_rabbit_1  -> RabbitMQ server
production_server_web_1 -> Flask based web application
production_server_worker_1_1 -> Celery worker 
```

Now we will add multiple workers in the cluster using docker commands. 

- Currently, there is one worker available. We will add two more workers. 

```console 
docker-compose up --scale worker_1=3 -d
```

- Check the cluster status.

```console
docker-compose ps
```

Output will be:

```console
            Name                          Command               State                                             Ports                                           
------------------------------------------------------------------------------------------------------------------------------------------------------------------
production_server_rabbit_1     docker-entrypoint.sh rabbi ...   Up      15671/tcp, 0.0.0.0:15672->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp
production_server_web_1        python ./app.py --host=0.0.0.0   Up      0.0.0.0:5100->5100/tcp
production_server_worker_1_1   celery -A workerA worker - ...   Up
production_server_worker_1_2   celery -A workerA worker - ...   Up                                                             
production_server_worker_1_3   celery -A workerA worker - ...   Up
```

Now we have 3 workers running in the system. 

- Now scale down the cluster.

```console 
docker-compose up --scale worker_1=1 -d
```

## Questions

1. What problems Task-2 deployment strategy solves compared to the strategy adopted in Task-1? 

2. What are the outstanding issues that the deployment strategy of Task-2 cannot not address? What are the possible solutions to address those outstanding issues? 

3. What is the difference between horizontal and vertical scalability? The strategy discussed in Task-2, is it horizontal or vertical scalability? 

-----------------------------

TERMINATE THE SERVER VM STARTED FOR TASK-2!

-----------------------------

# Continuous Integration and Continuous Delivery (CI/CD)

I 

## Task-3: Deployment of multiple servers using Ansible

For this task we need three VMs

1. Client VM: This machine will serve as an Ansible host name and initiate the configuration process. 

2. Production Server: The machine will host the dockerised version of the application discussed in previous tasks (1 and 2).

3. Development Server: The machine will host the development environment and push the new changes to the production server. 

### Steps to setup Ansible host and orchestration environment

1. Login to the Client machine

```console 
ssh -i ubuntu@<PRODUCTION-SERVER-IP>
```

2. Goto `technical-training/model-serving/ci_cd` directory. This directory contains the following two sub-directories 

```
/production_server 
 - Flask Application based frontend 
    -- app.py
    -- static
    -- templates
 - Celery and RabbitMQ setup
    -- run_task.py
    -- workerA.py
 - Machine learning Model and Data 
    -- model.h5
    -- model.json
    -- pima-indians-diabetes.csv
/development_server
 - Machine learning Model and Data 
    -- model.h5
    -- model.json
    -- pima-indians-diabetes.csv
    -- neural_net.py
  
```

Open different files and try to understand the application's structure. 

3. Goto the `technical-training/model-serving/openstack-client/single_node_with_docker_ansible_client` directory. This is the code that we will run to contextualize our production server. The code is based on the following files:

```console
- CloudInit files 
  -- prod-cloud-cfg.txt
  -- dev-cloud-cfg.txt
- OpenStack code  
  -- start_instance.py
- Ansible files
  -- setup_var.yml
  -- configuration.yml  
```

The client code will start two VMs and uisng Ansible orchestration environment it will contextualize both of the VMs simultanously. 

4. Installation and configuration of Ansible on the client machine.

- First will generate a cluster SSH key.

First check the username you are login as 

```console
whoami
```

Output

```console
ubuntu
```

You need to be as _ubuntu_ user. If you are _root_ user switch back to _ubuntu_ user. 

Create a directory 

```console
mkdir -p /home/ubuntu/cluster-keys

```

```console
ssh-keygen -t rsa
```

Output

```console
Generating public/private rsa key pair.
Enter file in which to save the key (/home/ubuntu/.ssh/id_rsa): /home/ubuntu/cluster-keys/cluster-key
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/ubuntu/cluster-keys/cluster-key.
Your public key has been saved in /home/ubuntu/cluster-keys/cluster-key.pub.
The key fingerprint is:
4a:dd:0a:c6:35:4e:3f:ed:27:38:8c:74:44:4d:93:67 demo@a
The key's randomart image is:
+--[ RSA 2048]----+
|          .oo.   |
|         .  o.E  |
|        + .  o   |
|     . = = .     |
|      = S = .    |
|     o + = +     |
|      . o + o .  |
|           . o   |
|                 |
+-----------------+
```

Now we have cluster ssh keys at the following location:

1. Private key: `/home/ubuntu/cluster-keys/cluster-key`

2. Public key: `/home/ubuntu/cluster-keys/cluster-key.pub`

3. Now we start Production and Development servers. But first open `prod-cloud-cfg.txt` delete the old key from the section `ssh_authorized_keys:` and copy the complete contents of `/home/ubuntu/cluster-keys/cluster-key.pub` in the section `ssh_authorized_keys:` 

Repeat same step 3 with the `dev-cloud-cfg.txt`. Delete the old key from the section `ssh_authorized_keys:` and copy the complete contents of `/home/ubuntu/cluster-keys/cluster-key.pub` in the section `ssh_authorized_keys:`

4. Run the `start_instance.py` code.

```console
python3 start_instance.py
```

The output will give you the internal IPs of the VMs. 

```console
user authorization completed.
Creating instances ... 
waiting for 10 seconds.. 
Instance: prod_server_with_docker_6225 is in BUILD state, sleeping for 5 seconds more...
Instance: dev_server_6225 is in BUILD state, sleeping for 5 seconds more...
Instance: prod_server_with_docker_6225 is in ACTIVE state, sleeping for 5 seconds more...
Instance: dev_server_6225 is in BUILD state, sleeping for 5 seconds more...
Instance: __prod_server_with_docker_6225__ is in ACTIVE state ip address: __192.168.1.19__
Instance: __dev_server_6225__ is in ACTIVE state ip address: __192.168.1.17__
```
Now we have two VM running with the internal IP addresses.

5. Install Ansible packages on the client machine. 

```console
sudo bash
```

```console
apt-add-repository ppa:ansible/ansible
```
```console
apt update
```
```console
apt install ansible
```
We have ansible packages install. Now we will enter these IP addresses in the Ansible hosts file.

i. prod_server_with_docker_6225  -> 192.168.1.19

ii. dev_server_6225 -> 192.168.1.17

6. Open the Ansible inventory file and add the IP address in that file. For this step you need to swtich to _root_ user.

```console
sudo bash
```

```console
nano  /etc/ansible/hosts
```

file contents

```console
[servers]
prod_server ansible_host=<production server IP address>
dev_server ansible_host=<development server IP address>

[all:vars]
ansible_python_interpreter=/usr/bin/python3

[prod_server]
prod_server ansible_connection=ssh ansible_user=appuser

[dev_server]
dev_server ansible_connection=ssh ansible_user=appuser
```

If you need to learn more about Ansible, here are some useful links: 

Ansible official site 
https://www.ansible.com/

Easy installation instructions
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-18-04

- Just to confirm the access premission are correctly set, access production and development server from the client VM. 

First switch back to user _ubuntu_

```console
ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@<PRODUCTION-SERVER-IP>
```

If the login is successfull, exit from the production server and repeat the step with development server 

```console
ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@<DEVELOPMENT-SERVER-IP>
```
If the login successfull, exit from the development server. 

- For this step you need to be login as _ubuntu_ user on the client VM. 

Now we will run the Ansible script available in the `technical-training/model-serving/openstack-client/single_node_with_docker_ansible_client` directory. 

```console
export ANSIBLE_HOST_KEY_CHECKING=False
```

```console
ansible-playbook configuration.yml --private-key=/home/ubuntu/cluster-keys/cluster-key
```

The process will take 10 to 15 minutes to complete. Once the process successfully completed you have both production and development servers ready. 

Attach floating IP address to the production server and access the same web page as we have in previous tasks.  

## Questions

1 - What is the difference between CloudInit and Ansible? 

2 - Explain the configurations available in `dev-cloud-cfg.txt` and `prod-cloud-cfg.txt` files.

3 - What problem we have solved by using Ansible?

---------------------------------

The Task-4 is the continuation of Task-3. Do NOT terminate your instances setup in Task-3. 

---------------------------------

## Task-4: CI/CD using Git HOOKS 

This 

0. SSH key based communication between production and development servers 

- Login to development server 
    
  ```console
  ssh -i cluster-key appuser@<DEVELOPMENT-SERVER-IP>
  ```
    
- Generate SSH key 
    
  ```console
  ssh-keygen
  ```

_NOTE: This step will create two files, private key `/home/appuser/.ssh/id_rsa` and public key `/home/appuser/.ssh/id_rsa.pub`._

- copy the contents of public key file `/home/appuser/.ssh/id_rsa.pub` from the development server.

- Login to production server
    
```console
ssh -i cluster-key appuser@<PRODUCTION-SERVER-IP>
```

- Open file `/home/appuser/.ssh/authorized_keys` and past the contents of the public key files. 

```console
nano /home/appuser/.ssh/authorized_keys
``` 

1. Login to the Production Server 

```console
ssh -i cluster-key appuser@<PRODUCTION-SERVER-IP> 
```
   
- Create a directory (it will be jump directory)
   
```console
pwd 
```

Output

```console
/home/appuser/
```

```console
mkdir my_project
```

```console
cd my_project
``` 

- Here is the path to your jump directory. Double check that user `appuser` is the owner of `my_project` directory. 
   
```console
pwd
/home/appuser/my_project       
```
   
- Create git empty directory 
   
```console
git init --bare
```
   
Initialized empty Git repository in `/home/appuser/my_project/`

- Create a git hook `post-receive`
 
```console
nano hooks/post-receive
```
File contents  

```console
#!/bin/bash
while read oldrev newrev ref
do
    if [[ $ref =~ .*/master$ ]];
    then
        echo "Master ref received.  Deploying master branch to production..."
        git --work-tree=/technical-training/model-serving/ci_cd/production_server --git-dir=/home/appuser/my_project checkout -f
    else
        echo "Ref $ref successfully received.  Doing nothing: only the master branch may be deployed on this server."
    fi
done
```

- Change permissions
 
```console
chmod +x hooks/post-receive
```
  
- Exit Production Server

2. login to the Development Server

```console
ssh -i cluster-key appuser@<DEVELOPMENT-SERVER-IP>
```
   
- Create a directory

```console
pwd
/home/appuser/
```

```console
mkdir my_project
```

```console
cd my_project
```

- This is your development directory. Double check that user `appuser` is the owner of `my_project` directory.

```console
pwd
/home/appuser/my_project 
```
   
- Create empty git repository

```console
git init
```

Output

```console
 Initialized empty Git repository in `/home/appuser/project/.git/`
```

- Add files `model.h5` and  `model.json` in `/home/appuser/project/` directory. The files are available in `/technical-training/model-serving/ci_cd/development_server/` directory. 

- Goto `/home/appuser/project` directory
    
- Add files for the commit 
   
```console
git add .
```
  
- Commit files
 
```console
git commit -m "new model" 
```
   
- connect development server's git to production server's git. 

```console
git remote add production appuser@<PRODUCTIONS-SERVER-IP>:/home/appuser/my_project
```
   
- Push your commits to the production server
   
```console
git push production master
```
Output

```console
Delta compression using up to 2 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 2.36 KiB | 2.36 MiB/s, done.
Total 4 (delta 0), reused 0 (delta 0)
remote: Master ref received.  Deploying master branch to production...
To 192.168.1.21:/home/appuser/my_project
* [new branch]      master -> master 
```

For further details visit following link: 
https://www.digitalocean.com/community/tutorials/how-to-use-git-hooks-to-automate-development-and-deployment-tasks

3. Goto `/technical-training/model-serving/ci_cd/development_server/` directory. The directory contains the `neural_net.py` python script. The script will train a model and generate new model files `model.h5` and  `model.json`. Now we will make changes in the model files, move them in the git repository, make a commit and than push these new model files in the running  production pipeline. 

- Run the script 
 
 ```console
   python3 neural_net.py 
   ```
- Copy model files (`model.h5` and  `model.json`) from the development directory `technical-training/model-serving/ci_cd/development_server/` to the git repository `/home/appuser/project` on the development server.    
   
```console
   cp /technical-training/model-serving/ci_cd/development_server/model*  /home/appuser/project/.
   ```   
- Add to the git repository. 
 
 ```console
 git add . 
 ```
 
- Finally, commit and push the new model files. 
 
 ```console
git commit -m "new model" 
```

```console
git push production master
```
Output

```console
Delta compression using up to 2 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 2.36 KiB | 2.36 MiB/s, done.
Total 4 (delta 0), reused 0 (delta 0)
remote: Master ref received.  Deploying master branch to production...
To 192.168.1.21:/home/appuser/my_project
* [new branch]      master -> master 
```

- Access the url `http://<PRODUCTION-SERVER-IP>:5100/predictions` and you will see the changes in predictions.

4. Improve the model by changing parameters or network architecture in the `neural_net.py` file and repeat the step-3 to push the new model to the production pipeline. 

## Questions

1 - What are git hooks? Explain the `post-receive` script available in this task. 

2 - We have created a empty git repository on the production server. Why we need that directory? 

3 - Write the names of four different git hooks and explain their functionalities. 
Hints - Read the link available in the task or access sample scripts available in the `.hooks` directory. 
