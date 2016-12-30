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
$ cd profile/server
$ docker-compose up
```

If you want a full local enviroment, you will need to start [elasticsearch] and define ELASTICSEARCH_URL environment.

```console
$ docker run -p 9200:9200 elasticsearch:2.4.3
```

You can override this endpoint using this variables
```
ELASTICSEARCH_URL - Full URL in the form http://MY.HOSTNAME.COM:9200, http//localhost:9200, etc
```

To execute tests, install all dependencies from requirements_test.txt into lib_tests path:
```
pip install -r requirements_test.txt -t lib_tests
```

To run the tests
```
nosetests -v tests
```
#### Coverage:

To measure tests coverage in Python code. This recipe runs nosetests suite and presents coverage at the end:
```
nosetests -v --with-cover --cover-html --cover-package=. tests/
```
A detailed report from coverage can be found at cover folder in project's path.

## Production Setup
* Elasticsearch credentials is stored as /server/nginx/.htpasswd file. Change default value using htpasswd command

```console
$ htpasswd -c nginx/.htpasswd admin
```

## Continuous Delivery
This scaffolding uses a Travis CI for continous build, test and delivery a package on google cloud platform.
See more detail by reading this article
https://cloud.google.com/solutions/continuous-delivery-with-travis-ci

ref: https://cloud.google.com/solutions/continuous-delivery-with-travis-ci
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
$ sudo travis encrypt-file credentials.tar.gz --add
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
