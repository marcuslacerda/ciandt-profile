# Introduction
Profile is a powerfull search engine to search people and their connections. .

[TODO: figure show people search and connection]

## Prerequisites
[Google Cloud SDK][gcloud] used do knowledge map crawler
[Git][] and [Python 2.7.9 ][Python]. For Python you need to install the following modules:
* pip install elasticsearch
* pip install lxml
* pip install pyyaml

## Setup Instructions

```console
$ git clone git@github.com:marcuslacerda/profile.git
$ cd profile/tools
$ echo "Increase your max virtual memory areas to at least 262144"
$ sudo sysctl -w vm.max_map_count=262144;  echo "see details on https://goo.gl/pmBprp"
$ docker-compose up
```

You can override this endpoint using this variables
```
ELASTICSEARCH_URL - Full URL in the form http://MY.HOSTNAME.COM:9200, http//localhost:9200, etc
```

Install all dependencies from requirements_test.txt into lib_tests path and python-nose:
```
pip install -r requirements_test.txt -t lib_tests
sudo apt install python-nose
```
You can run all test using this command
```
export GOOGLE_CLIENT_SECRET=test
export GOOGLE_CLIENT_ID=test
export ELASTICSEARCH_URL=http://localhost:9200
docker run -p 9200:9200 docker.elastic.co/elasticsearch/elasticsearch:6.2.1
nosetests -v tests
```
#### Coverage:

To measure tests coverage in Python code. This recipe runs nosetests suite and presents coverage at the end:
```
nosetests -v --with-cover --cover-html --cover-package=. tests/
```
A detailed report from coverage can be found at cover folder in project's path.

### Jobs

```
$ pip install -r jobs/requirements.txt -t jobs/lib/
$ cd jobs
$ python script_load_profile.py --logging_level DEBUG
```
There are 3 jobs: script_load_profile, script_load_detail, script_update_rescission

## Production Setup
* Elasticsearch credentials is stored as /server/nginx/.htpasswd file. Change default value using htpasswd command

```console
$ htpasswd -c nginx/.htpasswd admin
```

## Continuous Delivery
This scaffolding uses a Travis CI for continous build, test and delivery a package on google cloud platform.
See more detail by reading this article
https://cloud.google.com/solutions/continuous-delivery-with-travis-ci


Create a tar archive file containing both of these credentials. This is important because Travis CI can decrypt only one file. In a terminal window, run the following command:

```
$ tar -pczf credentials.tar.gz service_account_secret.json .env
```

In the .travis.yml file, remove the encryption information. This information will be automatically added when you encrypt your keys in the next step. Edit the file and after before_install, remove the follow line:
```
openssl aes-256-cbc -K $encrypted_4cb330591e04_key
```

Encrypt the file locally. If prompted to overwrite the existing file, respond yes.
```console
$ sudo travis encrypt-file credentials.tar.gz --add -p
```


## Contributing
[Pull requests][] are welcome; see the [contributor guidelines][] for details.

## known issues
1. People API do not return the project name. The script scans people html to get the project name, as workaround.
1. Unit test don't work on MAC OX. There are lots of error occurred when using pip install packages on Mac OS. So I recommend you install nose using easy_install => pip uninstall nose && sudo easy_install nose

[gcloud]: https://cloud.google.com/sdk/
[Git]: http://help.github.com/set-up-git-redirect
[Python]: https://www.python.org
[Pull requests]: https://help.github.com/categories/collaborating-on-projects-using-issues-and-pull-requests/
[elasticsearch]: https://www.elastic.co/products/elasticsearch
