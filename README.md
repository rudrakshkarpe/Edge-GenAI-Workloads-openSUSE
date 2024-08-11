# Edge-GenAI-Workloads-openSUSE
Google Summer of Code 2024 @ openSUSE Project

<details>


<summary> TODO ✅ </summary> 

- [ ] Fix local rancher cluster issue 
- [ ] Raise PR for openSUSE News
- [ ] Try Podman approach 
- [ ] Refactor codebase 
- [ ] Add more tests
- [ ] Add more documentation
- [ ] Fix local document caache issue

</details>


<details> 

<summary> Deployment set-up </summary>


### setting up rancher on a single docker node 

```bash
docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged \
  rancher/rancher:v.2.8.4
```




### setting up a custom k3s cluster   

```bash
curl -sfL https://get.k3s.io | \
        INSTALL_K3S_VERSION=v1.27.15+k3s2 \
        INSTALL_K3S_EXEC='server --cluster-init --write-kubeconfig-mode=644' \
        INSTALL_K3S_NAME='k3s-ollama' \
        INSTALL_K3S_BIN_DIR='/home/rudraksh/k3s' \
        sh -s -
```

</details>