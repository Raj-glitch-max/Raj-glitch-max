<h1 align="center">Raj Patil</h1>

<p align="center">
  DevOps Engineer &nbsp;·&nbsp; Open Source &nbsp;·&nbsp; AWS &nbsp;·&nbsp; Kubernetes &nbsp;·&nbsp; Terraform
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/raj-patil-311b6b259/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  &nbsp;
  <a href="mailto:rpdinkar92260@gmail.com">
    <img src="https://img.shields.io/badge/Email-EA4335?style=flat&logo=gmail&logoColor=white" alt="Email" />
  </a>
  &nbsp;
  <img src="https://komarev.com/ghpvc/?username=Raj-glitch-max&color=6e7681&style=flat" alt="Profile views" />
</p>

---

<div align="center">

<h3><code>avi@github ~ $ whoami</code></h3>
<table>
  <tr>
    <td valign="top"><img src="./avi-ascii.svg" width="370" /></td>
    <td valign="top"><img src="./info-card.svg" width="490" /></td>
  </tr>
</table>

<br><br>

<h3><code>avi@github ~ $ ./contributions.sh</code></h3>
<img src="./contrib-heatmap.svg" width="860" />

</div>

---


## What I build

I find real gaps in DevOps tooling and ship focused, composable CLI tools that solve one thing precisely.

---

## Projects

### [tf-why](https://github.com/Raj-glitch-max/tf.why) &nbsp;·&nbsp; `pip install tf-why`

> Terraform tells you something drifted. **tf-why tells you who did it.**

```bash
terraform show -json plan.tfplan | tf-why
```

```
aws_security_group.web  (ingress rules changed)
├── Changed by:   john.doe@company.com
├── When:         2 days ago
├── Via:          AWS Console
└── Event:        AuthorizeSecurityGroupIngress
```

Reads Terraform plan JSON → queries AWS CloudTrail → outputs the exact actor, timestamp, and method.
No database. No dashboard. No agents. 25+ AWS resource types.

---

### [kubernetes-llm-incident-response-benchmark](https://github.com/Raj-glitch-max/kubernetes-llm-incident-response-benchmark)

> Benchmarking LLMs on real Kubernetes incident diagnosis.

Injects real failure scenarios into a live cluster and measures how accurately LLMs diagnose, explain, and suggest remediation — structured, repeatable, and scored.

---

### [AI-DRIVEN-self-healing-CICD](https://github.com/Raj-glitch-max/AI-DRIVEN-self-healing-CICD)

> A CI/CD pipeline that detects and heals its own failures.

GitHub Actions + LLM pipeline that monitors build failures, classifies root cause, and automatically applies or suggests fixes — closing the loop between failure detection and remediation.

---

## Stack

<p>
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=FF9900" alt="AWS"/>
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white" alt="Kubernetes"/>
  <img src="https://img.shields.io/badge/Terraform-623CE4?style=flat&logo=terraform&logoColor=white" alt="Terraform"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white" alt="GitHub Actions"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black" alt="Linux"/>
</p>

---

<p align="center">
  <img height="150" src="https://github-readme-stats.vercel.app/api?username=Raj-glitch-max&show_icons=true&theme=github_dark&hide_rank=true&hide_border=true" alt="GitHub stats"/>
  &nbsp;
  <img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Raj-glitch-max&layout=compact&theme=github_dark&hide_border=true" alt="Top languages"/>
</p>
