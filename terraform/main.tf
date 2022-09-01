
provider "aws" {
  shared_credentials_files = ["~/.aws/credentials"]
  profile                  = "cloudplayground"
  region = "us-east-1"
}

# create servers
resource "aws_instance" "sandbox" {
  ami           = "ami-052efd3df9dad4825"
  instance_type = "t1.micro"
  root_block_device {
    volume_size = 10 # in GB <<----- I increased this!
  }
  vpc_security_group_ids = [aws_security_group.main.id]
  associate_public_ip_address = true
  count = 1
  key_name = "mykey"

  tags = {
    Name = "server-${count.index}"
  }
  user_data = <<EOF
#!/bin/bash
LOGFILE=/home/ubuntu/activity.log
# install pip
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install python3-pip python3-venv python3-flask -y >> $LOGFILE
# cd folder
cd /home/ubuntu
# clone repo
git clone https://github.com/h0me5k1n/sosrallycalc.git >> $LOGFILE
# chmod repo
sudo chown ubuntu:ubuntu sosrallycalc -R
# cd repo
cd sosrallycalc
# create environment
python3 -m venv env;source env/bin/activate >> $LOGFILE
# pip flask
pip install flask
# run app in background
nohup python3 -u sosrallycalc.py >> $LOGFILE 2>&1 &

EOF
}

resource "aws_security_group" "main" {
  egress = [
    {
      cidr_blocks      = [ "0.0.0.0/0", ]
      description      = ""
      from_port        = 0
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "-1"
      security_groups  = []
      self             = false
      to_port          = 0
    }
  ]
# the below is needed in order for ssh to work
 ingress                = [
   {
     cidr_blocks      = [ "0.0.0.0/0", ]
     description      = "ssh"
     from_port        = 22
     ipv6_cidr_blocks = []
     prefix_list_ids  = []
     protocol         = "tcp"
     security_groups  = []
     self             = false
     to_port          = 22
  },
   {
     cidr_blocks      = [ "0.0.0.0/0", ]
     description      = "flask"
     from_port        = 3000
     ipv6_cidr_blocks = []
     prefix_list_ids  = []
     protocol         = "tcp"
     security_groups  = []
     self             = false
     to_port          = 5044
  }
  ]
}

# add my public key to the key pairs list
resource "aws_key_pair" "deployer" {
  key_name   = "mykey"
  public_key = file("~/.ssh/id_rsa.pub")
}

