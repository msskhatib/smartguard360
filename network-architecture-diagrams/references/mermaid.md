# Mermaid for network & architecture diagrams

Mermaid is the default tool: text-based, renders natively on GitHub, GitLab,
most Markdown viewers, and Claude artifacts with zero install. Two diagram
types cover almost every architecture need.

- **`flowchart`** — the workhorse. `subgraph` blocks give you labeled trust
  zones (VPC, subnets, on-prem), edges carry protocol/port labels, and it
  renders everywhere. Use this by default.
- **`architecture-beta`** — purpose-built for cloud diagrams with grouped
  services and icons. Nicer for high-level "boxes in a cloud" pictures, but
  newer and less universally supported. Use when you want icons and a clean
  grouped look and the render target supports it.

## Table of contents
- [flowchart basics](#flowchart-basics)
- [Recipe: 3-tier web app in a VPC](#recipe-3-tier-web-app-in-a-vpc)
- [Recipe: public/private subnets across AZs](#recipe-publicprivate-subnets-across-azs)
- [Recipe: microservices request flow](#recipe-microservices-request-flow)
- [Recipe: hybrid on-prem to cloud](#recipe-hybrid-on-prem-to-cloud)
- [Styling: mark public-facing / async](#styling)
- [architecture-beta basics](#architecture-beta-basics)

## flowchart basics

Direction: `LR` (left→right, best for request flows) or `TB` (top→bottom,
best for layered stacks). Node shapes carry meaning — use them consistently:

```
flowchart LR
  user((User))                %% (( )) circle = external actor / entry point
  lb[Load Balancer]           %% [ ]   rectangle = service / compute
  db[(PostgreSQL)]            %% [( )] cylinder  = database / datastore
  cache{{Redis}}              %% {{ }} hexagon   = cache / queue
  bucket[/Object Store/]      %% [/ /] parallelogram = storage / external API
```

Edges carry labels — always put the protocol/port or intent on the wire:

```
  user -- HTTPS 443 --> lb
  lb -- HTTP --> app
  app -. async / SQS .-> worker   %% -. .-> dashed = asynchronous
```

Group nodes into labeled boundaries with `subgraph`:

```
flowchart LR
  subgraph vpc["VPC 10.0.0.0/16"]
    subgraph public["Public subnet"]
      alb[ALB]
    end
    subgraph private["Private subnet"]
      app[App servers]
    end
  end
  alb --> app
```

## Recipe: 3-tier web app in a VPC

```mermaid
flowchart LR
  user((Users))
  cdn[/CloudFront CDN/]

  subgraph vpc["VPC 10.0.0.0/16"]
    subgraph pub["Public subnet"]
      alb[Application<br/>Load Balancer]
    end
    subgraph app["Private subnet — app tier"]
      web1[Web server]
      web2[Web server]
      web3[Web server]
    end
    subgraph data["Private subnet — data tier"]
      db[(PostgreSQL<br/>primary)]
      dbr[(PostgreSQL<br/>replica)]
      cache{{Redis}}
    end
  end

  user -- HTTPS 443 --> cdn -- HTTPS --> alb
  alb -- HTTP 8080 --> web1 & web2 & web3
  web1 & web2 & web3 -- TCP 5432 --> db
  web1 & web2 & web3 -- TCP 6379 --> cache
  db -. replication .-> dbr
```

`a & b & c` fans one edge out to several nodes — concise for a tier of
identical instances.

## Recipe: public/private subnets across AZs

```mermaid
flowchart TB
  igw[Internet Gateway]
  subgraph vpc["VPC"]
    direction LR
    subgraph az1["Availability Zone A"]
      pub1[Public subnet<br/>NAT GW]
      prv1[Private subnet<br/>App + DB]
    end
    subgraph az2["Availability Zone B"]
      pub2[Public subnet<br/>NAT GW]
      prv2[Private subnet<br/>App + DB]
    end
  end
  igw --> pub1 & pub2
  pub1 --> prv1
  pub2 --> prv2
```

`direction LR` inside a subgraph lays that group out horizontally while the
outer graph stays vertical — useful for placing AZs side by side.

## Recipe: microservices request flow

```mermaid
flowchart LR
  client((Client))
  gw[API Gateway]
  subgraph k8s["Kubernetes namespace: prod"]
    auth[auth-svc]
    orders[orders-svc]
    pay[payment-svc]
    q{{Kafka}}
    notif[notify-svc]
  end
  db[(orders-db)]

  client -- HTTPS --> gw
  gw -- gRPC --> auth
  gw -- gRPC --> orders
  orders -- TCP 5432 --> db
  orders -- gRPC --> pay
  orders -. publish .-> q
  q -. consume .-> notif
```

## Recipe: hybrid on-prem to cloud

```mermaid
flowchart LR
  subgraph onprem["On-premises datacenter"]
    erp[ERP system]
    fw[Firewall]
  end
  subgraph cloud["AWS"]
    subgraph vpc["VPC"]
      app[App tier]
      dw[(Data warehouse)]
    end
  end
  erp --> fw
  fw == VPN / IPsec ==> app
  app -- ETL --> dw
```

`==>` draws a thick edge — handy for emphasizing a primary trunk like a
VPN tunnel or a direct-connect link.

## Styling

Highlight what faces the internet or which paths are asynchronous with
`classDef`. Restraint matters — color should encode one clear fact:

```mermaid
flowchart LR
  net((Internet)):::public
  alb[ALB]:::public
  app[App]
  net --> alb --> app

  classDef public fill:#fde68a,stroke:#d97706,color:#000;
```

Conventions worth keeping consistent across a set of diagrams: dashed edge =
asynchronous, thick edge = primary/trunk link, a warm fill = public-facing.
If you use them, add a one-line legend node so readers don't have to guess.

## architecture-beta basics

For a clean, grouped, icon-based cloud picture. Built-in icon names include
`cloud`, `database`, `disk`, `internet`, `server`; more are available by
registering an Iconify pack if the target supports it.

```mermaid
architecture-beta
    group api(cloud)[Production VPC]

    service gw(internet)[Gateway] in api
    service app(server)[App Server] in api
    service db(database)[Database] in api
    service store(disk)[Object Store] in api

    gw:R -- L:app
    app:R -- L:db
    app:B -- T:store
```

Edges attach to a compass side of each node (`:T` `:B` `:L` `:R`), which
lets you control routing. `in api` places a service inside a group. Prefer
`flowchart` when you need edge labels (ports/protocols) — `architecture-beta`
edges are unlabeled — or when the render target may not support the newer
syntax.
