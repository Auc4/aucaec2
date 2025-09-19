
# Sebastián Aucapiña Workshop

# Tools used for the workshop
For developing the basic API different tools and platforms are necessary to get access to the data via internet.

**Tools:**
- Python 3.12
- Node JS
- SSH client (any, but this guide uses ssh terminal emulator clients)
- Linux or Windows Subsytem for Linux (WSL)

**Platforms:**
- Github
- Amazon Web Services (AWS)

**Package managers:**
- pip
- npm

**Frameworks, modules and libraries:**
- FastAPI (Framework)
- venv (Python module)
- SQLModel (Python library)
- PM2

# Developing the Workshop
## Configuring a Repository in Github
For connect and transfer files to the repository it will be used SSH. In addition, before creating the key pairs, the repository will be created via GUI in [Github](https://github.com).

Once the repository is configured, it is required to set a key pairs to connect the local device to the remote repository.

``` bash
# Generate a key type ed25519 and add a comment to identify the public key
$ ssh-keygen -t ed25519 -C "my@email.example"

# Configure ssh-agent to maintain the information in memory for next access to the EC2 instance
$ eval "$(ssh-agent -s)"

# Add the private key to the agent
$ ssh-add ~/.ssh/id_ed25519

``` 

Use the command for ssh-agent if you are in a trusted device. The ssh-agent omits the passphrase for the ssh key.

After configuring the key pairs, it is necesary to copy the content within .pub file; then, copy the content within the security section of Github:
1. Click on your profile picture
2. Go to *Settings*
3. Go to *SSH and GPG keys*
4. Select *New SSH key*
5. Paste the content of the .pub file previously coppied

``` bash
# Test if Github accepts the key pairs
$ ssh -T git@github.com
```

## Adding Files to the Repository
After configuring the connection via SSH, it is necessary to add initial files to the repository and connect our local workspace remotely.

``` bash
$ git init .
$ touch README.md .gitignore
$ git add .
$ git commit -m "Dumb text"
$ git branch -M main
$ git remote add origin git@github.com:user/reponame.git
$ git push -u origin main
```

This is the process for the first time and to establish a connection between our repository and the local workspace. When the connection is established, the `add`, `commit` and `push` commands are required. 

## Configuring main.py for the API

To develop the API it is recommended to create a separate folder. Maker sure that `venv` python module is installed.

``` bash
# "env" could be anything 
$ python3 -m venv env 

$ touch main.py

# Activate the virtual environment
$ source env/bin/activate

$ pip install "fastapi[standard]" sqlmodel
```

These process is necessary to give functionality the [API file](./main.py). After finishing your own *main.py*, follow again the process to [commit your changes](Adding Files to the Repository). 

> Note
> Be aware that is not recommended to include the content of your *env* folder and your privake .pem key.
> Therefore, within the *.gitignore* file include `env/` and `.pem`. 

## Configure the EC2 Instance in AWS
To configure an instance in AWS, log in within your [Amazon Console](https://aws.amazon.com/es/) and access to the EC2 service.

After that, launch an instance using the Quick Start Amazon Image Machine (AMI). Select your own preferences for the type of machine and operating system. In my case, I will select Ubuntu.

It is necessary to create a key pairs to connect to the EC2 instance. I will create a .pem key pairs. When the public and private key are downloaded, it is required to set a read permission for the private key only for the owner. When everything is ready, create the instante.

Before connecting to the EC2, it is necessary to configure a rule for admit inbound traffic.
1. Go to the EC2 console.
2. Go to *Network & Security*.
3. Go to *Security Groups*. 
4. Select the security group associated with your EC2.
5. Go to *Inbound rules*.
6. Select *Edit inbound rules*.
7. Add a rule to accept traffic from a custom TCP port. (I used the 8000 port)

``` bash
# Set the permissions
$ chmod 400 key.pem

# Connect using ssh
# The link is provided in the platform of aws
$ ssh -i "key.pem" user_os@ec2-ip.region.amazonaws.com
``` 

## Clone Repository and Set Up the API

The process within the EC2 system is similarly as in the [configuration of the main.py file](#configuring-mainpy-for-the-api)
``` bash
# This could be different depending on the OS
$ sudo apt update -y && sudo apt upgrade -y 
$ sudo apt install python3.12-venv nodejs npm -y

# Install pm2 daemon 
$ npm pm2
 
# Clone the remote repository
$ git clone https://github.com/user/repo.git

# Configure the environment in the server
$ cd repo_name/
$ python3 -m venv env
$ source env/bin/activate
$ pip install "fastapi[standard]" sqlmodel

# Initialize the service using pm2
$ pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name fastapi-app 
```
When the service is ready, the API will be accesible with the public IP of the EC2 in the direction *<public_ip>:8000/docs*. 
