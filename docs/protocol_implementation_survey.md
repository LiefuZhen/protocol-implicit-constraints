# NDSS 风格 Implementation-centered 协议实验对象调研表

> 当前交付：T1 协议与实现调研。  
> 目标：构建一个可复现的 Implementation-centered experimental dataset，用于后续 CVE -> Implementation mapping、implicit constraint extraction、cross-implementation comparison 和 Docker-based execution experiments。  
> 口径：Implementation 是实验对象，Protocol 只是该对象实现的协议类别。因此主表每一行必须以 Subject (Implementation) 开头。

## 1. ProtocolGuard Artifact 核对

本调研参考论文 `ProtocolGuard: Detecting Protocol Non-compliance Bugs via LLM-guided Static Analysis and Dynamic Verification` 的 Table I，并结合官方 artifact：

| 来源 | 结论 | 对本仓库的用法 |
|---|---|---|
| GitHub `songxpu/ProtocolGuard` | 官方 README 给出 Ubuntu 22.04.3 LTS、Python 3.10、Go 1.18.1、LLVM 12/14、Cursor、GLLVM、SVF、Scapy、AFLNet 等环境线索。 | 作为 Docker execution recipe 的参考模板。 |
| Zenodo `10.5281/zenodo.17933922` | Zenodo API 标题为 `Artifact of the paper: ProtocolGuard`，open access，Apache-2.0，文件为 `ProtocolGuard.zip`。 | 作为论文实验代码和 Sol worked example 的来源。 |
| `draft/artifacts/ProtocolGuard.zip` | 本地 artifact 中包含 `rule_extraction/`、`program_slicing/`、`inconsistency_detection/`、`dynamic_verification/`、`config/config.toml`、`example/sol.tar.gz`。 | 仅作参考，不作为本仓库正式实验代码。 |

Artifact 中可以确认的路径：

| Artifact path | 对应论文模块 | 说明 |
|---|---|---|
| `ProtocolGuard/rule_extraction/` | Protocol Rule Extraction | RFC/OASIS 文档处理、keyword 处理、rule 处理。 |
| `ProtocolGuard/program_slicing/` | LLM-guided Program Slicing | LLVM/AST/SVF 静态分析框架；artifact 中 `src/` 内容需后续复核完整性。 |
| `ProtocolGuard/inconsistency_detection/violation_check.py` | LLM-based Inconsistency Detection | 用 LLM 比较 rule 与 code slice。 |
| `ProtocolGuard/dynamic_verification/assert_generate/` | Assertion Generation | 生成 assertion 插桩任务。 |
| `ProtocolGuard/dynamic_verification/packet_generate/` | Test Case Generation | 生成反例、Scapy 脚本、PCAP/raw payload。 |
| `ProtocolGuard/dynamic_verification/DFUZZ/` | Directed Protocol Fuzzing | 选择性插桩和 directed fuzzing 相关 pass。 |
| `ProtocolGuard/example/sol.tar.gz` | Worked Example | 包含 Sol 源码、Dockerfile、bitcode、SQLite DB、rule_config 和构建产物。 |

## 2. P0/P1/P2/P3 判定标准

| 优先级 | 含义 | 判定依据 |
|---|---|---|
| P0 | 第一轮优先实验对象 | Docker 容易跑；Specification 清楚；Section/Field binding 明确；输入可构造；implicit constraint 典型。 |
| P1 | 第二轮扩展对象 | 研究价值高且可执行，但状态机或工程复杂度高于 P0。 |
| P2 | 后期高价值对象 | 协议重要，但构建、状态空间、依赖或 harness 成本较高。 |
| P3 | 暂存备选对象 | 覆盖面有价值，但不建议 T1/T4 第一阶段投入。 |

## 3. NDSS 风格实验对象主表

> Docker Recipe 为最小可执行线索，后续 T4 需要固定 commit、补 Dockerfile 并实测。  
> Specification Section / Field Binding 是 implicit constraint 的 grounding key，不能只保留 RFC 首页链接。

| Subject (Implementation) | Protocol | Specification | Spec Section / Field Binding | Reason (Experiment Feasibility) | Priority | Repo / Artifact Source | Docker Execution Recipe |
|---|---|---|---|---|---|---|---|
| Sol | MQTT 3.1.1 | [OASIS MQTT 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) | §3.1 CONNECT; §3.1.3.1 Client Identifier; §3.8 SUBSCRIBE | 论文 case study 和 artifact worked example；状态机小，packet injection 容易，适合第一条 walkthrough。 | P0 | https://github.com/codepr/sol; `ProtocolGuard/example/sol.tar.gz` | base `ubuntu:22.04`; deps `build-essential git cmake clang llvm`; build `cmake -DCMAKE_C_COMPILER=clang .. && make`; run `./build/sol` |
| TinyMQTT | MQTT 3.1.1 | [OASIS MQTT 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) | §3.1 CONNECT; §3.1.3.1 Client Identifier; §3.3 PUBLISH; §3.8 SUBSCRIBE | 论文 Table I subject；规模小，适合 cross-implementation comparison；上游需从 artifact/作者处确认。 | P0 | ProtocolGuard artifact / upstream 待确认 | base `ubuntu:22.04`; deps `build-essential git cmake`; build `artifact 中确认后 make`; run `artifact 中确认 broker binary` |
| Mosquitto | MQTT 5.0 | [OASIS MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) | §3.1 CONNECT; §3.8 SUBSCRIBE; §3.9 SUBACK; §4.13 Handling Errors | 成熟实现，broker + libmosquitto client 双路径；可复用 CVE-2024-10525 的 SUBACK cardinality 线索。 | P0 | https://github.com/eclipse-mosquitto/mosquitto | base `ubuntu:22.04`; deps `build-essential git cmake libc-ares-dev libssl-dev`; build `cmake -S . -B build && cmake --build build`; run `./build/src/mosquitto -c mosquitto.conf` |
| libcoap | CoAP | [RFC 7252](https://www.rfc-editor.org/rfc/rfc7252.txt) | §3 Message Format; §4 Message Transmission; §5.3 Request/Response Matching; §5.4 Options | RFC 主试点；Token、Message ID、Option parsing 都适合 implicit constraint；但多 transport 路径需先限定 UDP。 | P0 | https://github.com/obgm/libcoap | base `ubuntu:22.04`; deps `build-essential git cmake libssl-dev`; build `cmake -S . -B build -DENABLE_TESTS=ON && cmake --build build`; run `./build/bin/coap-server -v 7` |
| FreeCoAP | CoAP | [RFC 7252](https://www.rfc-editor.org/rfc/rfc7252.txt) | §3 Message Format; §5.4 Options; §5.10 Response Code | 小型 CoAP 实现，适合和 libcoap 做 cross-implementation comparison。 | P0 | https://github.com/keith-cullen/FreeCoAP | base `ubuntu:22.04`; deps `build-essential git make`; build `make`; run `./server/coap-server` |
| Dnsmasq | DHCPv6 / DNS | [RFC 8415](https://www.rfc-editor.org/rfc/rfc8415.txt); [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.txt) | RFC 8415 §7 Message Formats; §18 Client/Server Exchanges; RFC 1035 §4.1.4 Compression | 论文 Table I DHCPv6 subject；代码规模适中，也能覆盖 DNS/DHCP 基础设施协议。 | P1 | https://thekelleys.org.uk/gitweb/?p=dnsmasq.git;a=summary | base `ubuntu:22.04`; deps `build-essential git pkg-config libdbus-1-dev nettle-dev`; build `make`; run `./src/dnsmasq --no-daemon --port=5353` |
| NDHS | DHCPv6 | [RFC 8415](https://www.rfc-editor.org/rfc/rfc8415.txt) | §7 Message Formats; §18 Client/Server Exchanges; §21 Options | 论文 Table I subject；适合 DHCPv6 message/options 复核，但上游和构建方式需从 artifact 确认。 | P1 | ProtocolGuard artifact / upstream 待确认 | base `ubuntu:22.04`; deps `build-essential git make`; build `artifact 中确认后 make`; run `artifact 中确认 daemon/client binary` |
| pure-ftpd | FTP / FTPS | [RFC 959](https://www.rfc-editor.org/rfc/rfc959.txt); [RFC 2228](https://www.rfc-editor.org/rfc/rfc2228.txt); [RFC 3659](https://www.rfc-editor.org/rfc/rfc3659.txt) | RFC 959 §4.1.1 Access Control Commands; RFC 2228 AUTH/PBSZ/PROT; RFC 3659 REST/SIZE/MLST | 论文 Table I subject；AUTH/PBSZ/PROT/REST/RNFR/RNTO 状态约束典型。 | P1 | https://github.com/jedisct1/pure-ftpd | base `ubuntu:22.04`; deps `build-essential git autoconf automake libtool libssl-dev`; build `./autogen.sh && ./configure && make`; run `./src/pure-ftpd -S 2121` |
| uFTP | FTP / FTPS | [RFC 959](https://www.rfc-editor.org/rfc/rfc959.txt); [RFC 2228](https://www.rfc-editor.org/rfc/rfc2228.txt); [RFC 3659](https://www.rfc-editor.org/rfc/rfc3659.txt) | RFC 959 §4.1.1 USER/PASS/RNFR/RNTO; RFC 2228 AUTH/PBSZ/PROT; RFC 3659 REST | 论文 case study 涉及 AUTH 后重新授权；小型实现适合状态机分析，但上游需确认。 | P1 | ProtocolGuard artifact / upstream 待确认 | base `ubuntu:22.04`; deps `build-essential git make libssl-dev`; build `artifact 中确认后 make`; run `artifact 中确认 ftpd binary -p 2121` |
| TLSE | TLS 1.3 | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt) | §4 Handshake Protocol; §4.1 Key Exchange Messages; §4.2 Extensions | 论文 Table I subject；轻量 TLS 实现，适合先做 supported_versions、key_share、certificate 等规则。 | P1 | https://github.com/eduardsui/tlse | base `ubuntu:22.04`; deps `build-essential git make`; build `make`; run `./examples/server` |
| wolfSSL | TLS 1.3 | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt) | §4.1 Handshake Protocol; §4.2.1 Supported Versions; §4.6.1 NewSessionTicket | 论文 case study 已发现 version negotiation downgrade；价值高但代码量大。 | P2 | https://github.com/wolfSSL/wolfssl | base `ubuntu:22.04`; deps `build-essential git autoconf libtool`; build `./autogen.sh && ./configure --enable-tls13 && make`; run `./examples/server/server -v 4` |
| llhttp | HTTP/1.1 parser | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9112 §2 Message; §3 Request Line; §5 Field Syntax; §6 Message Body | HTTP 必补；parser bug 和 implicit constraint 最典型；llhttp 适合轻量 harness。 | P0 | https://github.com/nodejs/llhttp | base `ubuntu:22.04`; deps `build-essential git cmake python3 nodejs npm`; build `npm install && make`; run `./build/llhttp_test` |
| HAProxy | HTTP/1.1 proxy | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9112 §6.1 Transfer-Encoding; §6.2 Content-Length; §9.3 Message Parsing Robustness | HTTP desync、header/body 边界、connection reuse 适合 implicit constraint；Docker 化容易。 | P0 | https://github.com/haproxy/haproxy | base `ubuntu:22.04`; deps `build-essential git libssl-dev zlib1g-dev`; build `make TARGET=linux-glibc USE_OPENSSL=1`; run `./haproxy -f haproxy.cfg -db` |
| nginx | HTTP/1.1 server/proxy | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9112 §3 Request Target; §5 Field Syntax; §6 Message Body | 工程成熟，适合和 HAProxy/Apache 做 cross-implementation comparison。 | P0 | https://github.com/nginx/nginx | base `ubuntu:22.04`; deps `build-essential git libpcre3-dev zlib1g-dev libssl-dev`; build `./auto/configure --with-debug && make`; run `objs/nginx -c nginx.conf -g 'daemon off;'` |
| Apache httpd | HTTP/1.1 server | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9110 §7 Routing HTTP Messages; RFC 9112 §6 Message Body | 标准服务器实现；可对照 nginx/HAProxy，但依赖略多。 | P1 | https://github.com/apache/httpd | base `ubuntu:22.04`; deps `build-essential git libapr1-dev libaprutil1-dev libpcre2-dev libssl-dev`; build `./buildconf && ./configure && make`; run `./httpd -X -f conf/httpd.conf` |
| nghttp2 | HTTP/2 | [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113.txt); [RFC 7541](https://www.rfc-editor.org/rfc/rfc7541.txt) | RFC 9113 §4 Frames; §5 Streams; §6 Frame Definitions; RFC 7541 §2.3 Header Table | HTTP/2 必补；frame length、stream state、HPACK、SETTINGS 都是 strong grounding。 | P0 | https://github.com/nghttp2/nghttp2 | base `ubuntu:22.04`; deps `build-essential git autoconf automake libtool pkg-config libssl-dev`; build `autoreconf -i && ./configure && make`; run `./src/nghttpd 8443 server.key server.crt` |
| h2o | HTTP/2 / HTTP/1.1 | [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt); [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113.txt) | RFC 9113 §5 Stream States; §6.5 SETTINGS; RFC 9112 §6 Message Body | 同时支持 HTTP/1.1/2，适合 server 行为对照；复杂度中等。 | P1 | https://github.com/h2o/h2o | base `ubuntu:22.04`; deps `build-essential git cmake libssl-dev zlib1g-dev`; build `cmake -S . -B build && cmake --build build`; run `./build/h2o -c h2o.conf` |
| quiche | QUIC / HTTP/3 | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.txt); [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.txt); [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.txt); [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.txt) | RFC 9000 §4 Streams; §12 Packets and Frames; RFC 9114 §6 Stream Mapping; §7.2 SETTINGS | QUIC/HTTP3 建议补；现代 transport state machine 典型，但依赖和状态空间较大。 | P1 | https://github.com/cloudflare/quiche | base `ubuntu:22.04`; deps `build-essential git cmake cargo clang`; build `cargo build --examples`; run `./target/debug/examples/http3-server --listen 0.0.0.0:4433` |
| ngtcp2 + nghttp3 | QUIC / HTTP/3 | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.txt); [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.txt) | RFC 9000 §7 Connection Establishment; §10 Connection Termination; RFC 9114 §4 HTTP/3 Frames | C 系生态，适合和 quiche/msquic 对照；构建依赖较多。 | P1 | https://github.com/ngtcp2/ngtcp2; https://github.com/ngtcp2/nghttp3 | base `ubuntu:22.04`; deps `build-essential git autoconf automake libtool pkg-config libssl-dev`; build `按 ngtcp2/nghttp3 README 构建`; run `examples/server 0.0.0.0 4433 server.key server.crt` |
| BIND 9 | DNS | [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.txt); [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.txt); [RFC 6891](https://www.rfc-editor.org/rfc/rfc6891.txt) | RFC 1035 §4.1.1 Header; §4.1.4 Message Compression; RFC 6891 §6 OPT RR | DNS parser/cache 价值高；compression pointer 和 EDNS 边界适合做 P1。 | P1 | https://gitlab.isc.org/isc-projects/bind9 | base `ubuntu:22.04`; deps `build-essential git libuv1-dev libssl-dev libnghttp2-dev pkg-config`; build `autoreconf -fi && ./configure && make`; run `./bin/named/named -g -c named.conf` |
| miekg/dns | DNS library | [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.txt); [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.txt) | RFC 1035 §4.1.2 Question; §4.1.3 Resource Records; §4.1.4 Compression | Go 库易写 harness，适合先构造 compression/label 边界输入。 | P1 | https://github.com/miekg/dns | base `ubuntu:22.04`; deps `git golang-go`; build `go test ./...`; run `go run ./_examples/reflect` |
| OpenSSL | TLS 1.3 / DTLS | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt); [RFC 9147](https://www.rfc-editor.org/rfc/rfc9147.txt) | RFC 8446 §4 Handshake; RFC 9147 §5 Record Layer; §7 Handshake | 生态核心但代码大；适合后期验证 TLS/DTLS 约束泛化性。 | P2 | https://github.com/openssl/openssl | base `ubuntu:22.04`; deps `build-essential git perl`; build `./Configure linux-x86_64 && make`; run `apps/openssl s_server -accept 4433 -tls1_3 -cert cert.pem -key key.pem` |
| mbedTLS | TLS 1.3 / DTLS | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt); [RFC 9147](https://www.rfc-editor.org/rfc/rfc9147.txt) | RFC 8446 §4.2 Extensions; RFC 9147 §4.2 Epoch and Sequence Number | 嵌入式 TLS/DTLS，适合 IoT 场景；比 OpenSSL 小。 | P1 | https://github.com/Mbed-TLS/mbedtls | base `ubuntu:22.04`; deps `build-essential git cmake python3`; build `cmake -S . -B build && cmake --build build`; run `./build/programs/ssl/ssl_server2` |
| Apache Qpid Proton | AMQP 1.0 | [OASIS AMQP 1.0](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.html) | AMQP 1.0 Transport: Connections, Sessions, Links, Frames, Delivery State | Message Queue 加分项；AMQP 有正式 Specification，frame/link/session 状态适合 implicit constraint。 | P1 | https://github.com/apache/qpid-proton | base `ubuntu:22.04`; deps `build-essential git cmake python3-dev libsasl2-dev libssl-dev`; build `cmake -S . -B build && cmake --build build`; run `./build/c/examples/broker` |
| RabbitMQ | AMQP 0-9-1 / AMQP 1.0 plugin | [AMQP 0-9-1](https://www.rabbitmq.com/resources/specs/amqp0-9-1.pdf); [OASIS AMQP 1.0](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.html) | AMQP 0-9-1 Method Frame; Connection.Start/Tune/Open; Channel.Open; Queue.Declare | 工业常用 MQ；功能复杂，适合作为后期 broker 行为对象。 | P2 | https://github.com/rabbitmq/rabbitmq-server | base `ubuntu:22.04`; deps `erlang git make`; build `make`; run `make run-broker` |
| librdkafka | Kafka Protocol | [Apache Kafka Protocol](https://kafka.apache.org/protocol) | Request Header; ApiVersions; Metadata; Produce; Fetch; Consumer Group APIs | Kafka 非 RFC，但工业价值高；C/C++ 客户端库适合 Docker harness。 | P1 | https://github.com/confluentinc/librdkafka | base `ubuntu:22.04`; deps `build-essential git cmake libssl-dev zlib1g-dev`; build `./configure && make`; run `examples/rdkafka_example -b kafka:9092 -L` |
| Apache Kafka | Kafka Protocol | [Apache Kafka Protocol](https://kafka.apache.org/protocol) | ApiVersions; Metadata; Produce; Fetch; JoinGroup/SyncGroup | 非 RFC 但可作为扩展；需要 Java 环境，运行成本高于 librdkafka。 | P2 | https://github.com/apache/kafka | base `ubuntu:22.04`; deps `openjdk-17-jdk git`; build `./gradlew jar -x test`; run `bin/kafka-server-start.sh config/server.properties` |
| Dropbear SSH | SSH | [RFC 4251](https://www.rfc-editor.org/rfc/rfc4251.txt); [RFC 4252](https://www.rfc-editor.org/rfc/rfc4252.txt); [RFC 4253](https://www.rfc-editor.org/rfc/rfc4253.txt); [RFC 4254](https://www.rfc-editor.org/rfc/rfc4254.txt) | RFC 4253 §7 Key Exchange; RFC 4252 §5 Authentication; RFC 4254 §5 Channel Mechanism | 小型 SSH 实现，key exchange/auth/channel 状态清楚，适合后期安全协议对照。 | P1 | https://github.com/mkj/dropbear | base `ubuntu:22.04`; deps `build-essential git zlib1g-dev`; build `./configure && make`; run `./dropbear -F -E -p 2222` |
| chrony | NTPv4 | [RFC 5905](https://www.rfc-editor.org/rfc/rfc5905.txt) | §7 Packet Format; §8 On-Wire Protocol; §9 Peer Process | UDP 基础设施协议；packet field 和 state 约束清楚，Docker 可行。 | P1 | https://gitlab.com/chrony/chrony | base `ubuntu:22.04`; deps `build-essential git libcap-dev libseccomp-dev`; build `./configure && make`; run `./chronyd -d -f chrony.conf` |
| Net-SNMP | SNMPv3 | [RFC 3411](https://www.rfc-editor.org/rfc/rfc3411.txt); [RFC 3412](https://www.rfc-editor.org/rfc/rfc3412.txt); [RFC 3414](https://www.rfc-editor.org/rfc/rfc3414.txt) | RFC 3412 §6 Message Processing; RFC 3414 §3 USM Timeliness; §3.2 Message Security | ASN.1/BER parser、security model、engineBoots/time 适合隐式约束，但配置复杂。 | P2 | https://github.com/net-snmp/net-snmp | base `ubuntu:22.04`; deps `build-essential git autoconf libtool libssl-dev`; build `./configure && make`; run `agent/snmpd -f -Lo -C -c snmpd.conf` |
| libmodbus | Modbus TCP | [Modbus Application Protocol](https://modbus.org/specs.php) | MBAP Header; Function Code; Length Field; Unit Identifier | 工控协议小，TCP payload 简单，适合作为非 Web/IoT 的 P1 扩展。 | P1 | https://github.com/stephane/libmodbus | base `ubuntu:22.04`; deps `build-essential git autoconf libtool`; build `./autogen.sh && ./configure && make`; run `./tests/unit-test-server` |
| open62541 | OPC UA | [OPC UA Core Specification](https://reference.opcfoundation.org/Core/) | SecureChannel; Session; MessageChunk; Service Request/Response | 工控/IoT 价值高，但 Specification 和状态较复杂。 | P2 | https://github.com/open62541/open62541 | base `ubuntu:22.04`; deps `build-essential git cmake python3`; build `cmake -S . -B build && cmake --build build`; run `./build/bin/examples/server` |

## 4. 候选扩展池

下表不是第一轮必须做完的对象，而是为了覆盖更多应用层和传输层协议，保留可复现实验候选。列结构仍然保持 Implementation-centered。

| Subject (Implementation) | Protocol | Specification | Spec Section / Field Binding | Reason (Experiment Feasibility) | Priority | Repo / Artifact Source | Docker Execution Recipe |
|---|---|---|---|---|---|---|---|
| lwIP | TCP/IP stack | [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.txt); [RFC 768](https://www.rfc-editor.org/rfc/rfc768.txt) | TCP state machine; sequence number; reassembly; UDP datagram boundary | 真正传输层实现，适合后期验证 TCP/UDP 约束，但 harness 成本较高。 | P2 | https://git.savannah.nongnu.org/cgit/lwip.git | base `ubuntu:22.04`; deps `build-essential git cmake`; build `cmake -S . -B build && cmake --build build`; run `custom unit test harness` |
| lksctp-tools | SCTP | [RFC 9260](https://www.rfc-editor.org/rfc/rfc9260.txt) | Association setup; multi-streaming; DATA chunk; SACK | SCTP 是传输层补充；状态复杂，先作为覆盖候选。 | P3 | https://github.com/sctp/lksctp-tools | base `ubuntu:22.04`; deps `build-essential git autoconf automake libtool`; build `./bootstrap && ./configure && make`; run `./src/apps/sctp_test` |
| libwebsockets | WebSocket | [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.txt) | §4 Opening Handshake; §5 Data Framing; masking; fragmentation | WebSocket 是 HTTP 扩展后的长连接协议，frame length/masking 隐式约束清楚。 | P1 | https://github.com/warmcat/libwebsockets | base `ubuntu:22.04`; deps `build-essential git cmake libssl-dev`; build `cmake -S . -B build && cmake --build build`; run `./build/bin/lws-minimal-ws-server` |
| OpenLDAP | LDAPv3 | [RFC 4511](https://www.rfc-editor.org/rfc/rfc4511.txt) | §4 Protocol Model; BindRequest; SearchRequest; BER message envelope | BER parser、bind/search 状态清楚，但配置成本中等。 | P2 | https://github.com/openldap/openldap | base `ubuntu:22.04`; deps `build-essential git groff libssl-dev libsasl2-dev`; build `./configure && make depend && make`; run `servers/slapd/slapd -d 1 -f slapd.conf` |
| FreeRADIUS | RADIUS | [RFC 2865](https://www.rfc-editor.org/rfc/rfc2865.txt); [RFC 2866](https://www.rfc-editor.org/rfc/rfc2866.txt) | Access-Request; Identifier; Authenticator; Attribute format | UDP 认证协议，属性编码和认证状态适合隐式约束，但配置复杂。 | P2 | https://github.com/FreeRADIUS/freeradius-server | base `ubuntu:22.04`; deps `build-essential git libssl-dev libtalloc-dev`; build `./configure && make`; run `build/bin/local/radiusd -X` |
| FRRouting | BGP-4 | [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271.txt) | §4 Message Formats; §6 FSM; OPEN/UPDATE/KEEPALIVE | 路由控制面重要，FSM 典型，但实验环境较重。 | P2 | https://github.com/FRRouting/frr | base `ubuntu:22.04`; deps `build-essential git autoconf automake libtool libreadline-dev`; build `./bootstrap.sh && ./configure && make`; run `bgpd -f bgpd.conf -d` |
| Postfix | SMTP | [RFC 5321](https://www.rfc-editor.org/rfc/rfc5321.txt) | §4.1 SMTP Commands; MAIL/RCPT/DATA state; reply codes | 邮件状态机清楚，但服务配置和依赖较多。 | P2 | https://github.com/vdukhovni/postfix | base `ubuntu:22.04`; deps `build-essential git libdb-dev libssl-dev`; build `make makefiles && make`; run `master -d` |
| Dovecot | IMAP / POP3 | [RFC 9051](https://www.rfc-editor.org/rfc/rfc9051.txt); [RFC 1939](https://www.rfc-editor.org/rfc/rfc1939.txt) | IMAP command states; literal parsing; POP3 authorization/transaction/update | 邮件读取协议状态明显，适合后期 parser/state 约束。 | P2 | https://github.com/dovecot/core | base `ubuntu:22.04`; deps `build-essential git autoconf automake libtool libssl-dev`; build `./autogen.sh && ./configure && make`; run `dovecot -F -c dovecot.conf` |
| Redis | Redis RESP | [Redis protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec/) | RESP array/bulk string; command arity; inline protocol | 非 RFC，但线协议简单，适合快速 parser harness。 | P2 | https://github.com/redis/redis | base `ubuntu:22.04`; deps `build-essential git tcl`; build `make`; run `src/redis-server --protected-mode no` |
| memcached | Memcached text/binary | [Memcached protocol](https://github.com/memcached/memcached/blob/master/doc/protocol.txt) | text command grammar; binary header; key/value length | 非 RFC，协议简单，适合作为缓存线协议扩展。 | P2 | https://github.com/memcached/memcached | base `ubuntu:22.04`; deps `build-essential git autoconf libevent-dev`; build `./autogen.sh && ./configure && make`; run `./memcached -u root -p 11211` |
| PostgreSQL | PostgreSQL wire protocol | [PostgreSQL protocol](https://www.postgresql.org/docs/current/protocol.html) | StartupMessage; Authentication; Query; ErrorResponse | 数据库线协议公开完整，startup/auth/query 状态适合隐式约束。 | P2 | https://github.com/postgres/postgres | base `ubuntu:22.04`; deps `build-essential git bison flex libreadline-dev zlib1g-dev`; build `./configure && make`; run `postgres -D data` |
| NATS Server | NATS protocol | [NATS protocol](https://docs.nats.io/reference/reference-protocols/nats-protocol) | CONNECT/INFO/PUB/SUB/MSG; subscription state | 非 RFC，但文本协议轻量，适合 message queue 扩展。 | P2 | https://github.com/nats-io/nats-server | base `ubuntu:22.04`; deps `git golang-go`; build `go build ./...`; run `./nats-server -DV` |
| Kamailio | SIP | [RFC 3261](https://www.rfc-editor.org/rfc/rfc3261.txt) | §7 SIP Messages; §8 UAC Behavior; §17 Transactions | SIP 状态机和 header parser 复杂，适合后期实时通信协议。 | P2 | https://github.com/kamailio/kamailio | base `ubuntu:22.04`; deps `build-essential git bison flex libssl-dev`; build `make cfg && make all`; run `kamailio -f kamailio.cfg -DD -E` |
| live555 | RTSP / RTP | [RFC 7826](https://www.rfc-editor.org/rfc/rfc7826.txt); [RFC 3550](https://www.rfc-editor.org/rfc/rfc3550.txt) | RTSP request/response; session; RTP sequence/timestamp | 流媒体协议，session 和序号约束明显；源码获取需复核。 | P2 | http://www.live555.com/liveMedia/ | base `ubuntu:22.04`; deps `build-essential wget`; build `./genMakefiles linux && make`; run `./testProgs/testOnDemandRTSPServer` |
| rsyslog | Syslog | [RFC 5424](https://www.rfc-editor.org/rfc/rfc5424.txt); [RFC 6587](https://www.rfc-editor.org/rfc/rfc6587.txt) | RFC 5424 message format; RFC 6587 octet-counting framing | 日志协议简单，TCP framing 适合 parser 边界研究。 | P2 | https://github.com/rsyslog/rsyslog | base `ubuntu:22.04`; deps `build-essential git autoconf automake libtool pkg-config`; build `autoreconf -fvi && ./configure && make`; run `tools/rsyslogd -n -f rsyslog.conf` |
| Fast DDS | DDS-RTPS | [OMG DDSI-RTPS](https://www.omg.org/spec/DDSI-RTPS/) | RTPS submessage; participant discovery; reliability state | 工业/机器人常用，协议复杂，作为后期覆盖项。 | P3 | https://github.com/eProsima/Fast-DDS | base `ubuntu:22.04`; deps `build-essential git cmake`; build `cmake -S . -B build && cmake --build build`; run `examples/C++/HelloWorldExample` |

## 5. 第一轮推荐 Dataset 切分

| 级别 | Subject | 选择理由 |
|---|---|---|
| 必须纳入 | Sol, Mosquitto, libcoap, FreeCoAP, llhttp, HAProxy, nghttp2 | 覆盖论文 MQTT/CoAP 基线和必须补的 HTTP/1.1/HTTP/2；都具备明确 Section binding 和较好的 Docker 可执行性。 |
| 建议纳入 | Dnsmasq, BIND 9, pure-ftpd, TLSE, quiche, ngtcp2/nghttp3, librdkafka | 覆盖 DNS/FTP/TLS/QUIC/Kafka，能支撑跨 Protocol 泛化，但构建或状态空间更复杂。 |
| 后期纳入 | wolfSSL, OpenSSL, RabbitMQ, Apache Kafka, Net-SNMP, open62541 | 研究价值高，但第一轮容易被环境和状态爆炸拖慢。 |
| Artifact 待确认 | TinyMQTT, uFTP, NDHS | 论文 Table I 必须保留在调研中，但上游和可执行路径要先从 artifact 复核。 |

## 6. 设计说明

### 6.1 为什么从 Protocol-centered 改为 Implementation-centered

本课题最终要做的是 implementation-based experiments。Protocol 只能说明标准对象，例如 MQTT、CoAP、HTTP/2；真正能被构建、运行、插桩、fuzzing、复现实验的是 Implementation，例如 Mosquitto、libcoap、nghttp2。NDSS/USENIX 风格的实验对象表通常以 Subject 为主，因为后续所有证据链都要落到具体代码仓库、commit、build command、run command 和测试输入。

### 6.2 为什么需要 Section-level binding

implicit constraint 不是凭空生成的。每条候选约束都必须绑定到 Specification 的具体 Section、字段、消息类型或状态语义。例如 HTTP/1.1 的 Content-Length/Transfer-Encoding、MQTT CONNECT Client Identifier、CoAP Option Parsing、DNS Compression Pointer、TLS supported_versions。Section-level binding 是 CVE -> rule -> code slice -> constraint 的 grounding key。

### 6.3 为什么 Docker execution 是实验基础

后续 T4/T7 如果要比较不同实现，必须保证每个 Subject 都能在统一环境中构建和运行。Docker recipe 至少要固定 base image、dependencies、build command、run command。没有 Docker execution，调研表只能算资料清单，不能支撑 reproducible experimental dataset。

### 6.4 为什么 P0/P1/P2 需要可解释性

P0/P1/P2 不是主观排序，而是实验可行性判断。P0 应该具备简单状态机、输入容易构造、Specification Section 清楚、Docker 可运行、容易做 cross-implementation comparison 等特点；P2/P3 则通常是因为状态空间大、依赖复杂、harness 成本高或 artifact 来源未确认。可解释优先级能帮助课题组决定第一轮做什么、哪些放到后期。

## 7. 后续需要补的工作

1. 从 `draft/artifacts/ProtocolGuard.zip` 或 Zenodo 下载包中确认 TinyMQTT、uFTP、NDHS 的完整路径、commit、license 和 build/run command。
2. 为 P0 subject 建立真实 Dockerfile，并把 recipe 从“调研线索”升级为“实测命令”。
3. 为每个 subject 固定 commit/tag，避免后续上游变化导致实验不可复现。
4. 把每个 Section binding 继续细化到具体 rule text，形成后续 CVE mapping 和 implicit constraint extraction 的输入。
