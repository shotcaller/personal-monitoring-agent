To get postgres in docker run command

```shell
docker run --name agent-postgres `
  -e POSTGRES_USER=agentuser `
  -e POSTGRES_PASSWORD=agentpass `
  -e POSTGRES_DB=agentdb `
  -p 5432:5432 `
  -d postgres:16
```