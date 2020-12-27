# Introduction 
This is an HTTP API to return largest 5 repos of a given GitHub handle in descending order.

# Usage / Live Demo
_Temporarily down as part of moving my website to AWS_

The base URL to deployed API is ```https://apis.melaus.xyz/top5```, and has two endpoints:

- ```https://apis.melaus.xyz/top5/<github_handle>```:
    - returns high-level information (name, url and size) about the largest 5 repos of a user
- ```https://apis.melaus.xyz/top5/<github_handle>/detailed```: 
    - returns all information about the largest 5 repos of a user


# Technical Details
## API Development
```Python``` and the ```Flask``` framework is used to create this API. 

This is built in two parts. ```github.py``` works as a 'library' and carries out the call to the public GitHub API to obtain repo information of a user. The content is being sorted and transformed to form the output of the two endpoints. The GitHub API returns a status 404 if the API call is failed, e.g. a non-existing username is given. This API handles such error similarly. ```top5_api.py``` forms the structure of the API call using ```Flask```.

Pagination is used to retrieve all public repos of the given user, as the maximum number of repos that can be retrieved per call is 100. A token is used to increase the rate limit per hour.

## Deployment
This is the first time I have written an API and made it available on the web. The closest experience was setting up my [static personal website](https://www.melaus.xyz) using ```pelican```, which also gave me basic experience in encrypting a website, basic handling of ```nginx``` and self-hosting on DigitalOcean.

For deployment, the first hurdle that needed solving is the way to deploy a ```Flask``` API. To enable a more scalable and reliable solution, a ```uWSGI``` application server is used rather than the built-in server. With the help of this [guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04), I set up the API with associated configurations and run it as a system service, so that it is quicker to make changes and can run in the background and restart automatically if the machine was turned off.

To host the API, I use my aforementioned personal website. First, I created the subdomain ```apis.melaus.xyz``` by adding a CNAME DNS record that aliases to ```apis.melaus.xyz```. I then created the nginx configuration file that specifies the local location of the API, so that it can be served on the web. Also, I updated my certificate to include the new subdomain to make it accessible. By enabling the configuration and restarting ```nginx```, the API is live.
