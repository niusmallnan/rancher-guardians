# rancher-guardians
守护rancher不因为细小的问题积劳成疾

## build image
`docker build -t rancher-guardians .`

## run
```
docker run -d --name rancher-guardians \
        --restart=unless-stopped rancher-guardians \
        --url <rancher-server-url:http://xxxxx:8080> \
        --access-key <access-key> \
        --secret-key <secret-key>
```
