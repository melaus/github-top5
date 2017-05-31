# Introduction 
This is an HTTP API to return largest 5 repos of a given GitHub handle in descending order.

# Usage / Live Demo
The base URL to deployed API is ```https://apis.melaus.xyz/top5```, and has two endpoints:

- ```https://apis.melaus.xyz/top5/<github_handle>```:
    - returns high-level information (name, url and size) about the largest 5 repos of a user
- ```https://apis.melaus.xyz/top5/<github_handel>/detailed```: 
    - returns all information about the largest 5 repos of a user


# Technical Details
## API Development
```Python``` and the ```Flask``` framework is used to create this API. 

This is built in two parts. ```github.py``` works as a 'library' and carries out the call to the public GitHub API to obtain repo information of a user. The content is being sorted and transformed to form the output of the two endpoints. The GitHub API returns a status 404 if the API call is failed, e.g. a non-existing username is given. This API handles such error similarly.

```top5_api.py``` forms the structure of the API call using ```Flask```.

## Deployment
The first hurdle that neede solving is the way to deploy a ```Flask``` API. To enable a more scalable and reliable solution, a ```uWSGI``` application server is used rather than the built-in server. With the help of this [guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04), I set up the API with associated configurations and run it as a system service, so that it is quicker to make changes and can run in the background and restart automatically if the machine was turned off.

To host the API, I use my encrypted, self-hosted [website](https://www.melaus.xyz) on DigitalOcean with a basic setup of ```nginx```. 

First, I created the subdomain ```apis.melaus.xyz``` by adding a CNAME DNS record that aliases to ```apis.melaus.xyz```. I then created the nginx configuration file that specifies the local location of the API, so that it can be served on the web. By enabling the configuration and restarting ```nginx```, the API is live.
