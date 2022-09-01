# MANUAL RUNNING
1. Clone the project
2. Create a virtual environment
```
python3 -m venv env;source env/bin/activate
```
2. install flask
```
pip install flask
```
3. Run the app
```
python3 sosrallycalc.py
```
# DOCKER
Create and run in a container
Build a docker container
```
docker build --tag sosrallycalc .
```
Run the container
```
docker run -p 3000:3000 sosrallycalc
```
# TERRAFORM
Although this isn't the proper usage for Terraform, I have included a main.tf file in the terraform folder.
aws credentials should be configured already (as per aws cli) and, by default, the main.tf uses a profile called "cloudplayground"
```
aws configure --profile cloudplayground
```
Then use the following to deploy:
```
terraform init
terraform plan
terraform apply
```