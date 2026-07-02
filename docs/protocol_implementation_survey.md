# NDSS 风格 Implementation-centered 协议与实现调研表

本文参考 ProtocolGuard 论文 Table I 的组织方式，对候选协议及其开源 Implementation 进行 Implementation-centered 调研。调研重点包括协议标准来源、Specification Section / Field Binding、实现代码来源、Artifact 可确认情况，以及推荐 Pilot 选择。

## 1. ProtocolGuard Artifact 核对

本节记录 ProtocolGuard 论文、公开仓库和 Artifact 对本调研的参考价值。这里的结论仅用于确认调研来源，不表示本仓库已经复现完整实验流程。

| 来源 | 调研结论 | 参考价值 |
|---|---|---|
| GitHub `songxpu/ProtocolGuard` | 官方 README 给出 Ubuntu 22.04.3 LTS、Python 3.10、Go 1.18.1、LLVM 12/14、Cursor、GLLVM、SVF、Scapy、AFLNet 等环境线索。 | 可作为后续 Docker recipe、静态分析依赖和 ProtocolGuard-style workflow 的参考。 |
| Zenodo `10.5281/zenodo.17933922` | Zenodo 标题为 `Artifact of the paper: ProtocolGuard`，open access，Apache-2.0，文件为 `ProtocolGuard.zip`。 | 可用于核对论文 Artifact 结构、模块划分和 worked example。 |
| `draft/artifacts/ProtocolGuard.zip` | 当前仓库保留的 Artifact 副本包含 `rule_extraction/`、`program_slicing/`、`inconsistency_detection/`、`dynamic_verification/`、`config/config.toml`、`example/sol.tar.gz`。 | 可确认 Sol worked example；其他论文 Table I Subject 的完整源码路径仍需复核。 |

Artifact 中可以确认的路径：

| Artifact path | 对应论文模块 | 说明 |
|---|---|---|
| `ProtocolGuard/rule_extraction/` | Protocol Rule Extraction | RFC/OASIS 文档处理、keyword 处理、rule 处理。 |
| `ProtocolGuard/program_slicing/` | LLM-guided Program Slicing | 可以确认存在静态分析框架入口、头文件和 CMake 结构；但当前上传的压缩包中 `src/` 核心 pass 源码不完整，需要后续从完整 Zenodo Artifact 或作者仓库复核。 |
| `ProtocolGuard/inconsistency_detection/violation_check.py` | LLM-based Inconsistency Detection | 用 LLM 比较 rule 与 code slice。 |
| `ProtocolGuard/dynamic_verification/assert_generate/` | Assertion Generation | 生成 assertion 插桩任务。 |
| `ProtocolGuard/dynamic_verification/packet_generate/` | Test Case Generation | 生成反例、Scapy 脚本、PCAP/raw payload。 |
| `ProtocolGuard/dynamic_verification/DFUZZ/` | Directed Protocol Fuzzing | 选择性插桩和 directed fuzzing 相关 pass。 |
| `ProtocolGuard/example/sol.tar.gz` | Worked Example | 可以确认包含 Sol 源码、Dockerfile、bitcode、SQLite DB、rule_config 和构建产物。 |

## 2. NDSS 风格实验对象主表

主表参考 ProtocolGuard Table I，但增加 Version / Commit / Tag、Section / Field Binding 和 Repo / Artifact Source，用于建立 Specification 到 Implementation 的对应关系。

| Subject (Implementation) | Protocol | Version / Commit / Tag | Specification | Spec Section / Field Binding | Repo / Artifact Source |
|---|---|---|---|---|---|
| Sol | MQTT 3.1.1 | `373d8` | [OASIS MQTT 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) | §3.1 CONNECT; §3.1.3.1 Client Identifier; §3.8 SUBSCRIBE | https://github.com/codepr/sol; `ProtocolGuard.zip/example/sol.tar.gz` confirmed |
| TinyMQTT | MQTT 3.1.1 | `6226ad`（源码未确认） | [OASIS MQTT 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) | §3.1 CONNECT; §3.1.3.1 Client Identifier; §3.3 PUBLISH; §3.8 SUBSCRIBE | 论文 Table I 中的 Subject；当前上传的 `ProtocolGuard.zip` 中未确认源码路径。已检查候选仓库 https://github.com/hsaturn/TinyMqtt，但该仓库主要面向 ESP8266/ESP32，语言以 C++ 为主，且未确认论文版本 `6226ad`，因此暂不确认，继续标记为 pending。 |
| Mosquitto | MQTT 5.0 | `849e0f` | [OASIS MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) | §3.1 CONNECT; §3.8 SUBSCRIBE; §3.9 SUBACK; §4.13 Handling Errors | https://github.com/eclipse-mosquitto/mosquitto |
| libcoap | CoAP | `17c3fe` | [RFC 7252](https://www.rfc-editor.org/rfc/rfc7252.txt) | §3 Message Format; §4 Message Transmission; §5.3 Request/Response Matching; §5.4 Options | https://github.com/obgm/libcoap |
| FreeCoAP | CoAP | `3adc2e` | [RFC 7252](https://www.rfc-editor.org/rfc/rfc7252.txt) | §3 Message Format; §5.4 Options; §5.10 Response Code | https://github.com/keith-cullen/FreeCoAP |
| Dnsmasq | DHCPv6 / DNS | `2.91` | [RFC 8415](https://www.rfc-editor.org/rfc/rfc8415.txt); [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.txt) | RFC 8415 §7 Message Formats; §18 Client/Server Exchanges; RFC 1035 §4.1.4 Compression | https://thekelleys.org.uk/gitweb/?p=dnsmasq.git;a=summary |
| NDHS | DHCPv6 | `4b2728`; 候选上游 commit `4b2728a` | [RFC 8415](https://www.rfc-editor.org/rfc/rfc8415.txt) | §7 Message Formats; §18 Client/Server Exchanges; §21 Options | 候选上游已确认：https://github.com/niklata/ndhs；论文版本前缀 `4b2728` 可对应到 commit `4b2728a`；协议为 DHCPv4/DHCPv6 server，语言以 C 为主。当前状态：candidate upstream confirmed；commit `4b2728a` confirmed；Docker validation pending。 |
| pure-ftpd | FTP / FTPS | `381857` | [RFC 959](https://www.rfc-editor.org/rfc/rfc959.txt); [RFC 2228](https://www.rfc-editor.org/rfc/rfc2228.txt); [RFC 3659](https://www.rfc-editor.org/rfc/rfc3659.txt) | RFC 959 §4.1.1 Access Control Commands; RFC 2228 AUTH/PBSZ/PROT; RFC 3659 REST/SIZE/MLST | https://github.com/jedisct1/pure-ftpd |
| uFTP | FTP / FTPS | `646404`（源码未确认） | [RFC 959](https://www.rfc-editor.org/rfc/rfc959.txt); [RFC 2228](https://www.rfc-editor.org/rfc/rfc2228.txt); [RFC 3659](https://www.rfc-editor.org/rfc/rfc3659.txt) | RFC 959 §4.1.1 USER/PASS/RNFR/RNTO; RFC 2228 AUTH/PBSZ/PROT; RFC 3659 REST | 论文 Table I 中的 Subject；当前上传的 `ProtocolGuard.zip` 中未确认源码路径。已检查候选仓库 https://github.com/troglobit/uftpd，该仓库是 C 语言 FTP/TFTP server，但未确认论文版本 `646404`，且未确认支持 RFC 2228 中的 AUTH/PBSZ/PROT 或 FTPS 语义，因此暂不确认，继续标记为 pending。 |
| TLSE | TLS 1.3 | `1af154` | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt) | §4 Handshake Protocol; §4.1 Key Exchange Messages; §4.2 Extensions | https://github.com/eduardsui/tlse |
| wolfSSL | TLS 1.3 | `7fb750` | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt) | §4.1 Handshake Protocol; §4.2.1 Supported Versions; §4.6.1 NewSessionTicket | https://github.com/wolfSSL/wolfssl |
| llhttp | HTTP/1.1 parser | `v9.4.2` | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9112 §2 Message; §3 Request Line; §5 Field Syntax; §6 Message Body | https://github.com/nodejs/llhttp |
| HAProxy | HTTP/1.1 proxy | `v3.4.0` | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9112 §6.1 Transfer-Encoding; §6.2 Content-Length; §9.3 Message Parsing Robustness | https://github.com/haproxy/haproxy |
| nginx | HTTP/1.1 server/proxy | `release-1.31.2` | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9112 §3 Request Target; §5 Field Syntax; §6 Message Body | https://github.com/nginx/nginx |
| Apache httpd | HTTP/1.1 server | `2.4.68` | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.txt); [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt) | RFC 9110 §7 Routing HTTP Messages; RFC 9112 §6 Message Body | https://github.com/apache/httpd |
| nghttp2 | HTTP/2 | `v1.69.0` | [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113.txt); [RFC 7541](https://www.rfc-editor.org/rfc/rfc7541.txt) | RFC 9113 §4 Frames; §5 Streams; §6 Frame Definitions; RFC 7541 §2.3 Header Table | https://github.com/nghttp2/nghttp2 |
| h2o | HTTP/2 / HTTP/1.1 | `v2.2.6` | [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.txt); [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113.txt) | RFC 9113 §5 Stream States; §6.5 SETTINGS; RFC 9112 §6 Message Body | https://github.com/h2o/h2o |
| quiche | QUIC / HTTP/3 | `0.29.2` | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.txt); [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.txt); [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.txt); [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.txt) | RFC 9000 §4 Streams; §12 Packets and Frames; RFC 9114 §6 Stream Mapping; §7.2 SETTINGS | https://github.com/cloudflare/quiche |
| ngtcp2 + nghttp3 | QUIC / HTTP/3 | ngtcp2 `v1.24.0`; nghttp3 `v1.17.0` | [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.txt); [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.txt) | RFC 9000 §7 Connection Establishment; §10 Connection Termination; RFC 9114 §4 HTTP/3 Frames | https://github.com/ngtcp2/ngtcp2; https://github.com/ngtcp2/nghttp3 |
| BIND 9 | DNS | `v9.21.23` | [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.txt); [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.txt); [RFC 6891](https://www.rfc-editor.org/rfc/rfc6891.txt) | RFC 1035 §4.1.1 Header; §4.1.4 Message Compression; RFC 6891 §6 OPT RR | https://gitlab.isc.org/isc-projects/bind9 |
| miekg/dns | DNS library | `v1.1.72` | [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.txt); [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035.txt) | RFC 1035 §4.1.2 Question; §4.1.3 Resource Records; §4.1.4 Compression | https://github.com/miekg/dns |
| OpenSSL | TLS 1.3 / DTLS | `openssl-4.0.1` | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt); [RFC 9147](https://www.rfc-editor.org/rfc/rfc9147.txt) | RFC 8446 §4 Handshake; RFC 9147 §5 Record Layer; §7 Handshake | https://github.com/openssl/openssl |
| mbedTLS | TLS 1.3 / DTLS | `mbedtls-4.1.0` | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.txt); [RFC 9147](https://www.rfc-editor.org/rfc/rfc9147.txt) | RFC 8446 §4.2 Extensions; RFC 9147 §4.2 Epoch and Sequence Number | https://github.com/Mbed-TLS/mbedtls |
| Apache Qpid Proton | AMQP 1.0 | `0.40.0` | [OASIS AMQP 1.0](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.html) | AMQP 1.0 Transport: Connections, Sessions, Links, Frames, Delivery State | https://github.com/apache/qpid-proton |
| RabbitMQ | AMQP 0-9-1 / AMQP 1.0 plugin | `v4.3.2` | [AMQP 0-9-1](https://www.rabbitmq.com/resources/specs/amqp0-9-1.pdf); [OASIS AMQP 1.0](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.html) | AMQP 0-9-1 Method Frame; Connection.Start/Tune/Open; Channel.Open; Queue.Declare | https://github.com/rabbitmq/rabbitmq-server |
| librdkafka | Kafka Protocol | `v2.15.0` | [Apache Kafka Protocol](https://kafka.apache.org/protocol) | Request Header; ApiVersions; Metadata; Produce; Fetch; Consumer Group APIs | https://github.com/confluentinc/librdkafka |
| Apache Kafka | Kafka Protocol | `4.3.1` | [Apache Kafka Protocol](https://kafka.apache.org/protocol) | ApiVersions; Metadata; Produce; Fetch; JoinGroup/SyncGroup | https://github.com/apache/kafka |
| Dropbear SSH | SSH | `DROPBEAR_2026.91` | [RFC 4251](https://www.rfc-editor.org/rfc/rfc4251.txt); [RFC 4252](https://www.rfc-editor.org/rfc/rfc4252.txt); [RFC 4253](https://www.rfc-editor.org/rfc/rfc4253.txt); [RFC 4254](https://www.rfc-editor.org/rfc/rfc4254.txt) | RFC 4253 §7 Key Exchange; RFC 4252 §5 Authentication; RFC 4254 §5 Channel Mechanism | https://github.com/mkj/dropbear |
| chrony | NTPv4 | `4.8` | [RFC 5905](https://www.rfc-editor.org/rfc/rfc5905.txt) | §7 Packet Format; §8 On-Wire Protocol; §9 Peer Process | https://gitlab.com/chrony/chrony |
| Net-SNMP | SNMPv3 | `v5.9.5.2` | [RFC 3411](https://www.rfc-editor.org/rfc/rfc3411.txt); [RFC 3412](https://www.rfc-editor.org/rfc/rfc3412.txt); [RFC 3414](https://www.rfc-editor.org/rfc/rfc3414.txt) | RFC 3412 §6 Message Processing; RFC 3414 §3 USM Timeliness; §3.2 Message Security | https://github.com/net-snmp/net-snmp |
| libmodbus | Modbus TCP | `v3.1.12` | [Modbus Application Protocol](https://modbus.org/specs.php) | MBAP Header; Function Code; Length Field; Unit Identifier | https://github.com/stephane/libmodbus |
| open62541 | OPC UA | `v1.5.5` | [OPC UA Core Specification](https://reference.opcfoundation.org/Core/) | SecureChannel; Session; MessageChunk; Service Request/Response | https://github.com/open62541/open62541 |

### 2.1 Version / LoC 核对表

本表用于集中记录 Version / Commit / Tag 与 LoC。ProtocolGuard Table I 中已有的 11 个 Subject 使用论文表格给出的 Version 和 LoC；新增候选 Subject 已优先选择 upstream 的稳定 tag/release。新增项的 LoC 暂记为“待统计”，后续应在固定 tag 上用统一工具统计，避免不同分支或统计口径导致不可复现。

| Subject (Implementation) | Protocol | Version / Commit / Tag | LoC | LoC 来源 / 状态 |
|---|---|---|---|---|
| Sol | MQTT 3.1.1 | `373d8` | 4.4K | ProtocolGuard Table I |
| TinyMQTT | MQTT 3.1.1 | `6226ad`（源码未确认） | 11.5K | ProtocolGuard Table I；源码路径 pending |
| Mosquitto | MQTT 5.0 | `849e0f` | 46.2K | ProtocolGuard Table I |
| libcoap | CoAP | `17c3fe` | 45.3K | ProtocolGuard Table I |
| FreeCoAP | CoAP | `3adc2e` | 26.6K | ProtocolGuard Table I |
| pure-ftpd | FTP / FTPS | `381857` | 22.2K | ProtocolGuard Table I |
| uFTP | FTP / FTPS | `646404`（源码未确认） | 6.7K | ProtocolGuard Table I；源码路径 pending |
| TLSE | TLS 1.3 | `1af154` | 41.8K | ProtocolGuard Table I |
| wolfSSL | TLS 1.3 | `7fb750` | 1456.3K | ProtocolGuard Table I |
| Dnsmasq | DHCPv6 / DNS | `2.91` | 33.4K | ProtocolGuard Table I |
| NDHS | DHCPv6 | `4b2728`; 候选上游 commit `4b2728a` | 5.6K | ProtocolGuard Table I；candidate upstream / commit 已确认，Docker validation pending |
| llhttp | HTTP/1.1 parser | `v9.4.2` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| HAProxy | HTTP/1.1 proxy | `v3.4.0` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| nginx | HTTP/1.1 server/proxy | `release-1.31.2` | 待统计 | 已选择 upstream release tag；LoC 后续在该 tag 上统计 |
| Apache httpd | HTTP/1.1 server | `2.4.68` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| nghttp2 | HTTP/2 | `v1.69.0` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| h2o | HTTP/2 / HTTP/1.1 | `v2.2.6` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| quiche | QUIC / HTTP/3 | `0.29.2` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| ngtcp2 + nghttp3 | QUIC / HTTP/3 | ngtcp2 `v1.24.0`; nghttp3 `v1.17.0` | 待统计 | 已分别选择 ngtcp2/nghttp3 upstream 稳定 tag；LoC 后续分别统计后汇总 |
| BIND 9 | DNS | `v9.21.23` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| miekg/dns | DNS library | `v1.1.72` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| OpenSSL | TLS 1.3 / DTLS | `openssl-4.0.1` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| mbedTLS | TLS 1.3 / DTLS | `mbedtls-4.1.0` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Apache Qpid Proton | AMQP 1.0 | `0.40.0` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| RabbitMQ | AMQP 0-9-1 / AMQP 1.0 plugin | `v4.3.2` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| librdkafka | Kafka Protocol | `v2.15.0` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Apache Kafka | Kafka Protocol | `4.3.1` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Dropbear SSH | SSH | `DROPBEAR_2026.91` | 待统计 | 已选择 upstream release tag；LoC 后续在该 tag 上统计 |
| chrony | NTPv4 | `4.8` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Net-SNMP | SNMPv3 | `v5.9.5.2` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| libmodbus | Modbus TCP | `v3.1.12` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| open62541 | OPC UA | `v1.5.5` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| lwIP | TCP/IP stack | `STABLE-2_0_1` | 待统计 | 已选择 upstream stable tag；LoC 后续在该 tag 上统计 |
| lksctp-tools | SCTP | `v1.0.21` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| libwebsockets | WebSocket | `v4.5.8` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| OpenLDAP | LDAPv3 | `OPENLDAP_REL_ENG_2_6_13` | 待统计 | 已选择 upstream release tag；LoC 后续在该 tag 上统计 |
| FreeRADIUS | RADIUS | `release_3_2_10` | 待统计 | 已选择 upstream release tag；LoC 后续在该 tag 上统计 |
| FRRouting | BGP-4 | `frr-10.6.1` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Postfix | SMTP | `v3.11.4` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Dovecot | IMAP / POP3 | `2.4.4` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Redis | Redis RESP | `8.8.0` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| memcached | Memcached text/binary | `1.6.42` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| PostgreSQL | PostgreSQL wire protocol | `REL_18_4` | 待统计 | 已选择 upstream release tag；LoC 后续在该 tag 上统计 |
| NATS Server | NATS protocol | `v2.14.3` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Kamailio | SIP | `6.1.3` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| live555 | RTSP / RTP | upstream release package 待确认 | 待统计 | live555 非 GitHub tag 形态；需后续固定源码包日期版本 |
| rsyslog | Syslog | `v8.2606.0` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |
| Fast DDS | DDS-RTPS | `v3.6.1` | 待统计 | 已选择 upstream 稳定 tag；LoC 后续在该 tag 上统计 |

## 3. 推荐试点（Pilot Recommendation）

Pilot Recommendation 是 Protocol-group-level 的选择，用于确定优先验证哪一类协议组；Priority 是 Subject-level 的实验可行性排序，用于说明单个 Implementation 的可执行难度和研究价值。两者不等价：例如 CoAP Pilot 包含 libcoap 和 FreeCoAP，而 libcoap、FreeCoAP 各自仍有独立 Priority。

| 推荐级别 | 试点协议组 | 推荐 Subject | 推荐理由 | 备注 |
|---|---|---|---|---|
| 首选试点 1 | CoAP | libcoap, FreeCoAP | RFC 7252 清楚，两个独立 C 实现，Message ID、Token、Options 适合约束分析，实现规模适中。 | RFC-only；适合作为最稳的第一组 Pilot。 |
| 首选试点 2 | HTTP/1.1 / HTTP/2 | llhttp, HAProxy, nginx, nghttp2 | RFC 9110/9112/9113 成熟，parser、Content-Length、Transfer-Encoding、frame、stream state 约束典型，实现丰富，输入容易构造。 | RFC-only；适合覆盖 parser 与 framing/state 两类约束。 |
| 备选试点 3 | DNS | BIND 9, miekg/dns, Dnsmasq | RFC 1035 / EDNS 约束丰富，compression pointer、label length、cache behavior 典型。 | RFC-only；配置和状态复杂度高于 CoAP/HTTP。 |
| 动机/对照 | MQTT | Sol, Mosquitto | ProtocolGuard baseline 和动机案例，ClientId、CONNECT、SUBACK 适合解释隐式约束。 | MQTT 是 OASIS 标准，不是 RFC；若要求 RFC-only，则不作为正式 Pilot。 |

## 4. Subject 优先级补充表

Priority 是 Subject-level 的实验可行性排序；推荐 Pilot 是 Protocol-group-level 的选择。

| Priority | 含义 | 排序依据 |
|---|---|---|
| P0 | 第一轮优先实验对象 | Docker 较容易跑；Specification 清楚；Section/Field binding 明确；输入可构造；implicit constraint 典型。 |
| P1 | 第二轮扩展对象 | 研究价值高且可执行，但状态机、依赖或工程复杂度高于 P0。 |
| P2 | 后期高价值对象 | 协议重要，但构建、状态空间、依赖或 harness 成本较高。 |
| P3 | 暂存备选对象 | 覆盖面有价值，但不建议在初始 Pilot 中投入。 |
| Pending | 来源待确认对象 | 论文中出现，但当前 Artifact 不能确认完整源码、commit 或 build/run 路径。 |

| Subject | Reason (Experiment Feasibility) | Priority |
|---|---|---|
| Sol | 论文 case study 和 Artifact worked example；状态机小，packet injection 容易，适合作为 ProtocolGuard baseline。 | P0 |
| TinyMQTT | 论文 Table I 中的 MQTT 3.1.1 Subject；当前上传 Artifact 未确认源码路径。已检查候选仓库 `hsaturn/TinyMqtt`，但该仓库主要是 C++ / Arduino / ESP 场景，且未确认版本 `6226ad`，暂不作为 confirmed subject。 | Pending |
| Mosquitto | 成熟 MQTT broker，Specification 清楚，可复用 CVE-2024-10525 的 SUBACK cardinality 线索。 | P0 |
| libcoap | Token、Message ID、Option parsing 都适合 implicit constraint；先限定 UDP 路径即可启动。 | P0 |
| FreeCoAP | 小型 CoAP 实现，适合和 libcoap 做 cross-implementation comparison。 | P0 |
| Dnsmasq | 论文 Table I DHCPv6 subject；同时覆盖 DNS/DHCP 基础设施协议，但配置和权限更复杂。 | P1 |
| NDHS | 论文 Table I 中的 DHCPv6 Subject；候选上游 `niklata/ndhs` 与协议、语言和版本前缀基本匹配，commit `4b2728a` 已确认；但仍需 Docker 编译、配置和最小输入验证。 | P1 |
| pure-ftpd | AUTH/PBSZ/PROT/REST/RNFR/RNTO 状态约束典型，构建可行但服务配置略重。 | P1 |
| uFTP | 论文 Table I 和 case study 涉及 FTP / FTPS 状态约束；已检查候选仓库 `troglobit/uftpd`，但未确认版本 `646404`，且未确认 AUTH/PBSZ/PROT 或 FTPS 支持，暂不作为 confirmed subject。 | Pending |
| TLSE | 轻量 TLS 实现，适合先做 supported_versions、key_share、certificate 等规则。 | P1 |
| wolfSSL | 论文 case study 已发现 version negotiation downgrade；价值高但代码量大。 | P2 |
| llhttp | HTTP parser bug 和 implicit constraint 最典型；轻量 parser 适合第一轮 harness。 | P0 |
| HAProxy | HTTP desync、header/body 边界、connection reuse 典型；Docker 化相对容易。 | P0 |
| nginx | 成熟 HTTP server/proxy，适合和 HAProxy/Apache 做 cross-implementation comparison。 | P0 |
| Apache httpd | 标准服务器实现；可对照 nginx/HAProxy，但依赖略多。 | P1 |
| nghttp2 | HTTP/2 frame length、stream state、HPACK、SETTINGS grounding 强。 | P0 |
| h2o | 同时支持 HTTP/1.1/2，适合 server 行为对照；复杂度中等。 | P1 |
| quiche | QUIC/HTTP3 状态机典型，现代性强，但 Rust/Cargo 和 TLS 依赖较多。 | P1 |
| ngtcp2 + nghttp3 | C 生态 QUIC/HTTP3 对照对象，构建链比 quiche 更复杂。 | P1 |
| BIND 9 | DNS compression pointer 和 EDNS 边界价值高，但构建与配置较重。 | P1 |
| miekg/dns | Go 库易写 harness，适合先构造 compression/label 边界输入。 | P1 |
| OpenSSL | 生态核心，但代码大、状态多，适合后期验证 TLS/DTLS 泛化性。 | P2 |
| mbedTLS | 嵌入式 TLS/DTLS，适合 IoT 场景，比 OpenSSL 小。 | P1 |
| Apache Qpid Proton | AMQP 有正式 Specification，frame/link/session 状态适合 implicit constraint。 | P1 |
| RabbitMQ | 工业常用 MQ，功能复杂，适合作为后期 broker 行为对象。 | P2 |
| librdkafka | Kafka 非 RFC 但工业价值高；C/C++ 客户端库适合 Docker harness。 | P1 |
| Apache Kafka | 协议价值高但 Java/集群运行成本高于 librdkafka。 | P2 |
| Dropbear SSH | 小型 SSH 实现，key exchange/auth/channel 状态清楚。 | P1 |
| chrony | UDP 基础设施协议，packet field 和 state 约束清楚。 | P1 |
| Net-SNMP | ASN.1/BER parser、security model、engineBoots/time 适合隐式约束，但配置复杂。 | P2 |
| libmodbus | 工控协议小，TCP payload 简单，适合作为非 Web/IoT 扩展。 | P1 |
| open62541 | 工控/IoT 价值高，但 Specification 和状态较复杂。 | P2 |
| lwIP | 真正传输层实现，适合后期验证 TCP/UDP 约束，但 harness 成本较高。 | P2 |
| lksctp-tools | SCTP 是传输层补充，状态复杂，先作为覆盖候选。 | P3 |
| libwebsockets | WebSocket frame length/masking/fragmentation 隐式约束清楚。 | P1 |
| OpenLDAP | BER parser、bind/search 状态清楚，但配置成本中等。 | P2 |
| FreeRADIUS | UDP 认证协议，属性编码和认证状态适合隐式约束，但配置复杂。 | P2 |
| FRRouting | 路由控制面重要，FSM 典型，但实验环境较重。 | P2 |
| Postfix | SMTP 状态机清楚，但服务配置和依赖较多。 | P2 |
| Dovecot | IMAP/POP3 parser/state 明显，适合后期 parser/state 约束。 | P2 |
| Redis | 非 RFC，但线协议简单，适合快速 parser harness。 | P2 |
| memcached | 非 RFC，协议简单，适合作为缓存线协议扩展。 | P2 |
| PostgreSQL | 公开 wire protocol 完整，startup/auth/query 状态适合隐式约束。 | P2 |
| NATS Server | 非 RFC，但文本协议轻量，适合 message queue 扩展。 | P2 |
| Kamailio | SIP 状态机和 header parser 复杂，适合后期实时通信协议。 | P2 |
| live555 | 流媒体协议，session 和序号约束明显；源码获取需复核。 | P2 |
| rsyslog | 日志协议简单，TCP framing 适合 parser 边界研究。 | P2 |
| Fast DDS | 工业/机器人常用，协议复杂，作为后期覆盖项。 | P3 |

## 5. 候选扩展池

扩展池仅用于后续选题参考，不作为推荐 Pilot。

| Subject (Implementation) | Protocol | Specification | Spec Section / Field Binding | Repo / Artifact Source |
|---|---|---|---|---|
| lwIP | TCP/IP stack | [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.txt); [RFC 768](https://www.rfc-editor.org/rfc/rfc768.txt) | TCP state machine; sequence number; reassembly; UDP datagram boundary | https://git.savannah.nongnu.org/cgit/lwip.git |
| lksctp-tools | SCTP | [RFC 9260](https://www.rfc-editor.org/rfc/rfc9260.txt) | Association setup; multi-streaming; DATA chunk; SACK | https://github.com/sctp/lksctp-tools |
| libwebsockets | WebSocket | [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.txt) | §4 Opening Handshake; §5 Data Framing; masking; fragmentation | https://github.com/warmcat/libwebsockets |
| OpenLDAP | LDAPv3 | [RFC 4511](https://www.rfc-editor.org/rfc/rfc4511.txt) | §4 Protocol Model; BindRequest; SearchRequest; BER message envelope | https://github.com/openldap/openldap |
| FreeRADIUS | RADIUS | [RFC 2865](https://www.rfc-editor.org/rfc/rfc2865.txt); [RFC 2866](https://www.rfc-editor.org/rfc/rfc2866.txt) | Access-Request; Identifier; Authenticator; Attribute format | https://github.com/FreeRADIUS/freeradius-server |
| FRRouting | BGP-4 | [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271.txt) | §4 Message Formats; §6 FSM; OPEN/UPDATE/KEEPALIVE | https://github.com/FRRouting/frr |
| Postfix | SMTP | [RFC 5321](https://www.rfc-editor.org/rfc/rfc5321.txt) | §4.1 SMTP Commands; MAIL/RCPT/DATA state; reply codes | https://github.com/vdukhovni/postfix |
| Dovecot | IMAP / POP3 | [RFC 9051](https://www.rfc-editor.org/rfc/rfc9051.txt); [RFC 1939](https://www.rfc-editor.org/rfc/rfc1939.txt) | IMAP command states; literal parsing; POP3 authorization/transaction/update | https://github.com/dovecot/core |
| Redis | Redis RESP | [Redis protocol specification](https://redis.io/docs/latest/develop/reference/protocol-spec/) | RESP array/bulk string; command arity; inline protocol | https://github.com/redis/redis |
| memcached | Memcached text/binary | [Memcached protocol](https://github.com/memcached/memcached/blob/master/doc/protocol.txt) | text command grammar; binary header; key/value length | https://github.com/memcached/memcached |
| PostgreSQL | PostgreSQL wire protocol | [PostgreSQL protocol](https://www.postgresql.org/docs/current/protocol.html) | StartupMessage; Authentication; Query; ErrorResponse | https://github.com/postgres/postgres |
| NATS Server | NATS protocol | [NATS protocol](https://docs.nats.io/reference/reference-protocols/nats-protocol) | CONNECT/INFO/PUB/SUB/MSG; subscription state | https://github.com/nats-io/nats-server |
| Kamailio | SIP | [RFC 3261](https://www.rfc-editor.org/rfc/rfc3261.txt) | §7 SIP Messages; §8 UAC Behavior; §17 Transactions | https://github.com/kamailio/kamailio |
| live555 | RTSP / RTP | [RFC 7826](https://www.rfc-editor.org/rfc/rfc7826.txt); [RFC 3550](https://www.rfc-editor.org/rfc/rfc3550.txt) | RTSP request/response; session; RTP sequence/timestamp | http://www.live555.com/liveMedia/ |
| rsyslog | Syslog | [RFC 5424](https://www.rfc-editor.org/rfc/rfc5424.txt); [RFC 6587](https://www.rfc-editor.org/rfc/rfc6587.txt) | RFC 5424 message format; RFC 6587 octet-counting framing | https://github.com/rsyslog/rsyslog |
| Fast DDS | DDS-RTPS | [OMG DDSI-RTPS](https://www.omg.org/spec/DDSI-RTPS/) | RTPS submessage; participant discovery; reliability state | https://github.com/eProsima/Fast-DDS |

## 6. 表格字段说明

| 字段 | 说明 |
|---|---|
| `Subject (Implementation)` | 具体代码实现，是后续可构建、运行、插桩、fuzzing 或对比分析的对象。 |
| `Specification` | 协议标准来源，优先使用 RFC、OASIS 或官方标准链接。 |
| `Version / Commit / Tag` | 用于固定代码版本。Specification 和 Section 说明“依据哪份标准”，commit/tag 说明“分析哪一版代码”。二者都需要保留，否则后续实验不可复现。 |
| `LoC` | 代码规模。论文 Table I Subject 使用论文给出的 LoC；新增 Subject 需要先固定 commit/tag，再用统一工具统计，避免不同分支或统计口径导致不可复现。 |
| `Spec Section / Field Binding` | 标准字段、消息、状态或 Section 位置，是后续 CVE 和约束分析的定位依据。 |
| `Repo / Artifact Source` | upstream 代码或 Artifact 中可确认的源码来源；不确定则标 `pending` 或“待确认”。 |
