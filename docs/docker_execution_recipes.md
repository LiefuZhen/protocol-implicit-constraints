# Docker Execution Recipes（未实测）

> 本文件记录各 Subject 的 Docker 构建与运行线索。
> 当前所有条目均为“未实测”，只能作为后续编写 Dockerfile、固定 commit/tag、补依赖和验证 build/run 的起点。
> `Source pending` 表示该 Subject 出现在论文 Table I 中，但当前上传的 `ProtocolGuard.zip` 尚未确认完整源码路径或可执行构建方式。

## 1. 使用口径

| 字段 | 含义 |
|---|---|
| Subject | 实验对象 Implementation。 |
| Status | 当前 Docker 可执行性状态。默认均为未实测。 |
| Base Image | 建议起始镜像，不代表最终实验镜像。 |
| Dependencies | 初步依赖线索，需要后续按目标 commit 实测修正。 |
| Build Command | 初步构建命令，可能需要按上游 README、tag 和系统依赖调整。 |
| Run Command | 初步运行入口，后续需要补配置文件、证书、端口和测试输入。 |
| Notes | 额外说明，尤其是 artifact 确认情况。 |

## 2. ProtocolGuard Artifact 中可确认的 Sol 线索

Sol 是当前上传 artifact 中唯一可以确认存在 worked example 源码和 Dockerfile 的 Subject。它仍然需要在本仓库后续重新 Docker build/run 后，才能从“未实测”升级为“已实测”。

| Subject | Status | Base Image | Dependencies | Build Command | Run Command | Notes |
|---|---|---|---|---|---|---|
| Sol | Artifact confirmed; 未实测 | `rikorose/gcc-cmake` in artifact Dockerfile; normalized option `ubuntu:22.04` | artifact Dockerfile 依赖镜像内 gcc/cmake；normalized option 可补 `build-essential git cmake clang llvm` | artifact Dockerfile: `cmake -DDEBUG=0 . && make`; normalized option: `cmake -DCMAKE_C_COMPILER=clang . && make` | artifact Dockerfile: `./sol -a 0.0.0.0` | `ProtocolGuard.zip/example/sol.tar.gz` confirmed. Artifact Dockerfile contains `COPY . /sol`, `WORKDIR /sol`, `EXPOSE 1883`, `CMD ./sol -a 0.0.0.0`. |

## 3. 主表 Subject Docker 线索（未实测）

| Subject | Status | Base Image | Dependencies | Build Command | Run Command | Notes |
|---|---|---|---|---|---|---|
| TinyMQTT | Source pending; 不可执行 | 待确认 | 待确认 | 待确认 | 待确认 | 论文 Table I Subject；当前上传的 `ProtocolGuard.zip` 未确认源码路径。已检查候选仓库 `https://github.com/hsaturn/TinyMqtt`，但该仓库主要是 C++ / Arduino / ESP 场景，且未确认版本 `6226ad`，暂不作为 confirmed subject。 |
| Mosquitto | 未实测 | `ubuntu:22.04` | `build-essential git cmake libc-ares-dev libssl-dev` | `cmake -S . -B build && cmake --build build` | `./build/src/mosquitto -c mosquitto.conf` | 需要后续固定 commit/tag，并补最小 `mosquitto.conf`。 |
| libcoap | 未实测 | `ubuntu:22.04` | `build-essential git cmake libssl-dev` | `cmake -S . -B build -DENABLE_TESTS=ON && cmake --build build` | `./build/bin/coap-server -v 7` | 第一轮建议限定 UDP server 路径。 |
| FreeCoAP | 未实测 | `ubuntu:22.04` | `build-essential git make` | `make` | `./server/coap-server` | 需要按实际仓库目录复核 binary 路径。 |
| Dnsmasq | 未实测 | `ubuntu:22.04` | `build-essential git pkg-config libdbus-1-dev nettle-dev` | `make` | `./src/dnsmasq --no-daemon --port=5353` | 低端口和 DHCP 场景可能需要容器权限，第一轮可先跑 DNS 非特权端口。 |
| NDHS | Candidate upstream confirmed; 未实测 | `ubuntu:22.04` | `build-essential git make`；可能需要 `ragel` | `git checkout 4b2728a && make` | 待补最小 `ndhs.conf` 后运行；可先用 `./ndhs --help` 检查入口 | 候选上游 `https://github.com/niklata/ndhs` 已确认；commit `4b2728a` 已确认；协议为 DHCPv4/DHCPv6 server，语言以 C 为主；Docker build/run 仍待验证。 |
| pure-ftpd | 未实测 | `ubuntu:22.04` | `build-essential git autoconf automake libtool libssl-dev` | `./autogen.sh && ./configure && make` | `./src/pure-ftpd -S 2121` | 需要补用户、目录和权限配置。 |
| uFTP | Source pending; 不可执行 | 待确认 | 待确认 | 待确认 | 待确认 | 论文 Table I Subject；当前上传的 `ProtocolGuard.zip` 未确认源码路径。已检查候选仓库 `https://github.com/troglobit/uftpd`，该仓库是 C 语言 FTP/TFTP server，但未确认版本 `646404`，且未确认 AUTH/PBSZ/PROT 或 FTPS 支持，暂不作为 confirmed subject。 |
| TLSE | 未实测 | `ubuntu:22.04` | `build-essential git make` | `make` | `./examples/server` | 需要复核 examples 路径和证书参数。 |
| wolfSSL | 未实测 | `ubuntu:22.04` | `build-essential git autoconf libtool` | `./autogen.sh && ./configure --enable-tls13 && make` | `./examples/server/server -v 4` | 代码量大，建议后续固定较小配置。 |
| llhttp | 未实测 | `ubuntu:22.04` | `build-essential git cmake python3 nodejs npm` | `npm install && make` | `./build/llhttp_test` | 更适合先写 parser harness，不一定需要完整 daemon。 |
| HAProxy | 未实测 | `ubuntu:22.04` | `build-essential git libssl-dev zlib1g-dev` | `make TARGET=linux-glibc USE_OPENSSL=1` | `./haproxy -f haproxy.cfg -db` | 需要补最小前后端配置。 |
| nginx | 未实测 | `ubuntu:22.04` | `build-essential git libpcre3-dev zlib1g-dev libssl-dev` | `./auto/configure --with-debug && make` | `objs/nginx -c nginx.conf -g 'daemon off;'` | 需要补容器内绝对 prefix 或可写临时目录配置。 |
| Apache httpd | 未实测 | `ubuntu:22.04` | `build-essential git libapr1-dev libaprutil1-dev libpcre2-dev libssl-dev` | `./buildconf && ./configure && make` | `./httpd -X -f conf/httpd.conf` | 依赖和配置较多，建议放 P1。 |
| nghttp2 | 未实测 | `ubuntu:22.04` | `build-essential git autoconf automake libtool pkg-config libssl-dev` | `autoreconf -i && ./configure && make` | `./src/nghttpd 8443 server.key server.crt` | 需要生成测试证书。 |
| h2o | 未实测 | `ubuntu:22.04` | `build-essential git cmake libssl-dev zlib1g-dev` | `cmake -S . -B build && cmake --build build` | `./build/h2o -c h2o.conf` | 需要补 HTTP/2 TLS 配置。 |
| quiche | 未实测 | `ubuntu:22.04` | `build-essential git cmake cargo clang` | `cargo build --examples` | `./target/debug/examples/http3-server --listen 0.0.0.0:4433` | Rust/Cargo 依赖较大，后续可考虑官方 image 或缓存。 |
| ngtcp2 + nghttp3 | 未实测 | `ubuntu:22.04` | `build-essential git autoconf automake libtool pkg-config libssl-dev` | 按 ngtcp2/nghttp3 README 先构建依赖再构建 examples | `examples/server 0.0.0.0 4433 server.key server.crt` | 构建链较长，需要单独实测。 |
| BIND 9 | 未实测 | `ubuntu:22.04` | `build-essential git libuv1-dev libssl-dev libnghttp2-dev pkg-config` | `autoreconf -fi && ./configure && make` | `./bin/named/named -g -c named.conf` | 建议先跑非递归最小 named.conf。 |
| miekg/dns | 未实测 | `ubuntu:22.04` | `git golang-go` | `go test ./...` | `go run ./_examples/reflect` | 更适合作为 Go harness library。 |
| OpenSSL | 未实测 | `ubuntu:22.04` | `build-essential git perl` | `./Configure linux-x86_64 && make` | `apps/openssl s_server -accept 4433 -tls1_3 -cert cert.pem -key key.pem` | 需要证书；构建耗时较长。 |
| mbedTLS | 未实测 | `ubuntu:22.04` | `build-essential git cmake python3` | `cmake -S . -B build && cmake --build build` | `./build/programs/ssl/ssl_server2` | 需复核 TLS 1.3 是否默认启用。 |
| Apache Qpid Proton | 未实测 | `ubuntu:22.04` | `build-essential git cmake python3-dev libsasl2-dev libssl-dev` | `cmake -S . -B build && cmake --build build` | `./build/c/examples/broker` | 需要复核 examples 是否随当前版本构建。 |
| RabbitMQ | 未实测 | `ubuntu:22.04` | `erlang git make` | `make` | `make run-broker` | 实际建议优先用官方 RabbitMQ image 做协议测试，再考虑源码构建。 |
| librdkafka | 未实测 | `ubuntu:22.04` | `build-essential git cmake libssl-dev zlib1g-dev` | `./configure && make` | `examples/rdkafka_example -b kafka:9092 -L` | 需要外部 Kafka broker 或 docker compose。 |
| Apache Kafka | 未实测 | `ubuntu:22.04` | `openjdk-17-jdk git` | `./gradlew jar -x test` | `bin/kafka-server-start.sh config/server.properties` | Java/集群成本较高，建议后期。 |
| Dropbear SSH | 未实测 | `ubuntu:22.04` | `build-essential git zlib1g-dev` | `./configure && make` | `./dropbear -F -E -p 2222` | 需要生成 host key。 |
| chrony | 未实测 | `ubuntu:22.04` | `build-essential git libcap-dev libseccomp-dev` | `./configure && make` | `./chronyd -d -f chrony.conf` | 需要补最小 chrony.conf。 |
| Net-SNMP | 未实测 | `ubuntu:22.04` | `build-essential git autoconf libtool libssl-dev` | `./configure && make` | `agent/snmpd -f -Lo -C -c snmpd.conf` | 配置复杂，建议后期。 |
| libmodbus | 未实测 | `ubuntu:22.04` | `build-essential git autoconf libtool` | `./autogen.sh && ./configure && make` | `./tests/unit-test-server` | 适合第一轮扩展 harness。 |
| open62541 | 未实测 | `ubuntu:22.04` | `build-essential git cmake python3` | `cmake -S . -B build && cmake --build build` | `./build/bin/examples/server` | 需复核 examples 构建选项。 |

## 4. 扩展池 Docker 线索（未实测）

| Subject | Status | Base Image | Dependencies | Build Command | Run Command | Notes |
|---|---|---|---|---|---|---|
| lwIP | 未实测 | `ubuntu:22.04` | `build-essential git cmake` | `cmake -S . -B build && cmake --build build` | `custom unit test harness` | 不是传统 daemon，需要自己写 harness。 |
| lksctp-tools | 未实测 | `ubuntu:22.04` | `build-essential git autoconf automake libtool` | `./bootstrap && ./configure && make` | `./src/apps/sctp_test` | SCTP 容器网络能力需要额外确认。 |
| libwebsockets | 未实测 | `ubuntu:22.04` | `build-essential git cmake libssl-dev` | `cmake -S . -B build && cmake --build build` | `./build/bin/lws-minimal-ws-server` | 需要复核 examples 是否启用。 |
| OpenLDAP | 未实测 | `ubuntu:22.04` | `build-essential git groff libssl-dev libsasl2-dev` | `./configure && make depend && make` | `servers/slapd/slapd -d 1 -f slapd.conf` | 配置成本较高。 |
| FreeRADIUS | 未实测 | `ubuntu:22.04` | `build-essential git libssl-dev libtalloc-dev` | `./configure && make` | `build/bin/local/radiusd -X` | 需要补最小 users/clients 配置。 |
| FRRouting | 未实测 | `ubuntu:22.04` | `build-essential git autoconf automake libtool libreadline-dev` | `./bootstrap.sh && ./configure && make` | `bgpd -f bgpd.conf -d` | 建议后续用容器网络拓扑实测。 |
| Postfix | 未实测 | `ubuntu:22.04` | `build-essential git libdb-dev libssl-dev` | `make makefiles && make` | `master -d` | 服务配置较重。 |
| Dovecot | 未实测 | `ubuntu:22.04` | `build-essential git autoconf automake libtool libssl-dev` | `./autogen.sh && ./configure && make` | `dovecot -F -c dovecot.conf` | 需要补认证和邮箱目录配置。 |
| Redis | 未实测 | `ubuntu:22.04` | `build-essential git tcl` | `make` | `src/redis-server --protected-mode no` | 非 RFC，但适合线协议 parser/state 扩展。 |
| memcached | 未实测 | `ubuntu:22.04` | `build-essential git autoconf libevent-dev` | `./autogen.sh && ./configure && make` | `./memcached -u root -p 11211` | 非 RFC，协议简单。 |
| PostgreSQL | 未实测 | `ubuntu:22.04` | `build-essential git bison flex libreadline-dev zlib1g-dev` | `./configure && make` | `postgres -D data` | 需要 `initdb` 和数据目录。 |
| NATS Server | 未实测 | `ubuntu:22.04` | `git golang-go` | `go build ./...` | `./nats-server -DV` | 非 RFC，但 message queue 扩展价值高。 |
| Kamailio | 未实测 | `ubuntu:22.04` | `build-essential git bison flex libssl-dev` | `make cfg && make all` | `kamailio -f kamailio.cfg -DD -E` | 依赖和配置较多。 |
| live555 | 未实测 | `ubuntu:22.04` | `build-essential wget` | `./genMakefiles linux && make` | `./testProgs/testOnDemandRTSPServer` | 上游发布形态需复核。 |
| rsyslog | 未实测 | `ubuntu:22.04` | `build-essential git autoconf automake libtool pkg-config` | `autoreconf -fvi && ./configure && make` | `tools/rsyslogd -n -f rsyslog.conf` | 需要补最小配置。 |
| Fast DDS | 未实测 | `ubuntu:22.04` | `build-essential git cmake` | `cmake -S . -B build && cmake --build build` | `examples/C++/HelloWorldExample` | 依赖链较长，建议后期。 |

## 5. 后续实测升级标准

一个 recipe 只有同时满足以下条件，才能从“未实测”改为“已实测”：

1. 固定上游 repo、commit/tag 和 license。
2. Docker build 在干净环境中成功。
3. Run command 能在容器中启动目标 parser/server/client。
4. 至少有一个最小协议输入能触发目标处理路径。
5. 记录端口、配置文件、证书、测试输入和退出方式。
